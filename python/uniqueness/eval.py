import sys
import os
import asyncio
from typing import List, Dict, Any

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from python.uniqueness.engine import AriaUniquenessEngine
from python.uniqueness.score import UniquenessScorer

class MockAgent:
    def __init__(self):
        self.config = type('Config', (), {'additional': {'UNIQUENESS_ENGINE': True}})

async def run_eval():
    print("RUNNING ARIA UNIQUENESS EVALUATION...")
    engine = AriaUniquenessEngine()
    scorer = UniquenessScorer(engine.config)
    agent = MockAgent()

    test_cases = [
        {
            "prompt": "I'm feeling really overwhelmed with all these tasks.",
            "raw": "I understand you are overwhelmed. Here is a plan to help. First, prioritize your tasks. Second, do them one by one. As an AI language model, I am here to assist."
        },
        {
            "prompt": "How do I fix a SyntaxError in Python?",
            "raw": "A SyntaxError means your code has a typo. Check your brackets. Certainly, I can help with that."
        },
        {
            "prompt": "Help me name my new project about neural networks.",
            "raw": "You could name it NeuralNetProject. Feel free to ask for more ideas."
        }
    ]

    print(f"\n{'Prompt':<50} | {'Score':<5} | {'Active Traits'}")
    print("-" * 120)

    for case in test_cases:
        prompt = case["prompt"]
        raw_response = case["raw"]

        # Process via engine
        processed_response = await engine.process_response(agent, prompt, raw_response)

        # We simulate the engine state for the scorer v1
        engine_state = {
            "active_traits": [t.__class__.__name__ for t in engine.traits],
            "ritual_applied": any("step" in processed_response.lower() or "plan" in processed_response.lower() for _ in [1])
        }

        score = scorer.calculate_score(processed_response, {"user_input": prompt}, engine_state)

        print(f"{prompt[:48]:<50} | {score:<5} | {engine_state['active_traits']}")
        print(f"  BEFORE: {raw_response}")
        print(f"  AFTER : {processed_response}")
        print("-" * 120)

if __name__ == "__main__":
    asyncio.run(run_eval())
