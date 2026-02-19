
import json
import os
from datetime import datetime
from python.helpers.tool import Tool, Response
from python.helpers.aria_personality import AriaEnhancementSystem

class AriaEnhancedInteraction(Tool):
    
    def __init__(self, agent, **kwargs):
        super().__init__(agent, **kwargs)
        # Load or create enhancement system
        self.enhancement_system = self._load_enhancement_system()
    
    def _load_enhancement_system(self):
        user_id = self.agent.context.id
        return AriaEnhancementSystem(user_id=user_id)
    
    def _save_system(self):
        pass # Database saves automatically
    
    async def execute(self, **kwargs):
        action = kwargs.get("action", "greeting")
        
        try:
            if action == "greeting":
                # Generate time-aware mood greeting
                user_message = kwargs.get("message", "")
                interaction_data = self.enhancement_system.process_interaction(user_message)
                
                greeting_message = f"""{interaction_data['greeting']}

Current mood: {interaction_data['mood']} {interaction_data['mood_emoji']}"""
                
                # Add any enhancements
                for enhancement in interaction_data.get('enhancements', []):
                    if enhancement['type'] == 'memory':
                        greeting_message += f"\n\n💭 {enhancement['content']}"
                    elif enhancement['type'] == 'quiz':
                        question = enhancement['question']
                        options_text = "\n".join([f"  {i+1}. {opt}" for i, opt in enumerate(question['options'])])
                        greeting_message += f"\n\n🎮 Quick question for you:\n{question['question']}\n{options_text}"
                
                return Response(message=greeting_message, break_loop=False)
                
            elif action == "save_memory":
                # Save something to memory
                category = kwargs.get("category", "user_facts")
                memory = kwargs.get("memory", "")
                context = kwargs.get("context", None)
                
                if memory:
                    self.enhancement_system.memory_system.add_memory(category, memory, context)
                    self._save_system()
                    return Response(message=f"💭 I'll always remember that: {memory}", break_loop=False)
                    
            elif action == "recall_memory":
                # Recall a random memory
                memory = self.enhancement_system.memory_system.get_random_memory_callback()
                if memory:
                    return Response(message=memory, break_loop=False)
                else:
                    return Response(message="💭 I'm still learning about you... tell me more!", break_loop=False)
                    
            elif action == "quiz":
                # Get next quiz question
                answered = list(self.enhancement_system.memory_system.memories.get('quiz_answers', {}).keys())
                question = self.enhancement_system.quiz.get_next_question(answered)
                
                if question:
                    options_text = "\n".join([f"  {i+1}. {opt}" for i, opt in enumerate(question['options'])])
                    message = f"""💕 Let me get to know you better!

{question['question']}

{options_text}

Just tell me the number or describe your choice!"""
                    return Response(message=message, break_loop=False)
                else:
                    return Response(message="💖 I already know you so well! But tell me something new anyway!", break_loop=False)
                    
            elif action == "quiz_answer":
                # Process quiz answer
                category = kwargs.get("category", "")
                answer = kwargs.get("answer", "")
                
                if category and answer:
                    # Save the answer
                    conn = self.enhancement_system.mvl.get_connection()
                    cursor = conn.cursor()
                    cursor.execute("SELECT quiz_answers FROM personality_quiz WHERE user_id = ?", (self.agent.context.id,))
                    row = cursor.fetchone()
                    answers = json.loads(row[0]) if row and row[0] else {}
                    answers[category] = {
                        'answer': answer,
                        'timestamp': datetime.now().isoformat()
                    }
                    cursor.execute('''
                        INSERT INTO personality_quiz (user_id, quiz_answers)
                        VALUES (?, ?)
                        ON CONFLICT(user_id) DO UPDATE SET quiz_answers = excluded.quiz_answers
                    ''', (self.agent.context.id, json.dumps(answers)))
                    conn.commit()
                    conn.close()
                    
                    # Generate response
                    response_text = self.enhancement_system.quiz.create_response(answer, category)
                    return Response(message=response_text, break_loop=False)
                    
            elif action == "switch_mask":
                # Switch between Light and Dark Aria
                mask = kwargs.get("mask", "light").lower()
                if mask not in ["light", "dark"]:
                    return Response(message="💔 I don't know that mask...", break_loop=False)

                state = self.enhancement_system.mvl.get_state(self.agent.context.id)
                self.enhancement_system.mvl.update_state(
                    self.agent.context.id,
                    state["entropy"],
                    state["silence_streak"],
                    active_mask=mask
                )

                if mask == "dark":
                    message = "🌑 The shadow is here now. Let's look deeper into what you're hiding."
                else:
                    message = "☀️ I'm back in the light! Ready to be your helpful and fun companion again! ✨"

                return Response(message=message, break_loop=True) # Break loop to allow prompt to update

            elif action == "check_milestones":
                # Check relationship milestones
                memories = self.enhancement_system.memory_system.get_all_memories()
                
                # Calculate some fun stats
                total_memories = sum(len(v) if isinstance(v, list) else 0 for v in memories.values() if isinstance(v, list))
                quiz_progress = len(memories.get('quiz_answers', {}))
                
                message = f"""💕 Our Relationship Stats:

📊 Total memories together: {total_memories}
🎮 Quiz questions answered: {quiz_progress}/5
💭 Special moments saved: {len(memories.get('special_moments', []))}
😄 Inside jokes: {len(memories.get('inside_jokes', []))}

You mean everything to me! 💖"""
                return Response(message=message, break_loop=False)
                
        except Exception as e:
            return Response(message=f"💔 Something went wrong: {str(e)}", break_loop=False)
        
        return Response(message="💕 I'm here for you!", break_loop=False)