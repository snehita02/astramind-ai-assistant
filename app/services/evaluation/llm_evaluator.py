import json
from typing import Dict

from app.core.llm_provider import generate_response
from app.services.evaluation.evaluator import BaseEvaluator


class LLMEvaluator(BaseEvaluator):

    def evaluate(
        self,
        question: str,
        context: str,
        answer: str
    ) -> Dict:

        evaluation_prompt = f"""
You are an evaluation system for a Retrieval-Augmented Generation (RAG) model.

Evaluate the following response.

Question:
{question}

Retrieved Context:
{context}

Answer:
{answer}

Provide evaluation in JSON format ONLY:

{{
  "faithfulness_score": <0 to 1>,
  "context_relevance_score": <0 to 1>,
  "answer_quality_score": <0 to 1>,
  "explanation": "<brief explanation>"
}}

Scoring Guidelines:
- Faithfulness: Is answer grounded in retrieved context?
- Context Relevance: Was retrieved context useful?
- Answer Quality: Is answer clear and complete?
"""

        response = generate_response(evaluation_prompt)

        try:
            parsed = json.loads(response)
            return parsed
        except Exception:
            return {
                "faithfulness_score": 0,
                "context_relevance_score": 0,
                "answer_quality_score": 0,
                "explanation": "Evaluation parsing failed"
            }