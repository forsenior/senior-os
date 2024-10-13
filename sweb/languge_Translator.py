from loadConfig import *

# This method is used for changing language in browser
class Translator:
    # Create initial function
    def __init__(self):
        self.language_config_database = load_sweb_config_json()
        # Default shortcut for language
        self.language_keys = ["cz","en","de"]
        self.current_language_in_browser = self.language_config_database["language"]["default_language"]
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
        return self.language_config_database["text"].get(key_text, f"No translation found for {key_text}")
    
    # Get audio from .json acroding Key value
    def get_translated_audio(self, button_name):
        key_audio = f"sweb_{self.current_language_in_browser}_{button_name}"
        return self.language_config_database["audio"].get(key_audio, f"No translation found for {key_audio}")

    # Get state of current language
    def get_current_language(self):
        return self.language_keys[self.current_language_index]