import streamlit as st
import pandas as pd
import time

from utils.data_manager import DataManager
from utils.prompt_manager import PromptManager
from utils.sheet_manager import SheetManager
from utils.user_manager import UserManager
from utils.docs_manager import PineconeManager
from utils.others import Others
from utils.ui_manager import UIManager
from utils.constants import Consts

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


# * - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# *** Sidebar Config
UIManager.render_sidebar()



# * - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# *** main function
def main():

    with st.sidebar:
        st.caption(f"Logged in as: **{st.session_state['user_id']}**")


    st.title("User Info")

    st.dataframe(
        pd.DataFrame(
            {"Nickname": [st.session_state['user_name']],
             "User ID": [st.session_state['user_id']],
             "Gmail": [st.session_state['user_email']],
             "Time for registration": [st.session_state['_registerTime']],
             "Database URL": [st.session_state["_dbURL"]]}
        ),
        hide_index = True,
        width = 1000
    )

    # * Button for resetting the database
    # TODO (page_account) update url setting & create button for reset the url


    # * Button for logging out
    if st.button("Log Out", "logout", icon = ":material/logout:", width = "stretch"):
        st.session_state['logged_in'] = False
        st.success("Logged Out")
        for session in ["user_email", "user_id", "_registerTime", "messages", "user_docs", "user_tags", "user_chats",
                        "sheet_id", "_dbURL"]:
            del st.session_state[session]
        time.sleep(2)
        st.rerun()

    # * Button for deregistering
    if st.secrets["permission"]["guest_mode"] == False:     # * guest mode = true -> not able to delete the account
        if st.button("**:red[Delete the Account]**", "deregister", icon = ":material/report:", width = "stretch"):
            UserManager.deregister()



# * - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# *** Authentication
if st.session_state['logged_in'] == False:
    # * 登入頁面
    st.info("Welcome! Please login or sign up to use the tool.")
    entry_l, entry_r = st.columns(2)
    with entry_l:
        if st.button("Login", "login", width = "stretch"):
            UserManager.log_in()
    with entry_r:
        if st.button("Sign Up", "register", width = "stretch"):
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