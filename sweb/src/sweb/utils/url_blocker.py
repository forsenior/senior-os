# Go through all domains in the phishing database
# If the domain is match, take a blocking
class URLBlocker:
    def __init__(self, paths_to_phishdatabase, permitted_website_list):
        self.blocked_urls_database = set()
        self.permitted_website_list = set()
        # Load file from file path
        # For filepath in paths_to_db:
        self.load_urls_from_phishing_database(paths_to_phishdatabase)
        self.load_urls_from_allowed_website(permitted_website_list)
        self.find_url_with_value(permitted_website_list)
        
        
    # Read all member in phishing database
    def load_urls_from_phishing_database(self,path):
        try:
            with open(path,"r") as openfile:
                # Real all member from the file until the file is None
                    if openfile is not None:
                        content  = openfile.read()
                        reading_url = content.strip().split('\n')
                        self.blocked_urls_database.update(reading_url)
        except FileNotFoundError:
            print("Phishing database not found, The application will continue to run without blocking any URLs")
            pass

    # Load all member in permitted website list               
    def load_urls_from_allowed_website(self, path):
        try:
            with open(path,"r") as openfile:
                # Real all member from the file until the file is None
                if openfile is not None:
                    content = openfile.read()
                    reading_url = content.strip().split('\n')
                    self.permitted_website_list.update(reading_url)
        except FileNotFoundError:
            print("Permitted website list not found, The application will continue to run without blocking any URLs")
            pass
    def find_url_with_value(self, search_value):
        
        for line in self.permitted_website_list:
            line = line.strip()
            if search_value in line:
                return line
        return None
    
      
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
    ## This function is used for loading permitted website from sconf
    def load_permitted_website_from_sconf(self, permitted_website_list):
        permitted_website_list = set()
        # Exit when error occurs and print notification to log
        try:
            path = permitted_website_list
            if not path:
                return ["seznam.cz"]
            
            with open(path, 'r') as open_file:
                content  = open_file.read()
                reading_website = content.strip().split('\n')
                permitted_website_list.update(reading_website)
            open_file.close
            return permitted_website_list
        except FileNotFoundError:
            return ["seznam.cz"]
        except Exception as e:
            return ["seznam.cz"]
