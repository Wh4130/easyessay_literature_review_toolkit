import streamlit as st 
from utils.data_manager import DataManager
from utils.others import Others

class UIManager:
        
    @staticmethod
    def render_sidebar():
        with st.sidebar:
            
            # * Icon & Title
            text_box, icon_box = st.columns((0.7, 0.3))
            with icon_box:
                st.markdown(f'''
                                <img class="image" src="data:image/jpeg;base64,{DataManager.image_to_b64(f"./pics/icon.png")}" alt="III Icon" style="width:500px;">
                            ''', unsafe_allow_html = True)
            with text_box:
                st.write(" ")
                st.header("Easy Essay")
                st.caption(f"**Literature Review Tool**")

            # * Pages
            if st.session_state["logged_in"]:
                st.page_link("index.py", label = 'Introduction & Demos', icon = ":material/info:")
                st.page_link("./pages/page_docs.py", label = 'Literature Management', icon = ":material/folder_open:")
                st.page_link("./pages/page_chat.py", label = 'Chat with Literature', icon = ":material/mark_chat_unread:")
                st.page_link("./pages/page_upload.py", label = 'Upload & Summarize Literature', icon = ":material/edit_square:")
                st.page_link("./pages/page_account.py", label = 'Account', icon = ":material/account_circle:")



            Others.fetch_IP()   