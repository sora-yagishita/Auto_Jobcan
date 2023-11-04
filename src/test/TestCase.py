class TestCase:
    def __init__(self):
        self.__name = ''

    def name(self):
        return self.__name

    def name(self, name):
        self.__name = name