from util.config import Config

class Constants:
    TIME_OUT = Config.get_wait_timeout()

    CSV_FILE_DIR = "csv\\"
    CSV_FILE_DIR_INPUT = CSV_FILE_DIR + "input\\"
    CSV_FILE_DIR_WORK = CSV_FILE_DIR + "work\\"
    CSV_FILE_DIR_COMPLETE = CSV_FILE_DIR + "complete\\"
    CSV_FILE_DIR_ERROR = CSV_FILE_DIR + "error\\"

    CSV_COLMN_NAME_STARTDATE = "Start date"
    CSV_COLMN_NAME_PROJECT = "Project"
    CSV_COLMN_NAME_DURATION = "Duration"

    MAPPING_FILE_PATH = "src\\util\\projectMapping.xml"
    MAPPING_FILE_PROJECT = "project"
    MAPPING_FILE_JOBCAN_PROJECT = "jobcanProject"
    MAPPING_FILE_DATA_PROJECT = "dataProject"
    MAPPING_FILE_EXCLUSION_PROJECT = "exclusionProject"

    JOBCAN_LOGIN_URL = Config.get_jobcan_login_url()
    JOBCAN_LOGIN_ID = Config.get_jobcan_login_id()
    JOBCAN_LOGIN_PASS = Config.get_jobcan_login_pass()
    JOBCAN_INPUT_WORK_URL = Config.get_jobcan_input_work_url()
    JOBCAN_TAGHET_TEMPLATE_NAME = Config.get_jobcan_target_templete_name()
    JOBCAN_XML_DATE_FORMAT = Config.get_jobcan_xml_date_formt()
    JOBCAN_INPUT_TRTGET_DATE_OPTION = Config.get_jobcan_input_target_date_option()
    JOBCAN_INPUT_START_DATE = Config.get_jobcan_input_target_start_date()
    JOBCAN_INPUT_END_DATE = Config.get_jobcan_input_target_end_date()
    JOBCAN_DEVIATE_AJUST_OPTION = Config.get_jobcan_deviate_ajust_option()
    JOBCAN_DEVIATE_AJUST_PROJECT_NAME = Config.get_jobcan_deviate_ajust_project_name()
    JOBCAN_INPUT_ORVER_WRITE_OPTION = Config.get_jobcan_input_orver_write_option()