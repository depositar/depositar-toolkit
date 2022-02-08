# 研究資料寄存所命令列工具 / Command Line Tools for depositar

## 事前準備

一連線設定檔，如 `invoke.yaml.example`，並命名為 `invoke.yaml`:

* owner_proj: 資料集所屬之專案
* api_url: CKAN 主機所在位址
* api_key: CKAN 使用者 API 金鑰

## 安裝

1. [安裝 depositar](https://docs.depositar.io/zh_TW/latest/maintaining/installing/install-from-source.html)
2. 進入 depositar 所安裝的 Python 虛擬環境：`$ . /usr/lib/ckan/default/bin/activate`
3. 安裝必須套件：`$ pip install -r requirements.txt`

## 操作方式

### 批次上傳工具 (load)

#### 準備檔案

* 後設資料 (資料集層級) CSV 檔案 (請將收到的 ods 檔案之「後設資料 (資料集層級)」工作表另存為 CSV)
* 後設資料 (資源層級) CSV 檔案 (請將收到的 ods 檔案之「後設資料 (資源層級)」工作表另存為 CSV)
* 欲上傳之實體檔案 (存於一資料夾)

#### 執行方式：

    $ inv load -d DATASETS -r RESOURCES -f FILES

* DATASETS: 後設資料 (資料集層級) CSV 檔案
* RESOURCES: 後設資料 (資源層級) CSV 檔案
* FILES: 實體檔案所在資料夾位置 (選用)

#### 執行範例：

    $ inv load -c /etc/ckan/default/development.ini -d dataset.csv -r resource.csv -f ./data

### 取得帳號與電子郵件清單 (usermail)

註：此功能僅列出帳號清單。去除重複與空值等工作，需另行處理。

#### 執行方式：

    $ inv usermail -c CONFIG -u USER

* CONFIG: CKAN config 檔案 (ini)
* USER: CKAN `系統管理員`帳號名稱 (選用；預設為 `default`)

#### 執行範例：

    $ inv usermail -c /etc/ckan/default/development.ini -u default
