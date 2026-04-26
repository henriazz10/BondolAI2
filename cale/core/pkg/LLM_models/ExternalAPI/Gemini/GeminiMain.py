# Developed by Bondol Team
# Coding in utf-8

# Copyright 2026 Henri.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

from google.genai.types import Tool, GenerateContentConfig, GoogleSearch # I am going to use it later
from cale.core.pkg.Utils.Logs import log_manager
from google.genai import types # I am also going to use it later
import google.genai.errors
from google import genai


DENIED_API_CHARACTERS = [" ", "\n", "\t", "\r", "\v", "\f", "\"", "'", "\\", "/", ":", "*", "?", "<", ">", "|",
                         "@", "#", "$", "%", "^", "&", "+", "=", "`", "~", "(", ")", "[", "]", "{", "}"]


log_manager = log_manager.LogManager()
class GeminiResponse:
    def __init__(self, api_key):
        if not api_key:
            with log_manager as log:
                log.write("No API key provided! Please check aistudio.google.com for more information", time=True,
                          microseconds=False, log_label="ERROR")
            raise ValueError("API key is required.")

        if set(DENIED_API_CHARACTERS) & set(api_key):
            with log_manager as log:
                log.write("Your API key contains invalid characters! Please check aistudio.google.com for"
                          " more information", time=True, microseconds=False, log_label="ERROR")
            raise ValueError("API key is not valid.")

        self.api_key = str(api_key)
        try:
            with log_manager as log:
                log.write(f"Opening session with Gemini API '{api_key[:5]}...{api_key[-2:]}' ", time=True,
                          microseconds=False, log_label="INFO")
                self.client = genai.Client(api_key=self.api_key)
                log.write("Session opened successfully", time=True,
                          microseconds=False, log_label="INFO")



        except google.genai.errors.ClientError as e:
            if "API_KEY_INVALID" in str(e):
                with log_manager as log:
                    log.write("Your API key is invalid! Please check aistudio.google.com for more information",
                              time=True, microseconds=False, log_label="ERROR")
            else:
                with log_manager as log:
                    log.write(f"An error occurred: {str(e)}", time=True,
                              microseconds=False, log_label="ERROR")



    def response(self, message):

        response = self.client.models.generate_content_stream(
            model="gemini-3-flash-preview",
            contents=[message]
        )
        for chunk in response:
            yield chunk



if __name__ == "__main__":

    ai = GeminiResponse(api_key= os.getenv('GEMINI_API_KEY'))
    for i in ai.response("Hello, how are you? Could you explain me how AI works?"):
        print(i.text)

