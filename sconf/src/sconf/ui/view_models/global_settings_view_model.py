from sconf.configuration.models.global_configuration import GlobalConfiguration
from sconf.configuration.models.smail_configuration import SmailConfiguration
from sconf.configuration.models.sweb_configuration import SwebConfiguration


# TODO: Switch to proper implementation using QObject and model change events
class GlobalViewModel:

    def __init__(self, global_configuration: GlobalConfiguration,
                 sweb_configuration: SwebConfiguration,
                 smail_configuration: SmailConfiguration):
        super().__init__()
        self._global_configuration = global_configuration
        self._sweb_configuration = sweb_configuration
        self._smail_configuration = smail_configuration

    def update_model(self, attribute_name, value):
        print(f"Attribute is being updated {attribute_name}, value: {value}")
        try:
            if attribute_name == "protectionLevel":
                self.__set_protection_level(value)
            setattr(self._global_configuration, attribute_name, value)
            print(f"Update complete new value is {getattr(self._global_configuration, attribute_name, value)}")
        except AttributeError as ex:
            print(f"Error: Exception occurred when trying to set attribute {attribute_name} \n"
                  f"exception: {ex}")

    def __set_protection_level(self, protection_level: int):
        """
            True and False values set in this method are to be interpreted as Enable and Disable respectively
        """
        self._global_configuration.protectionLevel = protection_level

        match protection_level:
            case '1':
                self._smail_configuration.sendPhishingWarning = True
                self._sweb_configuration.sendPhishingWarning = True
            case '2':
                self._smail_configuration.sendPhishingWarning = True
                self._smail_configuration.receiveWhitelistedEmailsOnly = True
                self._smail_configuration.showUrlInEmail = False

                self._sweb_configuration.sendPhishingWarning = True
                self._sweb_configuration.seniorWebsitePosting = False
            case '3':
                self._smail_configuration.sendPhishingWarning = True
                self._smail_configuration.receiveWhitelistedEmailsOnly = True
                self._smail_configuration.sendWhitelistedEmailsOnly = True
                self._smail_configuration.showUrlInEmail = False

                self._sweb_configuration.sendPhishingWarning = True
                self._sweb_configuration.seniorWebsitePosting = False
                self._sweb_configuration.allowWebSearch = False
                self._sweb_configuration.whiteListedWebsitesOnly = True
            case _:
                raise AttributeError("Setting protection level was attempted but value of "
                                     "protection level didn't match any case")
