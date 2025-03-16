from sconf.configuration.models.global_configuration import GlobalConfiguration
from sconf.configuration.models.smail_configuration import SmailConfiguration


# TODO: Switch to proper implementation using QObject and model change events
class SmailViewModel:
    _smailConfiguration: SmailConfiguration
    _globalConfiguration: GlobalConfiguration

    def __init__(self, smailConfiguration: SmailConfiguration,
                 globalConfiguration: GlobalConfiguration):
        super().__init__()
        self._smailConfiguration = smailConfiguration
        self._globalConfiguration = globalConfiguration

    def update_model(self, attribute_name: str, value):
        print(f"Attribute is being updated {attribute_name}, value: {value}")
        try:
            if attribute_name != "careGiverEmail":
                setattr(self._smailConfiguration, attribute_name, value)
                print(f"Update complete new value is {getattr(self._smailConfiguration, attribute_name, value)}")
                return
            else:
                setattr(self._globalConfiguration, attribute_name, value)
                print(f"Update complete new value is {getattr(self._globalConfiguration, attribute_name, value)}")

        except AttributeError:
            print(f"Error: attribute {attribute_name} does not exist in the current scope")
