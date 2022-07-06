class Settings():
    def __init__(self, options):
        self.options = options

    def checkOption(self, key):
        return self.options[key]

    def toggleOption(self, key):
        self.options[key] = not self.options[key]
        return self.options[key]