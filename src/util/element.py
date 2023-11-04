import json

class ElementConfig:

    @staticmethod
    def get_config_file():
        config_file_name = "./src/util/element.json"

        with open(config_file_name, encoding="utf-8") as file:
            config_file = json.load(file)
            return config_file

    @staticmethod
    def get_login_page_elements():
        return ElementConfig.get_config_file()["manager"]["login_page"]