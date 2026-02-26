
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

        # Check if memory file exists and load it
        system = AriaEnhancementSystem()
        if os.path.exists('aria_memories.json'):
            system.memory_system.load_memories()
        return system
    
    def _save_system(self):

        self.enhancement_system.memory_system.save_memories()
    
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
                    self.enhancement_system.memory_system.memories['quiz_answers'][category] = {
                        'answer': answer,
                        'timestamp': datetime.now().isoformat()
                    }
                    self._save_system()
                    
                    # Generate response
                    response_text = self.enhancement_system.quiz.create_response(answer, category)
                    return Response(message=response_text, break_loop=False)
                    
            elif action == "check_milestones":
                # Check relationship milestones
                memories = self.enhancement_system.memory_system.memories
                
                # Calculate some fun stats
                total_memories = sum(len(v) if isinstance(v, list) else len(v) for v in memories.values())
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