import json

class Config:

    @staticmethod
    def get_config_file():
        config_file_name = "./src/util/config.json"

        with open(config_file_name, encoding="utf-8") as file:
            config_file = json.load(file)
            return config_file

    @staticmethod
    def get_wait_timeout():
        return Config.get_config_file()["settings"]["wait_timeout"]

    @staticmethod
    def get_jobcan_login_url():
        return Config.get_config_file()["settings"]["jobcan_login_url"]

    @staticmethod
    def get_jobcan_login_id():
        return Config.get_config_file()["settings"]["jobcan_login_id"]

    @staticmethod
    def get_jobcan_login_pass():
        return Config.get_config_file()["settings"]["jobcan_login_pass"]

    @staticmethod
    def get_jobcan_input_work_url():
        return Config.get_config_file()["settings"]["jobcan_input_work_url"]

    @staticmethod
    def get_jobcan_target_templete_name():
        return Config.get_config_file()["settings"]["jobcan_target_templete_name"]

    @staticmethod
    def get_jobcan_xml_date_formt():
        return Config.get_config_file()["settings"]["jobcan_xml_date_formt"]

    @staticmethod
    def get_jobcan_input_target_date_option():
        return Config.get_config_file()["settings"]["jobcan_input_target_date_option"]

    @staticmethod
    def get_jobcan_input_target_start_date():
        return Config.get_config_file()["settings"]["jobcan_input_target_start_date"]

    @staticmethod
    def get_jobcan_input_target_end_date():
        return Config.get_config_file()["settings"]["jobcan_input_target_end_date"]

    @staticmethod
    def get_jobcan_deviate_ajust_option():
        return Config.get_config_file()["settings"]["jobcan_deviate_ajust_option"]

    @staticmethod
    def get_jobcan_deviate_ajust_project_name():
        return Config.get_config_file()["settings"]["jobcan_deviate_ajust_project_name"]

    @staticmethod
    def get_jobcan_input_orver_write_option():
        return Config.get_config_file()["settings"]["jobcan_input_orver_write_option"]