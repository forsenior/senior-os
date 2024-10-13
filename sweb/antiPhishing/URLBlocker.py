# Go through all domains in the phishing database
# If the domain is match, take a blocking
class URLBlocker:
    def __init__(self, paths_to_db):
        self.blocked_urls_database = set()
        # Load file from file path
        # For filepath in paths_to_db:
        self.load_urls_from_phishing_database(paths_to_db)
        
    # Read all member in phishing database
    def load_urls_from_phishing_database(self,path):
        with open(path,"r") as openfile:
             # Real all member from the file until the file is None
                if openfile is not None:
                    content  = openfile.read()
                    reading_url = content.strip().split('\n')
                    self.blocked_urls_database.update(reading_url)

    # Control that if the url is Block
    def is_url_blocked(self, input_url):
        if "login.microsoft" in input_url:
            return False
        elif "microsoft365.com" in input_url:
            return False
        else:
            for blocked_url in self.blocked_urls_database:
                if blocked_url in input_url:
                    return True
            return False