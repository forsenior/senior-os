from shelp.src.configuration.models.SwebConfiguration import SwebConfiguration


# TODO: Switch to proper implementation using QObject and model change events
class SwebViewModel:
    _swebConfiguration: SwebConfiguration

    def __init__(self, swebConfiguration: SwebConfiguration):
        super().__init__()
        self._swebConfiguration = swebConfiguration

    # TODO: Fix this issue where values are somehow saved straight into the DataClass model and are bypassing
    # data provider
    def update_model(self, attribute_name: str, value):
        print(f"Attribute is being updated {attribute_name}, value: {value}")
        self._swebConfiguration[attribute_name] = value
        print(f"Update complete new value is {self._swebConfiguration[attribute_name]}")
