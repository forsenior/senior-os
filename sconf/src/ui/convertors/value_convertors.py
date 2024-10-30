from typing import List


class StringValueConvertors:

    @staticmethod
    def string_to_bool(value: str) -> bool:
        if value == "Enable":
            return True

        return False

    @staticmethod
    def bool_to_string(value: bool) -> str:
        if value:
            return "Enable"

        return "Disable"

    @staticmethod
    def plain_text_to_list(value: str) -> List[str]:
        value = value.replace('\'', '')
        parsed_text = value.split(',')

        return parsed_text

    @staticmethod
    def list_to_plain_text(value: List[str]) -> str:
        deliminator = " ,"

        return deliminator.join(value)
