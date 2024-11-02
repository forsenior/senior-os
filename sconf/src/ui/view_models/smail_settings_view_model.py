from configuration.models.smail_configuration import SmailConfiguration


# TODO: Switch to proper implementation using QObject and model change events
class SmailViewModel:
    _smailConfiguration: SmailConfiguration

    def __init__(self, smailConfiguration: SmailConfiguration):
        super().__init__()
        self._smailConfiguration = smailConfiguration

    def update_model(self, attribute_name: str, value):
        print(f"Attribute is being updated {attribute_name}, value: {value}")
        try:
            setattr(self._smailConfiguration, attribute_name, value)
            print(f"Update complete new value is {getattr(self._smailConfiguration, attribute_name, value)}")
        except AttributeError:
            print(f"Error: attribute {attribute_name} does not exist in the current scope")
