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
import requests
import json
import time

st.set_page_config(page_title = "Easy Essay - Literature Summary Database", 
                   page_icon = ":material/history_edu:", 
                   layout="centered", 
                   initial_sidebar_state = "auto", 
                   menu_items={
        'Get Help': None,
        'Report a bug': "mailto:huang0jin@gmail.com",
        'About': """
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
    st.title("Upload your Literature")
    
    # * 登入後顯示使用者名稱與重新整理按鈕
    with st.sidebar:
        if st.button("Refresh", "reload", icon = ":material/refresh:"):
            del st.session_state["pdfs_raw"]
            del st.session_state["user_docs"]
            del st.session_state["user_tags"]
            del st.session_state["user_chats"]
            del st.session_state["messages"]
            st.rerun()
            
        st.caption(f"Logged in as: **{st.session_state['user_id']}**")
        # Others.fetch_IP()
    

    # *** 摘要產生器 ***
    # * 定義頁面區塊
    cl, cr = st.columns(2)
    with cl:
        button_upload = st.button("Upload", key = "upload", icon = ":material/upload:")
    with cr:
        button_start = st.button("Summarize", key = "summarize", type = "primary", icon = ":material/start:")
    
    if button_upload:
        DataManager.FORM_pdf_input()

    # * 定義資料預覽 CONTAINER
    BOX_PREVIEW = st.empty()

    # * 定義執行條件
    if button_start:
        # * First check if the raw data is prepared
        if st.session_state['pdfs_raw'].empty:
            st.warning("Please upload your document first！")
            st.stop()

        # * Check the sheet link
        client = SheetManager.authenticate_google_sheets()
        sheet_id = SheetManager.extract_sheet_id(st.session_state['_dbURL'])
        if sheet_id == None:
            st.stop()
        
    

        # TODO 這段，未來會想要前後端分開寫，並用 async
        BOX_PREVIEW.empty()
        # ** Generating Summary
        st.info("Generating summary and updating literature to vector database. Please do not switch to other pages or close this page...")
        # to_update = pd.DataFrame(columns = ["_fileId", "_fileName", "_summary", "_generatedTime", "_length", "_tag"])
        progress_bar = st.progress(0, "(0%)Processing...")

        for i, row in st.session_state['pdfs_raw'].iterrows():
            # --- generate unique idx
            while True:
                fileID = st.session_state["user_id"] + "-" + DataManager.generate_random_index()       #  Generate a random id for the doc
                if fileID not in st.session_state["user_docs"]["_fileId"].tolist():
                    break

            # create data instance by schema 
            doc_data_json = {
                "fileid": fileID,
                "filename": row['filename'].replace(" ", "_"),
                "content": "\n".join(row['content']),
                "user_id": st.session_state['user_id'],
                "tag": row['tag'],
                "lang": row['language'],
                "additional_prompt": row['additional_prompt'],
                "db_url": st.session_state['_dbURL']
            }

            
            progress_bar.progress(i / len(st.session_state['pdfs_raw']), f"({round(i / len(st.session_state['pdfs_raw']), 2) * 100}%)「{doc_data_json['filename']}」...")

            # with st.spinner("Generating Summary..."):
            #     prompt = PromptManager.summarize(row["language"], row["additional_prompt"])
            #     model = Summarizor(language = row['language'], other_instruction = row["additional_prompt"])
            #     summary = model.apiCall(contents)

            # * --- Send request to generate summary in background
            response = requests.post("https://easyessaybackend.onrender.com/summarize", json = doc_data_json)
            # response = requests.post("http://127.0.0.1:8000/summarize", json = doc_data_json) # for testing only
                

            # * --- Update the document to Pinecone Embedding Database
            with st.spinner("Upserting pdfs to Pinecone Embedding Database..."):
                st.session_state['pinecone'].insert_docs(
                    texts = row['content'],
                    namespace = fileID,
                    index_name = st.session_state['pinecone_idx_name']
                )

            # * Initialize chat history container
            with st.spinner("Initializing chat history container..."):
                st.session_state['messages'][fileID] =  {
                    "doc_id": fileID,
                    "doc_name": doc_data_json['filename'],
                    "doc_summary": "N/A",
                    "chat_history": []
                }
                
            
        progress_bar.empty()

        # ** Complete message
        st.success("Literature uploaded and being summarized. Please check the status by clicking the 'Check Status' button that follows, or check the result in **Literature Management** page or **Chat with Literature** page later.")
        time.sleep(1.5)
        del st.session_state["user_docs"]
        del st.session_state["pdfs_raw"]
        
    if st.button("Check Status", 
                key = "check_status", type = "primary", icon = ":material/history_edu:"):
        check_status = requests.get(f"https://easyessaybackend.onrender.com/tasks/{st.session_state['user_id']}")
        # check_status = requests.get(f"http://127.0.0.1:8000/tasks/{st.session_state['user_id']}") # for testing only
        with st.expander("Summary Generation Status"):
            st.dataframe(check_status.json())
            
    # *** 文獻原始資料預覽 ***
    with BOX_PREVIEW.container():
        preview_cache = st.data_editor(st.session_state["pdfs_raw"], 
                    disabled = ["length"], 
                    column_order = ["selected", "filename", "content", "tag", "language", "additional_prompt"],
                    column_config = {
                        "filename": st.column_config.TextColumn(
                            "Filename",
                            width = "medium",
                            max_chars = 200,
                            validate = r".+\.pdf"
                        ),
                        "content": None,
                        "tag": st.column_config.SelectboxColumn(
                            "Tag", 
                            help = "Tag for the literature",
                            width = "small",
                            options = st.session_state["user_tags"]["_tag"].tolist(),
                            required = True
                        ),
                        "language": st.column_config.SelectboxColumn(
                            "Language",
                            help = "Language that is used to generate the summary",
                            width = "small",
                            options = ["English", "Traditional Chinese", "Japanese"],
                            required = True
                        ),
                        "selected": st.column_config.CheckboxColumn(
                            "Select",
                            help = "Select the file that you want to summarize / delete"
                        ),
                        "additional_prompt": st.column_config.TextColumn(
                            "Additional Prompt",
                            help = "Additional instructions that you want to prompt the LLM (optional).",
                            max_chars = 500
                        )
                    },
                    hide_index = True,
                    width = 1000)
        if st.button("Delete selected file", key = "delete_pdf", icon = ":material/delete:"):
            with st.spinner("Deleting"):
                st.session_state["pdfs_raw"] = preview_cache[preview_cache["selected"] == False]
                st.rerun()

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
    st.markdown(UIManager.index_explanation_text, unsafe_allow_html = True)
    
else:
    
    if st.session_state["_dbURL"] in [None, ""]:
        st.subheader("Set up your literature database")
        st.warning("This account does not have database configured. Click the following button to set up your database!")
        st.stop()

    if "sheet_id" not in st.session_state:
        st.session_state["sheet_id"] = SheetManager.extract_sheet_id(st.session_state["_dbURL"])  # * initialized in user_manager!

    if "user_docs" not in st.session_state:
        with st.spinner("loading literature..."):
            st.session_state['user_docs'] = SheetManager.fetch(st.session_state["sheet_id"], "user_docs")

    if "user_tags" not in st.session_state:
        with st.spinner("loading tags..."):
            st.session_state["user_tags"] = SheetManager.fetch(st.session_state["sheet_id"], "user_tags") 

    if "user_chats" not in st.session_state:
        with st.spinner("loading chat histories..."):
            st.session_state["user_chats"] = SheetManager.fetch(st.session_state["sheet_id"], "user_chats") 

    if "messages" not in st.session_state:
        with st.spinner("parsing chat histories..."):
            st.session_state["messages"] = {}
            for _, row in st.session_state['user_docs'].iterrows():
                doc_id = row["_fileId"]
                doc_name = row["_fileName"]
                st.session_state["messages"].update({
                    doc_id: {
                        "doc_name": doc_name,
                        "chat_history": [
                            {
                                "role": row["_role"],
                                "content": row["_content"],
                                "model": row["_model"],
                                "time": row["_time"]
                            }
                            for _, row in st.session_state['user_chats'][st.session_state['user_chats']["_fileId"] == doc_id].iterrows()
                        ] if not st.session_state['user_chats'][st.session_state['user_chats']["_fileId"] == doc_id].empty
                        else []
                    }
                })

    main()