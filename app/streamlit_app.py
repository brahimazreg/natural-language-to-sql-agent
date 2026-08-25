import requests
import streamlit as st
import os

from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv(
    "API_URL",
    "http://127.0.0.1:8000/query",
)


st.set_page_config(
    page_title="Natural Language → SQL",
    page_icon="🗄️",
)

st.title("🗄️ Natural Language → SQL Agent")
st.write("Ask questions about the student database.")

query = st.text_input(
    "Your question",
    placeholder="e.g. Show me all students",
)

if st.button("Run Query", type="primary"):
    if not query.strip():
        st.warning("Please enter a question.")
    else:
        try:
            with st.spinner("Running query..."):
                response = requests.post(
                    API_URL,
                    json={"query": query},
                    timeout=60,
                )

            if response.status_code == 200:
                data = response.json()

                st.success("Query executed successfully.")

                answer = data.get("answer", [])

                if answer:
                    st.dataframe(
                        answer,
                        use_container_width=True,
                    )
                else:
                    st.info("No results found.")

            else:
                try:
                    error = response.json().get(
                        "detail",
                        "Unknown error",
                    )
                except Exception:
                    error = response.text

                st.error(error)

        except requests.exceptions.RequestException as e:
            st.error(f"Could not connect to API: {e}")