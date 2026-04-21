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

from datetime import datetime

class TimeUtils:
    def __init__(self):
        pass

    @staticmethod
    def get_precision_time(ms_digits: int = 3) -> str:
        now = datetime.now()
        if 0 > ms_digits or ms_digits > 6:
            raise ValueError("ms_digits must be between 0 and 6")

        current_base_time = now.strftime('%Y-%m-%d %H:%M:%S')
        if ms_digits == 0:
            return current_base_time
        micro_seconds = str(now.microsecond).zfill(6)[:ms_digits]


        return f"{current_base_time}.{micro_seconds}"

    @staticmethod
    def get_date(structure: str = "YY/MM/DD") -> str:

        format_map = {
            "YY": "%Y",
            "MM": "%m",
            "DD": "%d"
        }

        structure_parts = structure.split("/")
        output_instruction = []

        for part in structure_parts:
            if part in format_map:
                output_instruction.append(format_map[part])
            else:
                raise ValueError(f"Invalid structure: {part}, you must use 'YY', 'DD', 'MM' or leave the parameter "
                                 f"'structure' in blank for default format")

        instruction = "-".join(output_instruction)

        return datetime.now().strftime(instruction)


if __name__ == "__main__":
    timeu = TimeUtils()
    for i in range(7):
        print(f"[{timeu.get_precision_time(ms_digits=i)}]")

    print(timeu.get_date(structure= "DD/MM/YY"))