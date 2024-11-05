import re

from typing import List

protection_level_pattern = re.compile(r'[0-9]')

protection_level_conversion = {
    1: "PL1",
    2: "PL2",
    3: "PL3"
}

full_language_name_conversion = {
    "German": "De",
    "English": "Dn",
    "Czech": "Cz"
}


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

    @staticmethod
    def protection_level_to_int(value: str) -> int:
        return protection_level_pattern.findall(value)[0]

    @staticmethod
    def int_to_protection_level(value: int) -> str:
        return protection_level_conversion[value]

    @staticmethod
    def language_to_country_code(value: str) -> str:
        return full_language_name_conversion[value]

    @staticmethod
    def country_code_to_language(value: str) -> str:

        for country_code, country in full_language_name_conversion.items():
            if value == country:
                return country_code

        return "key doesn't exist"
