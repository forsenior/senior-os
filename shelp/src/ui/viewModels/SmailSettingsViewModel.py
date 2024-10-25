from shelp.src.configuration.models.SmailConfiguration import SmailConfiguration


# TODO: Switch to proper implementation using QObject and model change events
class SmailViewModel:
    _smailConfiguration: SmailConfiguration

    def __init__(self, smailConfiguration: SmailConfiguration):
        super().__init__()
        self._smailConfiguration = smailConfiguration

    # TODO: Fix this issue where values are somehow saved straight into the DataClass model and are bypassing
    # data provider
    def update_model(self, attribute_name: str, value):
        print(f"Attribute is being updated {attribute_name}, value: {value}")
        self._smailConfiguration[attribute_name] = value
        print(f"Update complete new value is {self._smailConfiguration[attribute_name]}")
