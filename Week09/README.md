# 第 9 週：文件處理與資料前處理

## 一、專題介紹

本專題使用 Python 和 Streamlit 建立文件處理工具，支援 TXT、MD、CSV、文字型 PDF 與 DOCX。提供文字清理、文件切塊、來源位置回查，以及 JSON、TXT 下載功能。

本次測試文件為自行製作的「校園創意市集活動說明」，內容為虛構活動資訊，不包含個人敏感資料。

## 二、環境版本

- Python：3.13.5
- Streamlit：1.67.0
- pypdf：7.0.1
- python-docx：1.2.0

## 三、啟動方式

安裝套件：

```powershell
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

啟動 App：

```powershell
.venv\Scripts\python.exe -m streamlit run student/app.py
```

## 四、A/B 切塊比較

使用同一份文件，清理後字元數皆為 524。

| 項目 | A 組 | B 組 |
|---|---:|---:|
| chunk_size | 120 | 120 |
| overlap | 0 | 20 |
| 字元數 | 524 | 524 |
| 片段數 | 5 | 6 |

B 組 Chunk 0 與 Chunk 1 的重疊文字：

「校內師生免費入場。主辦單位預計安排18個」

- Chunk 0：start=0、end=120
- Chunk 1：start=100、end=220
- 重疊長度：20 個字元

## 五、人工來源核對

核對問題：活動預計在哪一天舉行？

答案：2026 年 12 月 12 日（星期六）上午 9 時至下午 4 時。

原文依據：

「預計於2026年12月12日（星期六）上午9時至下午4時，在世新校園創意廣場舉行。」

A、B 兩組均以 chunk_id=0、start=0、end=120 進行來源核對，`cleaned_text[start:end]` 與片段原文一致。

其他核對資訊：

- 報名截止：2026 年 11 月 25 日晚上 8 時
- 每組最多：4 人
- 總名額：72 人

## 六、錯誤邊界測試

- 測試設定：chunk_size=120、overlap=120。
- 預期結果：系統拒絕切分。
- 實際結果：顯示「overlap 必須小於 chunk_size，否則切塊無法向前推進。」
- 修正方式：將 overlap 改為 20。
- 重新測試：成功產生 6 個片段。

## 七、輸出與功能限制

已完成 A、B 兩組 JSON 切塊結果，以及提供第 10 週使用的 `cleaned_text.txt`。

本工具僅提供文件讀取、清理、切塊與人工來源回查，不包含向量搜尋、Embedding、OpenAI API 或 AI 摘要功能。掃描型 PDF 的 OCR 未實作，相關功能未測試。
