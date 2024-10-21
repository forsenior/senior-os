from PyQt5.QtCore import QObject


class SettingsViewModel(QObject):
    def __init__(self, model):
        super().__init__()
        self.model = model
        self.model.dataChanged.connect(self.on_model_changed)

    def update_model(self, setting, value):
        self.model.update_setting(setting, value)

    def on_model_changed(self):
        # This method would be used to reflect changes from the model to the view
        print(f"Model updated: {self.model.__dict__}")