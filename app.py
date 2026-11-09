import json
import os
from datetime import datetime, timezone

import streamlit as st
from openai import OpenAI

APP_TITLE = "AI 活動報名訊息整理助手"
MODEL = os.getenv("OPENAI_MODEL", "gpt-5.4-mini")
MAX_INPUT_CHARS = 6000

SCHEMA = {
    "type": "object",
    "properties": {
        "event_name": {"type": "string", "description": "活動名稱；原文未提供時填「未提及」"},
        "event_date": {"type": "string", "description": "活動日期與時間；未提供時填「未提及」"},
        "location": {"type": "string", "description": "活動地點；未提供時填「未提及」"},
        "registration_deadline": {"type": "string", "description": "報名截止時間；未提供時填「未提及」"},
        "target_audience": {"type": "string", "description": "參加對象；未提供時填「未提及」"},
        "key_details": {"type": "array", "items": {"type": "string"}, "description": "原文提到的重要資訊"},
        "action_items": {"type": "array", "items": {"type": "string"}, "description": "讀者接下來需要採取的行動"},
        "missing_information": {"type": "array", "items": {"type": "string"}, "description": "舉辦或報名所需但原文未提供的資訊"}
    },
    "required": [
        "event_name", "event_date", "location", "registration_deadline",
        "target_audience", "key_details", "action_items", "missing_information"
    ],
    "additionalProperties": False
}

INSTRUCTIONS = """
你是活動資訊整理助手。只能根據使用者貼上的原文整理，不可自行補造日期、地點、
費用、網址、人名或其他事實。原文沒有提供的單一欄位請填「未提及」。
key_details 只列出原文確實出現的重要資訊；action_items 整理讀者可採取的下一步；
missing_information 列出對理解活動或完成報名有幫助、但原文沒有提供的資訊。
若原文不是活動資訊，仍須如實整理，並在 missing_information 說明無法判定的部分。
所有內容使用繁體中文，簡潔明確。
"""

def get_api_key():
    try:
        secret_key = st.secrets.get("OPENAI_API_KEY", "")
    except Exception:
        secret_key = ""
    return secret_key or os.getenv("OPENAI_API_KEY", "")

def validate_result(data):
    expected = set(SCHEMA["required"])
    if not isinstance(data, dict) or set(data.keys()) != expected:
        raise ValueError("模型回應欄位不符合預期。")
    for key in ["event_name", "event_date", "location", "registration_deadline", "target_audience"]:
        if not isinstance(data[key], str):
            raise ValueError(f"{key} 欄位格式錯誤。")
    for key in ["key_details", "action_items", "missing_information"]:
        if not isinstance(data[key], list) or not all(isinstance(x, str) for x in data[key]):
            raise ValueError(f"{key} 欄位格式錯誤。")
    return data

def analyze_text(source_text, api_key):
    client = OpenAI(api_key=api_key, timeout=60.0, max_retries=0)
    response = client.responses.create(
        model=MODEL,
        instructions=INSTRUCTIONS,
        input=source_text,
        text={
            "format": {
                "type": "json_schema",
                "name": "event_registration_summary",
                "strict": True,
                "schema": SCHEMA
            }
        }
    )
    if not getattr(response, "output_text", None):
        raise ValueError("模型沒有回傳可讀取的文字結果。")
    data = json.loads(response.output_text)
    return validate_result(data)

st.set_page_config(page_title=APP_TITLE, page_icon="📣", layout="centered")
st.title("📣 " + APP_TITLE)
st.caption("貼上活動公告，快速整理活動資訊、報名行動與待確認事項。")

st.info("本工具只整理你貼上的文字，不會自行補造缺漏資訊。請勿貼上個人敏感資料。")

with st.expander("使用方式", expanded=True):
    st.markdown(
        "1. 貼上活動公告或報名訊息。\n"
        "2. 檢查文字是否完整（最多 6,000 字元）。\n"
        "3. 明確開啟 API 開關，再按下整理。\n"
        "4. 逐欄核對結果；AI 整理內容仍需人工確認。"
    )

api_enabled = st.checkbox("我了解 API 可能產生費用，並同意本次提交呼叫 OpenAI API", value=False)
source_text = st.text_area(
    "活動公告原文",
    height=240,
    max_chars=MAX_INPUT_CHARS,
    placeholder="請貼上活動公告，例如：活動名稱、日期、地點、報名方式……"
)
st.caption(f"目前字數：{len(source_text)} / {MAX_INPUT_CHARS}")

if st.button("整理活動資訊", type="primary", use_container_width=True):
    st.session_state.pop("result", None)
    st.session_state.pop("source", None)
    st.session_state.pop("error", None)

    cleaned = source_text.strip()
    if not cleaned:
        st.session_state.error = "請先輸入活動公告，空白內容不會呼叫 API。"
    elif len(cleaned) > MAX_INPUT_CHARS:
        st.session_state.error = f"內容超過 {MAX_INPUT_CHARS} 字元，不會呼叫 API。"
    elif not api_enabled:
        st.session_state.error = "請先勾選 API 同意開關，再提交整理。"
    else:
        key = get_api_key()
        if not key:
            st.session_state.error = "找不到 OPENAI_API_KEY。請設定本機 .env 或 Streamlit Cloud Secrets。"
        else:
            try:
                with st.spinner("正在整理，請稍候……"):
                    result = analyze_text(cleaned, key)
                st.session_state.result = result
                st.session_state.source = cleaned
                st.session_state.success_time = datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")
            except json.JSONDecodeError:
                st.session_state.error = "模型回應不是有效 JSON，結果未保存。"
            except Exception as exc:
                st.session_state.error = f"處理失敗：{type(exc).__name__}。請檢查金鑰、模型權限或服務狀態；本次沒有可用結果。"

if st.session_state.get("error"):
    st.error(st.session_state.error)

if st.session_state.get("result"):
    data = st.session_state.result
    st.divider()
    st.subheader("整理結果")
    st.caption(f"成功時間：{st.session_state.get('success_time', '未記錄')}｜模型：{MODEL}｜本次提交最多 1 次 API 請求")

    scalar_fields = [
        ("活動名稱", "event_name"),
        ("活動日期與時間", "event_date"),
        ("活動地點", "location"),
        ("報名截止時間", "registration_deadline"),
        ("參加對象", "target_audience")
    ]
    for label, key in scalar_fields:
        st.markdown(f"**{label}**")
        st.write(data[key])

    for label, key in [
        ("重要資訊", "key_details"),
        ("接下來可以採取的行動", "action_items"),
        ("仍需確認的資訊", "missing_information")
    ]:
        st.markdown(f"**{label}**")
        if data[key]:
            for item in data[key]:
                st.markdown(f"- {item}")
        else:
            st.write("無")

    with st.expander("查看本次原文"):
        st.text(st.session_state.source)

    export_data = {
        "model": MODEL,
        "success_time": st.session_state.get("success_time"),
        "source": st.session_state.source,
        "result": data
    }
    st.download_button(
        "下載本次整理結果（JSON）",
        data=json.dumps(export_data, ensure_ascii=False, indent=2),
        file_name="event_summary.json",
        mime="application/json",
        use_container_width=True
    )

st.divider()
st.caption("課堂專題示範版｜請以原始公告及主辦單位公告為準。")
