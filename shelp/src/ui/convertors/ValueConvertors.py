

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
