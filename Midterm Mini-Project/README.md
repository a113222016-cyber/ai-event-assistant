# AI 活動報名訊息整理助手

一個使用 Streamlit + OpenAI API 的繁體中文小工具。使用者貼上活動公告後，系統以 Structured Outputs（JSON Schema）整理活動欄位、重要資訊、下一步行動及缺漏資訊。

## 專題目的

* **目標使用者：** 需要快速閱讀社團、校園或公開活動公告的學生與一般參與者。
* **解決問題：** 活動公告常散落在長篇文字中，日期、地點、截止時間及報名行動不易快速找到。
* **核心功能：** 將貼上的公告整理成固定欄位，並指出原文未提供、需要再確認的資訊。
* **資料原則：** 只依據原文整理；未提供的內容標示「未提及」，不自行推測。

## 功能與結構化欄位

|欄位|用途|
|-|-|
|event\_name|快速辨識活動名稱|
|event\_date|確認活動日期與時間|
|location|確認活動地點|
|registration\_deadline|掌握報名截止時間|
|target\_audience|判斷自己是否符合參加對象|
|key\_details|查看重要資訊|
|action\_items|知道下一步要做什麼|
|missing\_information|找出公告尚未說明的資訊|

本專題使用 OpenAI Responses API 的 `text.format` JSON Schema，設定 `strict: true`、所有欄位必填及 `additionalProperties: false`。程式另有基本型別檢查。

## 專案檔案

```text
Midterm Mini-Project/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── .env.example
├── .streamlit/
│   └── secrets.example.toml
├── 第08週\_課堂簡化版\_專題設計與驗收紀錄.md
└── sample\_data/
    └── sample\_announcement.txt
```

## 本機安裝與啟動

建議使用 Python 3.14，並依實際套件安裝結果確認環境相容性。

### Windows PowerShell

```powershell
cd "Midterm Mini-Project"
py -3.14 -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
```

編輯 `.env`，填入自己的 OpenAI API Key，然後啟動：

```powershell
streamlit run app.py
```

### macOS / Linux

```bash
cd "Midterm Mini-Project"
python3.14 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env
streamlit run app.py
```

編輯 `.env` 後再啟動。金鑰不可貼到公開程式碼、README 或截圖。

## 操作方式

1. 開啟 Streamlit App。
2. 貼上活動公告，最多 6,000 字元。
3. 勾選 API 同意開關。
4. 按「整理活動資訊」。
5. 檢查每個欄位是否能在原文找到依據。
6. 可下載 JSON 結果。

API 預設關閉。空白、未同意、缺少金鑰或超過字數限制時，不會呼叫 API。每次有效提交最多一次請求，`max\_retries=0`。

## Streamlit Community Cloud 部署（必做）

1. 將整個 `Midterm Mini-Project` 資料夾上傳到自己的 GitHub Repo 根目錄。
2. Commit / Push 後，在 GitHub 確認檔案路徑。
3. 到 [Streamlit Community Cloud](https://share.streamlit.io/) 建立 App。
4. 選擇自己的 Repo 與部署分支。
5. Main file path 填入：

   `Midterm Mini-Project/app.py`

6. 在 App 的 Settings → Secrets 設定：

```toml
   OPENAI\_API\_KEY = "你的 OpenAI API Key"
   ```

7. 確認 `requirements.txt` 可被平台安裝，等待 App 啟動。
8. 開啟雲端網址，先測試未勾選 API 時的提示，再啟用 API 完成真實測試。
9. 將 App 網址、部署分支、入口路徑、驗收日期及真實測試紀錄補入設計與驗收紀錄。

**目前已完成 GitHub 與 Streamlit Community Cloud 部署，並已在雲端完成真實 OpenAI API 測試。**



**GitHub Repo：https://github.com/a113222016-cyber/ai-event-assistant**



**Streamlit App：https://ai-event-assistant-ijxvcis6hgqgdmrue7vaqs.streamlit.app/**



**部署分支：main**



**Main file path：Midterm Mini-Project/app.py**



**雲端真實 API 測試紀錄**



**測試結果：成功**



**成功時間：2026-11-11 01:07:56（台灣時間）**



**模型：gpt-5.4-mini**



**本次提交最多 1 次 API 請求**



**測試活動：AI 人工智慧工作坊**



**輸入摘要：2026-12-15 13:30–16:30，世新大學管理學院，報名截止 2026-12-10，對象為全校學生，免費。**



**輸出摘要：成功整理活動名稱、日期時間、地點、報名截止、對象、重要資訊、下一步行動及待確認資訊。**

## 測試方式

* 空白輸入：應顯示提示，0 次 API 請求。
* 未勾選 API：應顯示提示，0 次 API 請求。
* 缺少金鑰：應在請求前停止。
* 正常公告：啟用 API 後整理一筆虛構活動資料，逐欄對照原文。
* 資訊不足公告：使用缺少日期或地點的資料，確認標示未提及或列入待確認。
* 新提交失敗：確認舊成功結果不會被誤當成新結果。

## 成本與限制

* 模型預設為 `gpt-5.4-mini`，可用 `OPENAI\_MODEL` 調整；實際可用性依 API 帳號權限確認。
* 文字長度上限 6,000 字元。
* 每次有效提交最多一次 API 請求，不自動重試。
* 模型輸出即使符合 Schema，也不代表事實一定正確，仍需人工核對。
* 本版本處理貼上的文字，不包含 PDF、Word、CSV 上傳。

## AI 協助與個人修改紀錄

本專題程式初稿由 AI 協助產生。提交前請自行閱讀程式、確認 API 帳號與模型可用性、完成本機及雲端測試，並在設計與驗收紀錄寫下你實際修改與驗證的內容。

## 參考資料

* [OpenAI Structured Outputs](https://developers.openai.com/api/docs/guides/structured-outputs)
* [Streamlit Forms](https://docs.streamlit.io/develop/concepts/architecture/forms)
* [Streamlit Community Cloud 部署](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy)
* [Streamlit App dependencies](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/app-dependencies)

