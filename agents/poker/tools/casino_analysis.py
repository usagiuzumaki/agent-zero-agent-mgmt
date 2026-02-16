import json
from python.helpers.tool import Tool, Response

class CasinoAnalysis(Tool):
    """
    Evaluates poker hands and provides raw data for mythic interpretation.
    """
    async def execute(self, **kwargs):
        cards = kwargs.get("cards", [])
        scenario = kwargs.get("scenario", "")

        result = {
            "raw_rank": None,
            "hand_class": None,
            "percentage": None,
            "scenario": scenario
        }

        if len(cards) >= 5:
            try:
                from treys import Card, Evaluator
                evaluator = Evaluator()
                # treys expects 2 hole cards and 3-5 board cards
                hole = [Card.new(c) for c in cards[:2]]
                board = [Card.new(c) for c in cards[2:]]
                rank = evaluator.evaluate(board, hole)
                hand_class = evaluator.get_rank_class(rank)
                class_string = evaluator.class_to_string(hand_class)
                percentage = 1.0 - evaluator.get_five_card_rank_percentage(rank)

                result["raw_rank"] = int(rank)
                result["hand_class"] = class_string
                result["percentage"] = round(percentage * 100, 2)
            except Exception as e:
                result["error"] = str(e)

        # The Casino Logician persona will take this JSON and turn it into a Fate Report.
        return Response(message=json.dumps(result, indent=2), break_loop=False)
