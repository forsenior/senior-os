
# This method is used for changing language in browser
class Translator:
    # Create initial function
    def __init__(self, _dataProvider, global_dataProvider):
        # Default shortcut for language
        self.language_keys = ["cz","en","de"]
        
        self.current_language_in_browser = global_dataProvider.language
        self.text = _dataProvider.text

        # Set current language is CZ =0 , EN = 1, DE = 2
        if(self.current_language_in_browser) == "cz":
            self.current_language_index = 0
        elif self.current_language_in_browser == "en":
            self.current_language_index = 1
        else:
            self.current_language_index = 2

    # Toggle between each languages
    def toggle_supported_language(self):
        # Increase the index to change the language
        self.current_language_index += 1
        # If we reached the end of the list, go back
        if self.current_language_index >= len(self.language_keys):
            self.current_language_index = 0
        # Change current language after this function called
        self.current_language_in_browser = self.language_keys[self.current_language_index]

    # Get text from .json acroding Key value
    def get_translated_text(self, button_name):
        key_text = f"sweb_{self.current_language_in_browser}_{button_name}"
        #print("text",self.text[1])
        #return self._dataProvider.text
        
        if key_text == "sweb_en_menu1":
            return self.text[0]
        if key_text == "sweb_en_menu2":
            return self.text[1]
        if key_text == "sweb_en_menu2Address":
            return self.text[2]
        if key_text == "sweb_cz_menu1":
            return self.text[3]
        if key_text == "sweb_cz_menu2":
            return self.text[4]
        if key_text == "sweb_cz_menu2Address":
            return self.text[5]
        if key_text == "sweb_de_menu1":
            return self.text[6]
        if key_text == "sweb_de_menu2":
            return self.text[7]
        if key_text == "sweb_de_menu2Address":
            return self.text[8]

    # Get state of current language
    def get_current_language(self):
        return self.language_keys[self.current_language_index]
