# VGH 自動初診掛號系統

這是一個使用 Python 和 Selenium 開發的台北榮總自動初診掛號表單提交系統。

## 功能特色

- 🤖 自動搜尋可用的掛號時段
- 📝 自動填寫個人資料表單
- ⚙️ 透過 .env 文件配置個人資料
- 🔒 支援個資保護選項設定
- 🏥 專門針對台北榮總掛號系統設計

## 安裝與使用

### 1. 環境要求

- Python 3.11+
- uv (Python 套件管理工具)

### 2. 安裝依賴

```bash
uv sync
```

### 3. 配置個人資料

編輯 `.env` 文件，填入您的個人資料：

```env
REGISTRATION_URL=

# 個人資料設定
ID_NUMBER=您的身分證號
NAME=您的姓名
BIRTH_DATE=2001/4/1
PHONE=您的手機號碼
ADDRESS=您的戶籍地址
EMERGENCY_CONTACT_NAME=緊急聯絡人姓名
EMERGENCY_CONTACT_PHONE=緊急聯絡人電話

# 健康習慣設定 (yes/no)
PASSIVE_SMOKING=no
SMOKING_HABIT=no
DRINKING_HABIT=no
BETEL_NUT_HABIT=no

# 個資同意設定 (yes/no)
AGREE_DATA_COLLECTION=no
AGREE_SATISFACTION_SURVEY=no
```

### 4. 執行程式

```bash
uv run main.py
```

或者直接執行：

```bash
python main.py
```

## 工作流程

1. 系統會自動開啟瀏覽器並前往指定的掛號頁面
2. 搜尋頁面中的可用時段 radio button (`name=regKey`)
3. 自動點選第一個可用的時段
4. 填寫表單中的個人資料
5. 設定健康習慣和個資同意選項
6. 詢問使用者是否要提交表單
7. 完成掛號流程

## 安全注意事項

- 請勿將包含個人資料的 `.env` 文件上傳到公開的程式碼庫
- 建議在測試完成後立即清除瀏覽器資料
- 系統僅用於合法的掛號用途

## 故障排除

- 如果找不到 radio button，請檢查網頁結構是否有變化
- 如果表單填寫失敗，請檢查 `.env` 文件中的資料格式
- 如果瀏覽器無法啟動，請確保已安裝 Chrome 瀏覽器

## 系統架構

本系統採用 uv 單檔架構設計：
- `main.py` - 主要程式邏輯
- `.env` - 個人資料配置
- `pyproject.toml` - uv 套件管理配置