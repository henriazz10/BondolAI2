import os

from google.genai.types import Tool, GenerateContentConfig, GoogleSearch # I am going to use it later
from ....Utils.Logs.log_manager import LogManager
from google.genai import types # I am also going to use it later
import google.genai.errors
from google import genai



denied_api_characters = [" ", "\n", "\t", "\r", "\v", "\f", "\"", "'", "\\", "/", ":", "*", "?", "<", ">", "|",
                         "@", "#", "$", "%", "^", "&", "+", "=", "`", "~", "(", ")", "[", "]", "{", "}"]

logger = LogManager()
class GeminiResponse:
    def __init__(self, api_key):
        if not api_key:
            with logger as log:
                log.write("No API key provided! Please check aistudio.google.com for more information", time=True,
                          microseconds=False, log_label="ERROR")
            raise ValueError("API key is required.")

        for i in denied_api_characters:
            if i in str(api_key):
                with logger as log:
                    log.write("Your API key contains invalid characters! Please check aistudio.google.com for"
                              " more information", time=True, microseconds=False, log_label="ERROR")
                raise ValueError("API key is not valid.")
        self.api_key = str(api_key)
        try:
            with logger as log:
                log.write(f"Opening session with Gemini API '{api_key[:5]}...{api_key[-2:]}' ", time=True,
                          microseconds=False, log_label="INFO")
                self.client = genai.Client(api_key=self.api_key)
                log.write("Session opened successfully", time=True,
                          microseconds=False, log_label="INFO")



        except google.genai.errors.ClientError as e:
            if "API_KEY_INVALID" in str(e):
                with logger as log:
                    log.write("Your API key is invalid! Please check aistudio.google.com for more information",
                              time=True, microseconds=False, log_label="ERROR")
            else:
                with logger as log:
                    log.write(f"An error occurred: {str(e)}", time=True,
                              microseconds=False, log_label="ERROR")



    def response(self, message):
        pass



if __name__ == "__main__":
    ai = GeminiResponse(api_key= os.getenv('GEMINI_API_KEY'))

    ai.response("Hello, how are you?")