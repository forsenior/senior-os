from screeninfo import get_monitors
# This class is used for detecting and calculating user monitor
class GetMonitorHeightAndWidth:
    def __init__(self):
        monitor = get_monitors()[0]
        self.screen_width, self.screen_height = monitor.width, monitor.height
        
    
    def get_height_screen(self):

        return self.screen_height
     
    def get_width_screen(self):
        return self.screen_width