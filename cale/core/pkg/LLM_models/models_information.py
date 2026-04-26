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

# from ..Utils.Time.time_utils import TimeUtils
import sys
import time
import json


JSON_NAME = "model_data"
db_parameters = []

class ModelInformation:
    def __init__(self):
        try:
            with open(JSON_NAME + ".json", "r", encoding='utf-8') as f:
                self.models_info = json.load(f)
            self.example_template = self.models_info["db_example"]
            db_parameters.extend(self.example_template)



        except FileNotFoundError:
            raise FileNotFoundError(f"{JSON_NAME} was not found")


    def extract_models_info(self, parameters: dict = None) -> dict:
        if not parameters:
            raise ValueError("'Parameters' dictionary is required to extract models information. \n"
                             f"You can use {db_parameters}")

        extracted_info = {}
        for model_key, model_data in self.models_info.items():
            if model_key == parameters["technical_name"]:
                extracted_info[model_key] = model_data

        return extracted_info


    @staticmethod
    def get_float_input(prompt: str) -> float:
        while True:
            try:
                value = float(input(prompt))
                return value
            except ValueError:
                print("Invalid input. Please enter a float value.")


    @classmethod
    def model_template_data_checker(cls, template: dict, data: dict):
        if set(template.keys()) != set(data.keys()):
            return False

        for key in template:
            if isinstance(template[key], dict):
                if not isinstance(data[key], dict):
                    return False

                if not cls.model_template_data_checker(template[key], data[key]):
                    return False

        return True

    def add_model(self, assistant: bool = True, data: dict = None):
        technical_name = ""

        
        if not data and not assistant:
            raise ValueError("You must provide data to add a model if assistant is set to False")

        elif assistant and data:
            print("Warning! Using the assistant will erase the data you provided. Do you want to continue? (y/n): ")
            if input().lower() != "y":
                print("Model addition cancelled. Exiting...")
                return

        if assistant:
            while True:
                print("Welcome to the assistant to add new models to the database!")
                gen_info = {
                    'family': input("Please enter the model family: "),
                    'technical_name': input("Please model's technical name: ").lower(),
                    'front_name': input("Please enter the model's front name (the name that will be shown to the user): "),
                    'company': input("Please enter the model company (e.g., OpenAI, Google, Meta, etc.): "),
                    'environment': input("Please enter the model environment (Cloud or Local): ").lower(),
                    'freemium': input("Is the model freemium? (y/n): ").lower()
                }
                print("Now, you are going to enter the model's pricing according with the following data, if the model doesnt"
                      "hasn't got a pricing, just put '0'. All pricing is per million tokens, in U.S dollars.")
                time.sleep(0.5)
                print("Please enter the model's pricing for the following categories: ")
                pricing = {
                    'input_prompts_minus_200000_tokens': self.get_float_input("Input for prompts minus 200000 tokens: "),
                    'input_prompts_more_than_200000_tokens': self.get_float_input("Input for for prompts at least 200000 tokens long: "),
                    'output_prompts_minus_200000_tokens': self.get_float_input("Output for prompts minus 200000 tokens: "),
                    'output_prompts_more_than_200000_tokens': self.get_float_input("Output for prompts at least 200000 tokens long: ")
                }

                print('You complete the first step! Now, you have to confirm the information you entered')

                for key, value in gen_info.items():
                    print(f"Name: {key}, Value: {value}")

                print("Now, let's check the pricing information:")

                for key, value in pricing.items():
                    print(f"Name: {key}, Value: {value}")


                if (confirmation := input("Please confirm that the information is correct (y/n/exit): ").lower()) == "exit":
                    print("Model addition cancelled. Exiting...")
                    return
                elif confirmation != "y":
                    print("Model addition cancelled. Trying again...")
                    continue

                technical_name = gen_info.pop('technical_name').lower()

                if technical_name in self.models_info:
                    if (overwrite := input("CAUTION! You entered a model that already exists in the database. \n"
                                           "Would you like to overwrite the existing model information? (y/n/exit): ")) == "exit":
                        print("Model addition cancelled. Exiting...")
                        return
                    elif overwrite != "y":
                        print("Model addition cancelled. Re-trying...")
                        continue

        elif not self.model_template_data_checker(self.models_info["db_example"], data):
            raise ValueError("The provided data doesnt match our formats. Please revise")

        else:
            raise Exception("We don't know what happened. Please try again. The model wasn't added to the database")


        self.models_info[technical_name] = {**gen_info, "pricing": pricing}

        with open(JSON_NAME + ".json", "w", encoding='utf-8') as f:
            json.dump(self.models_info, f, indent=4)
        print("Model added successfully!")
        return



if __name__ == "__main__":
    if (requested_action := input("What do you wanna do? (1: Add a new model, 2: Get model information, 3: Exit) \n")) == "1":
        model_info = ModelInformation()
        model_info.add_model()
    elif requested_action == "2":
        model_info = ModelInformation()
        enter_parameters = {
            "technical_name": input("Please enter the model's technical name: ").lower()
        }
        info = model_info.extract_models_info(enter_parameters)
        print(info)
    elif requested_action == "3":
        print("Exiting...")
        time.sleep(0.25)
        sys.exit(0)

