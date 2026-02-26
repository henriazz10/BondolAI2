import google.genai.errors
from google import genai
from ....Utils.Logs.log_manager import LogManager


logs = LogManager 
class GeminiResponse:
    def __init__(self, api_key):
        self.api_key = api_key
        try:
            self.client = genai.Client(api_key=self.api_key)
        except google.genai.errors.ClientError as e:
            if e["error"]["details"][0]["reason"] == "API_KEY_INVALID":
                with ("Make sure your API key is valid and active. Check aistudio.google.com to more information.")