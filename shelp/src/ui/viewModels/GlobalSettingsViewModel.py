from shelp.src.configuration.models.GlobalConfiguration import GlobalConfiguration


# TODO: Switch to proper implementation using QObject and model change events
class GlobalViewModel:
    _globalConfiguration: GlobalConfiguration

    def __init__(self, global_configuration: GlobalConfiguration):
        super().__init__()
        self._globalConfiguration = global_configuration

    # TODO: Fix this issue where values are somehow saved straight into the DataClass model and are bypassing
    # data provider
    def update_model(self, attribute_name: str, value):
        print(f"Attribute is being updated {attribute_name}, value: {value}")
        self._globalConfiguration[attribute_name] = value
        print(f"Update complete new value is {self._globalConfiguration[attribute_name]}")
