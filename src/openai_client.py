"""
Module to interact with openai API.
"""
import openai
from dotenv import load_dotenv
import os

load_dotenv()

class OpenAIClient:
    def __init__(self, temperature=0.2):
        self.api_key = os.getenv("OPENAI_APIKEY")
        self.model_name = "gpt-3.5-turbo"
        self.temperature = temperature
        openai.api_key = self.api_key


    def enrich_recommendation(self,input_recommendation) -> str:
        response = openai.ChatCompletion.create(
            model=self.model_name,
            messages=[{"role": "user", "content": self._generate_prompt(input_recommendation)}],
            temperature=self.temperature,
        )

        return response["choices"][0]["message"]["content"]

    def _generate_prompt(self,recommendation):
        return f"""Given the following input:{recommendation} Recommend 3 similar songs such as the input song, and provide short descriptions for all
            the recommended songs and why they would be similar, including the onese in the recommendation input.
        """
