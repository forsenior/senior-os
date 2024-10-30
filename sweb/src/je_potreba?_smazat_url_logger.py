from datetime import datetime

# Log: seq no:timestamp: %facility-severity-MNEMONIC:description
class URLLogger:
    def __init__(self):
        # 7 security levels for logging
        self.severity_log_levels = ["EMERGENCY","ALERT","CRITICAL","ERROR","WARNING","NOTICE","INFORMATIONAL","DEBUGGING"]
        self.log_file_name = "logPhishing.txt"
        self._init_()

    # Method for creating and opening file .txt
    def _init_(self):
        try:
            # Read file with file name
            with open(self.log_file_name, 'r',encoding='utf-8') as open_file:
                open_file.readline()
        except FileNotFoundError:
            # If file does not exist, show use w to create new and write parameter
            with open(self.log_file_name, 'w') as open_file:
                open_file.write("Logging phishing URL from Browser\n")
                
    # Input the the block message
    def log_blocked_url(self, facility, level_of_severity, mnemonic, description):
        self.log_to_txt(facility, self.severity_log_levels[level_of_severity], mnemonic, description)

    # When the URL is blocked from log_blocked_url, save to file .txt
    def log_to_txt(self, facility, severity, mnemonic, description):
        # Set current time 
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # seq no:timestamp: %facility-severity-MNEMONIC:description
        log_entry = f"{current_time} : {facility}-{severity} -> {mnemonic} : {description}\n"
        # Write to exising file .txt
        with open(self.log_file_name, 'a', encoding='utf-8') as open_file:
            open_file.write(log_entry)