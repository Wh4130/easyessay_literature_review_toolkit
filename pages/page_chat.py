import streamlit as st
import pandas as pd
import time
from datetime import datetime
import io
from utils.data_manager import DataManager
from utils.llm_manager import ChatBot
from utils.prompt_manager import PromptManager
from utils.sheet_manager import SheetManager
from utils.user_manager import UserManager
from utils.docs_manager import PineconeManager
from utils.others import Others
from utils.constants import Consts
from utils.ui_manager import UIManager

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

if "ChatBot" not in st.session_state:
    st.session_state["ChatBot"] = ChatBot()

if "PineconeDB" not in st.session_state:
    st.session_state["PineconeDB"] = PineconeManager()

if "characters" not in st.session_state:
    st.session_state["characters"] = {
        "user": ":material/face_3:",
        "assistant": ":material/robot_2:",
        "system": ":material/brightness_alert:"
    }

if "chat_params" not in st.session_state:
    st.session_state["chat_params"] = {
        "RAG_strictness": "high",
        "doc_id": "N/A",
        "summary": "N/A",
        "top_k": 5,
        "additional_sys_prompt": None
    }

# * - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# *** Sidebar Config
UIManager.render_sidebar()


# * - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# *** Function that renders selectbox for tags and documents
def ConfigLiterature():
    selected_tag = st.selectbox(":material/bookmark: Select a tag", [key for key in st.session_state['user_tags']['_tag']])
    XOR = st.session_state['user_docs']["_tag"] == selected_tag  
    selected_file = st.selectbox(":material/book_ribbon: Select a paper to chat", [key for key in st.session_state['user_docs'][XOR]['_fileName']])

    if selected_file:
        doc_id = st.session_state['user_docs'].loc[st.session_state['user_docs']['_fileName'] == selected_file, '_fileId'].tolist()[0]
        summary = st.session_state['user_docs'].loc[st.session_state['user_docs']['_fileName'] == selected_file, '_summary'].tolist()[0]

        st.session_state['chat_params']["doc_id"] = doc_id
        st.session_state['chat_params']["summary"] = summary
    else:
        st.session_state['chat_params']["doc_id"] = None
        st.session_state['chat_params']["summary"] = None
# * - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# *** Function that allows modification for LLM setting
def ConfigLLM():
    # * Model selection
    selected_model = st.selectbox(":material/toggle_on: Select the model", Consts.gemini_model_list)
    st.session_state["ChatBot"].changeModel(selected_model)

    # * Set top_k
    top_k = st.slider(":material/linear_scale: Select parameter k", 
                      value = 5,
                      min_value = 1, 
                      max_value = 20, 
                      help = """When you ask question, before sending your question to the AI model, the backend program first :blue[queries the **k** most similar text chunks from the literature], and then provides the result texts to AI model so that it can answer more precisely. 
                      
The higher :blue[**k**] is, the more contextual information is provided to AI. """)
    
    st.session_state["chat_params"]['top_k'] = top_k

# * - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# *** Function for the UI of chat history saving, and chat system prompt addition.
def ConfigChat():

    @st.dialog("Add additional system instructions")
    def additional_chat_sys_prompt():
        additional_prompts = st.text_area(
            "Additional system instructions.",
            value = st.session_state["chat_params"]["additional_sys_prompt"])
        if st.button("Save", width = "stretch"):
            st.session_state["chat_params"]["additional_sys_prompt"] = additional_prompts
            st.rerun()

    if st.button("Customize System Prompts", width = "stretch"):
        additional_chat_sys_prompt()


    # * Chat History Download
    st.caption(f"**:gray[Download Chat History]**", help = """1. First, click the **:blue[Prepare Chat History]** button.
2. Then click the download button on the right hand side. The download will start automatically. 
               
Chat histories will be saved in excel format.
""")
    chat_l, chat_r = st.columns((0.8, 0.2))
    chat_hist_io = b""

    with chat_l:
        if st.button("Prepare Chat History", "transform_chat_history", width = "stretch"):
            chat_hist_io = DataManager.compile_chat_histories(st.session_state["messages"])
    
    with chat_r:
        st.download_button(
            label    = "",
            data     = chat_hist_io,
            mime     = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            file_name = f"chat_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
            icon     = ":material/download:",
            type     = "primary" if chat_hist_io else "secondary",
            width = "stretch"
        )

def main():

    with st.sidebar:
        # * Selection box for selecting documents to chat with
        with st.container(border = True, height = 310):
            st.subheader(":material/settings: Settings")

            TAB_DOCS, TAB_MODEL, TAB_CHAT = st.tabs(["Literature", "Model", "Chat"])

            with TAB_DOCS:
                ConfigLiterature()
            with TAB_MODEL:
                ConfigLLM()
            with TAB_CHAT:
                ConfigChat()

            
        if st.button("Refresh", "reload", icon = ":material/refresh:", width = "stretch"):
            del st.session_state["pdfs_raw"]
            del st.session_state["user_docs"]
            del st.session_state["user_tags"]
            del st.session_state["user_chats"]
            del st.session_state["messages"]
            st.rerun()

        

        
        st.caption(f"Logged in as: **{st.session_state['user_id']}**")

    st.title("Chat with Literature")
    if not st.session_state['chat_params']["doc_id"]:
            st.warning("There is no literature under the selected tag. Please upload the literature in **Upload & Summarize Literature** page under the tag, or choose other tags.")
            st.stop()


    with st.expander(":material/dashboard: Literature Summary"):
        st.markdown(st.session_state['chat_params']['summary'], unsafe_allow_html = True)

    
    

    if st.session_state['chat_params']['doc_id'] not in st.session_state["messages"].keys():
        with st.chat_message("assistant", avatar = st.session_state["characters"]["assistant"]):
            st.markdown("**:blue[Ask me something about the paper!]**")
    else:
        for i, message in enumerate(
            st.session_state.messages[st.session_state['chat_params']['doc_id']]['chat_history']
            ):
            with st.chat_message(message["role"], avatar = st.session_state["characters"][message["role"]]):
                st.markdown(message["content"])

        


    if in_message := st.chat_input("Ask something regarding the selected literature:"):

        # *** --- User Input
        # Add user message to chat history
        user_input_time = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
        
        # Display user message in chat message container
        with st.chat_message("user", avatar = st.session_state["characters"]["user"]):
            st.markdown(in_message)

        (st.session_state.messages[st.session_state['chat_params']['doc_id']]['chat_history']
         .append({"role": "user", 
                  "content": in_message, 
                  "time": user_input_time,
                  "model": st.session_state["ChatBot"].model_key}))
        # Add user message to chat database (google sheet)
        SheetManager.insert(
            sheet_id  = st.session_state["sheet_id"],
            worksheet = "user_chats",
            row       = [st.session_state["chat_params"]["doc_id"], "user", in_message, "-", user_input_time]
        )

        # *** --- Query from Pinecone Embedding DB
        similar_text_ls = st.session_state["PineconeDB"].search(
                                            query = in_message, 
                                            k = st.session_state["chat_params"]['top_k'], 
                                            namespace = st.session_state["chat_params"]["doc_id"],   # napespace = document ID
                                            index_name = "easyessay"
        )
        # Display assistant response in chat message container
        try:
            with st.chat_message("assistant", avatar = st.session_state["characters"]["assistant"]):
                
                stream = (st.session_state["ChatBot"]
                          .apiCall(in_message,
                                   similar_text_ls,
                                    doc_summary = st.session_state["chat_params"]["summary"],
                                    additional_prompt = st.session_state["chat_params"]["additional_sys_prompt"]))
                
                
                response = st.write_stream(stream)

                if not st.session_state["ChatBot"].checkRagAvailability(st.session_state["chat_params"]["doc_id"]):
                    st.warning("This literature is not in the vector database, so the answer is only based on the summary!")
                
                assistant_answer_time = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
                (st.session_state.messages[st.session_state['chat_params']['doc_id']]['chat_history']
                .append({"role": "assistant", 
                         "content": response, 
                         "time": assistant_answer_time,
                         "model": st.session_state["ChatBot"].model_key}))
                
            # Add assistant message to chat database (google sheet)
            SheetManager.insert(
                sheet_id   = st.session_state["sheet_id"],
                worksheet  = "user_chats",
                row        = [st.session_state["chat_params"]["doc_id"], 
                                "assistant", 
                                response, 
                                st.session_state["ChatBot"].model_key, 
                                assistant_answer_time]
                        )
                
                
            
        except Exception as e:
            st.write(e)
            with st.chat_message("assistant", avatar = st.session_state["characters"]["system"]):
                st.error("**We encountered some errors when connecting to Gemini API... Please try again later. Remember to save the chat history if needed!**")




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