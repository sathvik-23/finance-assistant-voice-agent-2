import streamlit as st
import requests
from datetime import datetime

st.set_page_config(page_title="Finance Assistant", page_icon="📈", layout="centered")
st.title("📊 Multi-Agent Finance Assistant")

user_query = st.text_input("Your Question", placeholder="e.g. What’s our risk exposure in Asia tech stocks today?")
submit_button = st.button("Submit")

API_URL = "http://localhost:8001/v1/run"

if submit_button and user_query.strip():
    with st.spinner("Agents are analyzing your query..."):
        try:
            response = requests.post(
                API_URL,
                data={
                    "message": user_query,
                    "stream": "false",
                    "session_id": f"streamlit-session-{datetime.now().isoformat()}"
                }
            )
            if response.status_code != 200:
                st.error(f"❌ API Error: {response.status_code}\n{response.text}")
            else:
                data = response.json()

                # 🎯 Final summary (main content)
                st.markdown("### 🧠 Final Summary")
                st.markdown(data.get("content", "*No summary returned.*"))

                # 📦 Tool Calls
                tool_calls = data.get("tool_calls", [])
                if tool_calls:
                    st.markdown("### 🛠️ Tool Calls Executed")
                    for i, call in enumerate(tool_calls):
                        st.code(f"{i+1}. {call.get('raw', str(call))}", language="python")

                # 👨‍👩‍👧 Agent Responses
                member_responses = data.get("member_responses", [])
                if member_responses:
                    st.markdown("### 👥 Agent Responses")
                    for resp in member_responses:
                        name = resp.get("agent", {}).get("name", "Unnamed Agent")
                        content = resp.get("content", "No response")
                        with st.expander(f"📤 {name}"):
                            st.markdown(content)

        except Exception as e:
            st.error(f"🔌 Connection error: {e}")
