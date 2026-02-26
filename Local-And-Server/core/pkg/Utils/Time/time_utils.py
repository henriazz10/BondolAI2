from datetime import datetime


def get_precision_time(ms_digits: int = 3) -> str:
    now = datetime.now()
    if 0 >= ms_digits >= 6:
        raise ValueError("ms_digits must be between 0 and 6")

    current_base_time = now.strftime('%Y-%m-%d %H:%M:%S')
    micro_seconds = str(now.microsecond).zfill(6)[:ms_digits]

    if ms_digits == 0:
        return current_base_time

    return f"{current_base_time}.{micro_seconds}"

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

    for i in range(7):
        print(f"[{get_precision_time(ms_digits=i)}]")

    print(get_date(structure= "DD/MM/YY"))