from utils.data_manager import DataManager
from utils.llm_manager import Summarizor
from utils.prompt_manager import PromptManager
from utils.sheet_manager import SheetManager, GoogleSheetDB
from utils.user_manager import UserManager
from utils.docs_manager import PineconeManager
from utils.others import Others
from utils.constants import Consts
from utils.ui_manager import UIManager

import streamlit as st
import datetime as dt
import random
import pandas as pd
import json
import time

st.set_page_config(page_title = "Easy Essay - Literature Summary Database", 
                   page_icon = ":material/history_edu:", 
                   layout="centered", 
                   initial_sidebar_state = "auto", 
                   menu_items={
        'Get Help': None,
        'Report a bug': "mailto:huang0jin@gmail.com",
        'About': """- Model - **Gemini** 1.5 Flash
- Database Design - Google Sheets
- Developed by - **[Wally, Huang Lin Chun](https://antique-turn-ad4.notion.site/Wally-Huang-Lin-Chun-182965318fa7804c86bdde557fa376f4)**"""
    })
        

# * - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# *** Session State Config
if "pdfs_raw" not in st.session_state:
    st.session_state["pdfs_raw"] = pd.DataFrame(columns = ["filename", "content", "tag", "language", "selected", "additional_prompt"])

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if "user_infos" not in st.session_state:
    st.session_state["user_infos"] = ""

if "user_name" not in st.session_state:
    st.session_state["user_name"] = ""

if "user_id" not in st.session_state:
    st.session_state["user_id"] = ""

if "pinecone" not in st.session_state:
    st.session_state["pinecone"] = PineconeManager()

if "pinecone_idx_name" not in st.session_state:
    st.session_state["pinecone_idx_name"] = "easyessay"



# * - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# *** Sidebar Config
UIManager.render_sidebar()


# * - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# *** HTML & CSS
st.html("""<style>
div.stButton > button {
    width: 100%;  /* 設置按鈕寬度為頁面寬度的 60% */
    height: 50px;
    margin-left: 0;
    margin-right: auto;
}</style>
""")





# * - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# *** Main
def main():

    with st.sidebar:
        st.caption(f"Logged in as: **{st.session_state['user_id']}**")
        # Others.fetch_IP()
    
    TAB_INTRO, TAB_DEMOS = st.tabs(["Introduction", "Demos"])
    with TAB_INTRO:
        st.markdown(Consts.index_explanation_text, unsafe_allow_html = True)

    

# * - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# *** Authentication
if st.session_state['logged_in'] == False:

    # * 登入頁面
    st.info("Welcome! Please login or sign up to use the tool.")
    entry_l, entry_r = st.columns(2)
    with entry_l:
        if st.button("Login", "login"):
            UserManager.log_in()
    with entry_r:
        if st.button("Sign Up", "register"):
            UserManager.register()

    st.markdown(Consts.index_explanation_text, unsafe_allow_html = True)

else:
    
    if st.session_state["_dbURL"] in [None, ""]:
        st.subheader("Set up your literature database")
        st.warning("This account does not have database configured. Click the following button to set up your database!")

        if st.button("Set up database"):
            GoogleSheetDB.update_user_db_url()
            """
            load in google sheet url
            -> create data schema
            -> update the url to the meta database
            """

        st.stop()


    if "sheet_id" not in st.session_state:
        st.session_state["sheet_id"] = SheetManager.extract_sheet_id(st.session_state["_dbURL"])  # * initialized in user_manager!

    if "user_docs" not in st.session_state:
        st.session_state['user_docs'] = SheetManager.fetch(st.session_state["sheet_id"], "user_docs")

    if "user_tags" not in st.session_state:
        st.session_state["user_tags"] = SheetManager.fetch(st.session_state["sheet_id"], "user_tags") 

    if "user_chats" not in st.session_state:
        st.session_state["user_chats"] = SheetManager.fetch(st.session_state["sheet_id"], "user_chats") 

    if "messages" not in st.session_state:
        st.session_state["messages"] = {}
        for doc_id in st.session_state['user_chats']["_fileId"].unique().tolist():
            st.session_state["messages"].update({
                doc_id: {
                    "doc_id": doc_id,
                    "chat_history": [
                        {
                            "role": row["_role"],
                            "content": row["_content"],
                            "model": row["_model"],
                            "time": row["_time"]
                        }
                        for _, row in st.session_state['user_chats'][st.session_state['user_chats']["_fileId"] == doc_id].iterrows()
                    ]
                }
            })

    main()