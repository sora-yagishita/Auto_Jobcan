from selenium.webdriver.support.ui import WebDriverWait
from util.selenium_util import SeleniumUtil as su
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from util.Constants import Constants
from util.config import Config
import xml.etree.ElementTree as ET
import pandas as pd
import datetime
import shutil
import time
import re
import os

class TestCase:
    project_mapping = []
    target_csv_name = ""

    """
    初期化メソッド
    """
    def __init__(self):
        self._driver = su.get_driver()
        self._web_driver_wait = WebDriverWait(self._driver, Config.get_wait_timeout())
        self.set_project_mapping()
        self.get_csv_file_name()


    """
    XML取得メソッド
    """
    def set_project_mapping(self):
        xml_data = ET.parse(Constants.MAPPING_FILE_PATH).getroot()
        for target in xml_data.findall('./' + Constants.MAPPING_FILE_PROJECT):
            for jobcan_project in target:
                for data_project in jobcan_project:
                    data = {
                        Constants.MAPPING_FILE_JOBCAN_PROJECT: jobcan_project.attrib["name"],
                        Constants.MAPPING_FILE_DATA_PROJECT: data_project.attrib["name"]
                    }
                    self.project_mapping.append(data)

    """
    読み込み対象CSVファイル名取得処理
    inputディレクトリ内の最新のCSVファイルを取得
    """
    def get_csv_file_name(self):
        files = os.listdir(Constants.CSV_FILE_DIR_INPUT)
        paths = [os.path.join(Constants.CSV_FILE_DIR_INPUT, basename) for basename in files]
        self.target_csv_name = max(paths, key=os.path.getctime)

    """
    メインメソッド
    """
    def start_outo_jobcan(self):
        self.login_jobcan()
        self.input_work()
        self.move_csv_file_complete()

    """
    ログイン処理
    """
    def login_jobcan(self):
        self._driver.get(Constants.JOBCAN_LOGIN_URL)
        login_mail_text = self._driver.find_element_by_id("user_email")
        login_mail_text.send_keys(Constants.JOBCAN_LOGIN_ID)
        login_pass_text = self._driver.find_element_by_id("user_password")
        login_pass_text.send_keys(Constants.JOBCAN_LOGIN_PASS)
        self._driver.find_element_by_id("login_button").click()

    """
    工数入力処理
    """
    def input_work(self):
        self.transition_input_work()
        csv_data = self.get_csv_data()
        self.input_data_display_modal(csv_data)

    """
    工数入力画面遷移処理
    """
    def transition_input_work(self):
        self._driver.implicitly_wait(Constants.TIME_OUT)
        time.sleep(1) #Sleep入れないとスクリプトが実行されない
        self._driver.find_element_by_xpath('//a[contains(text(),"勤怠")]').click()
        self._driver.switch_to.window(self._driver.window_handles[1])
        self._driver.get(Constants.JOBCAN_INPUT_WORK_URL)

    """
    CSVデータからデータ取得処理
    """
    def get_csv_data(self):
        all_csv_data = pd.read_csv(self.target_csv_name, header=0, sep=',')
        format_csv_data = all_csv_data[[
            Constants.CSV_COLMN_NAME_STARTDATE,
            Constants.CSV_COLMN_NAME_PROJECT,
            Constants.CSV_COLMN_NAME_DURATION]].groupby([
                Constants.CSV_COLMN_NAME_STARTDATE,
                Constants.CSV_COLMN_NAME_PROJECT]).sum()
        csv_list = []
        for index, item in format_csv_data.itertuples():
            if Constants.JOBCAN_INPUT_TRTGET_DATE_OPTION:
                start_date = datetime.datetime.strptime(Constants.JOBCAN_INPUT_START_DATE, Constants.JOBCAN_XML_DATE_FORMAT)
                end_date = datetime.datetime.strptime(Constants.JOBCAN_INPUT_END_DATE, Constants.JOBCAN_XML_DATE_FORMAT)
                target_date = datetime.datetime.strptime(index[0], Constants.JOBCAN_XML_DATE_FORMAT)
                if (start_date > target_date) or (target_date > end_date):
                    continue

            dict = {
                Constants.CSV_COLMN_NAME_STARTDATE: index[0],
                Constants.CSV_COLMN_NAME_PROJECT: index[1],
                Constants.CSV_COLMN_NAME_DURATION: item
                }
            csv_list.append(dict)
        return csv_list

    """
    データ入力
    対象日時モーダル表示処理
    """
    def input_data_display_modal(self, csv_data):
        self._driver.implicitly_wait(Constants.TIME_OUT)
        before_target_date = ""
        for data in csv_data:
            start_date = data[Constants.CSV_COLMN_NAME_STARTDATE]
            if before_target_date != start_date:
                before_target_date = start_date
                self.transition_target_month(start_date)
                target_sec = self.get_target_unix_time(start_date)
                script_name = "openEditWindow(" + str(target_sec) + ");"
                self._driver.execute_script(script_name)
                if Constants.JOBCAN_INPUT_ORVER_WRITE_OPTION: self.remove_work_all()
                csv_data_date_list = [csv_data_date for csv_data_date in csv_data if csv_data_date[Constants.CSV_COLMN_NAME_STARTDATE] == start_date]
                self.input_data_input_work(csv_data_date_list)

    """
    対象月に画面遷移処理
    """
    def transition_target_month(self, target_date):
        date_time_now = datetime.datetime.now()
        now_year = date_time_now.year
        now_month = date_time_now.month
        exchanged_target_date = datetime.datetime.strptime(target_date, Constants.JOBCAN_XML_DATE_FORMAT)
        target_year = exchanged_target_date.year
        target_month = exchanged_target_date.month
        if now_year != target_year: self._driver.find_element_by_name('year').send_keys(str(target_year))
        if now_month != target_month: self._driver.find_element_by_name('month').send_keys(str(target_month))

    """
    対象日をUNIX時間に変換
    """
    def get_target_unix_time(self, target_date):
        date = datetime.datetime.strptime(target_date, Constants.JOBCAN_XML_DATE_FORMAT)
        unix_time = int(date.timestamp())
        return unix_time

    """
    入力済み項目削除処理
    """
    def remove_work_all(self):
        count = len(self._driver.find_elements_by_class_name('jbc-btn-danger'))
        for i in range(1, count):
            script_name = "removeRecord(" + str(i) + ");"
            self._driver.execute_script(script_name)

    """
    データ入力
    工数入力処理
    """
    def input_data_input_work(self, csv_data):
        data_index = -1
        duration_total = datetime.datetime.strptime('0:00', '%H:%M')
        for index, data in enumerate(csv_data):
            project = data[Constants.CSV_COLMN_NAME_PROJECT]
            jobcan_project_name = self.mapping_project_name(project)
            if len(jobcan_project_name):
                time.sleep(1) #Sleep入れないとスクリプトが実行されない
                self._driver.execute_script('addRecord();')
                data_index += 1
                duration = self.convert_duration(data[Constants.CSV_COLMN_NAME_DURATION])
                duration_changed = datetime.datetime.strptime(duration, '%H:%M')
                duration_total += datetime.timedelta(hours=duration_changed.hour, minutes=duration_changed.minute)
                self._driver.find_elements_by_name('projects[]')[data_index].send_keys(jobcan_project_name)
                self._driver.find_elements_by_name('tasks[]')[data_index].send_keys("対応")
                self._driver.find_elements_by_name('minutes[]')[data_index].send_keys(duration)
                self._driver.find_elements_by_name('minutes[]')[data_index].send_keys(Keys.TAB)
        if Constants.JOBCAN_DEVIATE_AJUST_OPTION: self.deviate_ajust(duration_total, data_index)
        self._driver.find_element_by_id("save").click()

    """
    取込データプロジェクト名とジョブカン上のプロジェクト名のマッピング
    """
    def mapping_project_name(self, data_project_name):
        project_name = ""
        for project_mapping in self.project_mapping:
            if (project_mapping[Constants.MAPPING_FILE_DATA_PROJECT] == data_project_name):
                project_name = project_mapping[Constants.MAPPING_FILE_JOBCAN_PROJECT]
        return project_name

    """
    時間フォーマット変更
    """
    def convert_duration(self, duration):
        td = datetime.timedelta(hours=duration)
        changed_duration = datetime.datetime.strptime(str(td), '%H:%M:%S').strftime('%H:%M')
        return changed_duration

    """
    誤差自動入力処理
    """
    def deviate_ajust(self, duration_total, data_index):
        actual_work_hour_text = self._driver.find_element_by_id("edit-menu-title").text
        pattern = re.compile('\d?\d:\d\d')
        actual_work_hour = datetime.datetime.strptime(pattern.findall(actual_work_hour_text)[0], '%H:%M') 
        if actual_work_hour <= duration_total: return
        
        deviate_work_hour_text = self._driver.find_element_by_id("un-match-time").text
        deviate_work_hour = datetime.datetime.strptime(pattern.findall(deviate_work_hour_text)[0], '%H:%M')
        if deviate_work_hour == 0: return
        
        self._driver.execute_script('addRecord();')
        self._driver.find_elements_by_name('projects[]')[data_index + 1].send_keys(Constants.JOBCAN_DEVIATE_AJUST_PROJECT_NAME)
        self._driver.find_elements_by_name('tasks[]')[data_index + 1].send_keys("対応")
        self._driver.find_elements_by_name('minutes[]')[data_index + 1].send_keys(deviate_work_hour.strftime('%H:%M'))
        self._driver.find_elements_by_name('minutes[]')[data_index + 1].send_keys(Keys.TAB)

    """
    対象csvファイルをcompleteディレクトリに移動
    """
    def move_csv_file_complete(self):
        shutil.move(self.target_csv_name, Constants.CSV_FILE_DIR_COMPLETE)
