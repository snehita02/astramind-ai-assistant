# from typing import Dict


# class BaseEvaluator:
#     """
#     Abstract evaluator interface.
#     Any evaluation framework (LLM, RAGAS, custom)
#     must implement this interface.
#     """

#     def evaluate(
#         self,
#         question: str,
#         context: str,
#         answer: str
#     ) -> Dict:
#         raise NotImplementedError("Evaluator must implement evaluate()")



from typing import Dict


class BaseEvaluator:
    """
    Abstract evaluator interface.
    Any evaluation framework (LLM, RAGAS, custom)
    must implement this interface.
    """

    def evaluate(
        self,
        question: str,
        context: str,
        answer: str
    ) -> Dict:
        raise NotImplementedError("Evaluator must implement evaluate()")


class SimpleEvaluator(BaseEvaluator):
    """
    Lightweight evaluator used by AstraMind.
    """

    def evaluate(
        self,
        question: str,
        context: str,
        answer: str
    ) -> Dict:

        normalized = answer.lower()

        # ------------------------------
        # Knowledge Boundary Safeguard
        # ------------------------------

        if (
            "i don't know" in normalized
            or "cannot determine" in normalized
            or "not enough information" in normalized
        ):
            return {
                "confidence": 0.2,
                "grounded": False,
                "evaluation": "Knowledge boundary triggered"
            }

        # ------------------------------
        # Simple Context Support Check
        # ------------------------------

        if context and len(context) > 50:
            return {
                "confidence": 0.9,
                "grounded": True,
                "evaluation": "The context strongly supports the answer."
            }

        return {
            "confidence": 0.5,
            "grounded": False,
            "evaluation": "Weak contextual grounding."
        }