
# ジョブカン工数自動入力ツール
CSVデータの情報をジョブカンの工数管理へ自動で入力を行います。

## インストール
 ・` ` ` 
pip install selenium
 ` ` ` 

## 使用ライブラリ
* Python 3.10.1
* selenium 4.1.0

## 使い方
### csvファイルの準備
1. `Outo_Jobcan\csv\tmp.csv` を `Outo_Jobcan\csv\input\`配下へコピーします
2. `Project`にプロジェクト名
`Start date`に対応日
`Duration`に対応時間を記載します
##### 注意点
* 対応時間は時間単位で記載してください。  
`0:30 → 0.5`  
`1:15 → 1.25`  
* このシステムは[Toggle](https://track.toggl.com)からCSVファイルをインポートされたCSVデータを使用する想定で作成してます。
下記の手順で簡単にCSVファイルを作成する事が可能です。
一旦テキトウに記載。「Toggle → Reports → Detailed → 表示範囲を指定 → Export → Download CSV」

### 実行準備
1. `Outo_Jobcan\src\util\config.json`の設定値を変更します  
`jobcan_login_id`にジョブカンのログインIDを入力してください  
`jobcan_login_pass`にジョブカンのログインパスワードを入力してください  
設定値の詳細に関しては、[こちら](#設定値の詳細説明)を参照
2. `Outo_Jobcan\src\driver\`配下にChromeDriverを配置してください  
ChromeDriverの取得方法は[こちら](https://zenn.dev/ryo427/articles/7ff77a86a2d86a)を参照
3. `Outo_Jobcan\src\util\projectMapping.xml`の変更を行います  
`jobcanProject`にジョブカン上のプロジェクト名を入力してください  
`dataProject`にCSVファイル上のプロジェクト名を入力してください  
紐づけを行いたい`jobcanProject`の子要素に`dataProject`を配置してください。

### 実行
1. `main.py`をPythonで実行します
2. Chromeがシークレットモードで開き、工数の自動入力が実施されます
3. 入力が完了した場合、`Outo_Jobcan\csv\input\`配下のCSVファイルが`Outo_Jobcan\csv\complete\`配下へ遷移されます

## 設定値の詳細説明
|  設定値論理名  |  設定値物理名  |  説明  |  デフォルト値  |
| ---- | ---- | ---- | ---- |
|  wait_timeout  |  タイムアウト時間  |  画面の読み込みが完了するまでの最大待機時間を指定出来ます  |  60000  |
|  jobcan_login_url  |  ジョブカンログイン画面URL  |  ジョブカンログイン画面のURLを設定してください  |  https://id.jobcan.jp/users/sign_in?app_key=wf  |
|  jobcan_login_id  |  ジョブカンログインID  |  ジョブカンにログインするためのIDを設定してください  |  xxx@xxx.co.jp  |
|  jobcan_login_pass  |  ジョブカンログインPASS  |  ジョブカンにログインするためのPASSを設定してください  |  password  |
|  jobcan_input_work_url  |  ジョブカン工数管理画面URL  |  ジョブカン工数自動入力画面のURLを指定してください  |  https://ssl.jobcan.jp/employee/man-hour-manage  |
|  jobcan_xml_date_formt  |  取込CSVファイルの日付形式  |  取込を行うCSVファイルの日付形式を指定してください  |  %Y-%m-%d  |
|  jobcan_input_target_date_option  |  日付指定オプション  |  自動入力の対象日を指定する事が可能になります<br>`jobcan_input_target_start_date`に入力開始日を設定<br>`jobcan_input_target_end_date`に入力終了日を設定してください  |  false  |
|  jobcan_input_target_start_date  |  入力開始日  |  `jobcan_input_target_date_option`が`TRUE`の時に参照されます<br>自動入力を行う開始日を設定してください  |  2023-01-01  |
|  jobcan_input_target_end_date  |  入力終了日  |  `jobcan_input_target_date_option`が`TRUE`の時に参照されます<br>自動入力を行う終了日を設定してください  |  2023-12-31  |
|  jobcan_deviate_ajust_option  |  残工数自動入力オプション  |  CSVデータの工数とジョブカン上の工数に差分がある場合<br>`jobcan_deviate_ajust_project_name`に設定したプロジェクト名で差分の工数を入力します  |  true  |
|  jobcan_deviate_ajust_project_name  |  残工数自動入力プロジェクト名  |  `jobcan_deviate_ajust_option`が`TRUE`の時に参照されます<br>工数の差分を入力するプロジェクト名を設定してください  |  【その他】  |
|  jobcan_input_orver_write_option  |  上書き入力オプション  |  ジョブカン上に既に工数の入力があった場合、全て削除をしてから自動入力を開始します  |  true  |

## 開発者
Sora Yagishita <sora.yagishita@gmail.com>