from configuration.models.global_configuration import GlobalConfiguration


# TODO: Switch to proper implementation using QObject and model change events
class GlobalViewModel:
    _globalConfiguration: GlobalConfiguration

    def __init__(self, global_configuration: GlobalConfiguration):
        super().__init__()
        self._globalConfiguration = global_configuration

    def update_model(self, attribute_name, value):
        print(f"Attribute is being updated {attribute_name}, value: {value}")
        try:
            setattr(self._globalConfiguration, attribute_name, value)
            print(f"Update complete new value is {getattr(self._globalConfiguration, attribute_name, value)}")
        except AttributeError:
            print(f"Error: attribute {attribute_name} does not exist in the current scope")
