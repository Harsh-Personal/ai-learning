from deepeval.models import DeepEvalBaseLLM
from langchain_groq import ChatGroq


class GroqJudge(DeepEvalBaseLLM):
    """
    Custom DeepEval judge model backed by Groq.
    DeepEval uses an LLM-as-judge to score metrics like Faithfulness,
    AnswerRelevancy, etc. By default it uses OpenAI — this swaps it for Groq.
    """

    def __init__(self, model_name: str = "llama-3.3-70b-versatile"):
        self.model_name = model_name
        self._model = ChatGroq(model=model_name, temperature=0)

    def load_model(self):
        return self._model

    def generate(self, prompt: str, schema=None):
        model = self.load_model()
        if schema:
            structured = model.with_structured_output(schema)
            return structured.invoke(prompt), 0
        res = model.invoke(prompt)
        return res.content, 0

    async def a_generate(self, prompt: str, schema=None):
        model = self.load_model()
        if schema:
            structured = model.with_structured_output(schema)
            res = await structured.ainvoke(prompt)
            return res, 0
        res = await model.ainvoke(prompt)
        return res.content, 0

    def get_model_name(self):
        return f"Groq/{self.model_name}"
