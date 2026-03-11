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