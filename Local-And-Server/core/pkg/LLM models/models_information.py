import json


json_name = "model_data"

class ModelInformation:
    def __init__(self):
        with open(json_name + ".json", "r") as f:
            self.models_info = json.load(f)

    def get_model_info(self, model_name):
        return self.models_info.get(model_name, None)