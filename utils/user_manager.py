import streamlit as st
import hashlib
import datetime as dt
import time
from utils.data_manager import DataManager
from utils.sheet_manager import SheetManager, GoogleSheetDB

class UserManager:
    # * Hash password
    @staticmethod
    def ps_hash(password: str):
        hash_object = hashlib.sha256(password.encode())
        return hash_object.hexdigest()
    
    # * Verify password
    @staticmethod
    def ps_verify(attempt: str, ps_hashed: str):
        return UserManager.ps_hash(attempt) == ps_hashed


    @staticmethod
    @st.dialog("Login")
    def log_in():
        user_id = st.text_input("User ID or Email")
        password = st.text_input("Password", type = "password")

        if st.secrets["permission"]["guest_mode"]:
            st.info("""Welcome guest! You can log in with:
                    
user id: **guest123** / password: **guest123**. 
                    
You don't need to create a new account.""")
        # * 登入
        if st.button("Login"):

            with st.spinner("Verifying..."):

                # 驗證登入
                st.session_state['user_infos'] = SheetManager.fetch(SheetManager.extract_sheet_id(st.secrets['gsheet-urls']['user']), "user_info")
                if ((user_id not in st.session_state['user_infos']['_userId'].tolist()) and
                    (user_id not in st.session_state['user_infos']['_email'].tolist())):

                    st.warning("User ID / Email Not Found!")
                    st.stop()
                if user_id.endswith("@gmail.com"): 
                    ps_hash_cached = st.session_state['user_infos'].loc[st.session_state['user_infos']['_email'] == user_id, "_password"].tolist()[0]
                else:
                    ps_hash_cached = st.session_state['user_infos'].loc[st.session_state['user_infos']['_userId'] == user_id, "_password"].tolist()[0]
                
                if not UserManager.ps_verify(password, ps_hash_cached):
                    st.warning("Wrong password! Try again!")
                    st.stop()

                # 成功登入
                st.session_state['logged_in'] = True
                

                try:
                    st.session_state['user_name'] = st.session_state['user_infos'].loc[st.session_state['user_infos']['_userId'] == user_id, "_username"].tolist()[0]
                    st.session_state['user_id'] = st.session_state['user_infos'].loc[st.session_state['user_infos']['_userId'] == user_id, "_userId"].tolist()[0]
                    st.session_state['_dbURL'] = st.session_state['user_infos'].loc[st.session_state['user_infos']['_userId'] == user_id, "_dbURL"].tolist()[0]
                

                except:
                    st.session_state['user_name'] = st.session_state['user_infos'].loc[st.session_state['user_infos']['_email'] == user_id, "_username"].tolist()[0]
                    st.session_state['user_id'] = st.session_state['user_infos'].loc[st.session_state['user_infos']['_email'] == user_id, "_userId"].tolist()[0]
                    st.session_state['_dbURL'] = st.session_state['user_infos'].loc[st.session_state['user_infos']['_email'] == user_id, "_dbURL"].tolist()[0]
                    


                st.session_state['user_email'] = st.session_state['user_infos'].loc[st.session_state['user_infos']['_userId'] == st.session_state["user_id"], "_email"].tolist()[0]
                st.session_state['_registerTime'] = st.session_state['user_infos'].loc[st.session_state['user_infos']['_userId'] == st.session_state["user_id"], "_registerTime"].tolist()[0]

                del ps_hash_cached
                del st.session_state["user_infos"]
                st.rerun()

    @staticmethod
    @st.dialog("Register")
    def register():
        username = st.text_input("User Nickname")
        user_id = st.text_input("User ID")
        email = st.text_input("Gmail")
        password_ = st.text_input("Password", type = "password")
        password_confirm = st.text_input("Password Confirmation", type = "password")
        database_url = st.text_input("Please input a PUBLICLY EDITABLE google sheet url as your database.")
        if st.button("Submit", key = "Regist"):
            st.session_state['user_infos'] = SheetManager.fetch(SheetManager.extract_sheet_id(st.secrets['gsheet-urls']['user']), "user_info")
            # * 註冊驗證
            if not username:
                st.warning("Please input User Nickname")
                st.stop()
            if not user_id:
                st.warning("Please input User ID")
                st.stop()
            if user_id in st.session_state['user_infos']['_userId'].tolist():
                st.warning("The User ID has been taken. Please try another one.")
                st.stop()
            if not email:
                st.warning("Please input gmail.")
                st.stop()
            if not email.endswith("@gmail.com"):
                st.warning("Please input valid gmail address.")
                st.stop()
            if email in st.session_state['user_infos']['_email'].tolist():
                st.warning("The gmail has been used to register. Please log in or try a different one.")
                st.stop()
            if not password_:
                st.warning("Please set up your password.")
                st.stop()
            if password_ != password_confirm:
                st.warning("Password confirmation did not match. Try again.")
                st.stop()
            if database_url in st.session_state['user_infos']['_dbURL'].tolist():
                st.warning("URL for data storage used. Open a new empty google sheet, set the link open and editable, and paste it here.")
                st.stop()

            # * Submit registration
            with st.spinner("Registering..."):
                st.session_state['_dbURL'] = database_url
                st.session_state['sheet_id'] = SheetManager.extract_sheet_id(database_url)
                st.session_state["user_tags"] = SheetManager.fetch(st.session_state["sheet_id"], "user_tags") 
                GoogleSheetDB.setup_database_schema(st.session_state['sheet_id'])

                now = dt.datetime.now().strftime("%I:%M%p on %B %d, %Y")
                SheetManager.insert(
                    sheet_id = SheetManager.extract_sheet_id(st.secrets['gsheet-urls']['user']),
                    worksheet = "user_info",
                    row = [username, user_id, email, UserManager.ps_hash(password_), now, database_url]
                )
                while True:
                    default_tag_id = DataManager.generate_random_index()
                    if default_tag_id not in st.session_state['user_tags']['_tag'].tolist():
                        SheetManager.insert(
                            sheet_id = st.session_state['sheet_id'],
                            worksheet = "user_tags",
                            row = [default_tag_id, "default"]
                        )
                        break
            st.success("Successfully registered!")
            time.sleep(3)
            st.session_state["logged_in"] = True
            st.session_state['user_name'] = username
            st.session_state['user_id'] = user_id
            st.session_state['user_email'] = email
            st.session_state['_registerTime'] = now
            st.session_state["_dbURL"] = database_url
            del st.session_state['user_tags']
            del st.session_state["user_infos"]
            st.rerun()

    @staticmethod
    @st.dialog("Confirmation on Deleting Account")
    def deregister():
        st.warning("Warning: \n\nThis operation will delete all user information and relevant data, including the raw text data in the vector database, and is not revertable. The literature summary and chat histories in your google sheet database will not be deleted.", icon = ':material/warning:')
        claim = st.text_input(f"If you are sure to delete the account, please input the User ID：\n\n:red[**{st.session_state['user_id']}**]")
        if st.button("DELETE", key = "confirm_deregister"):

            # *** Check if the claim is correct
            if claim != f"{st.session_state['user_id']}":
                st.warning("Please input the declaration.")
                st.stop()

            # *** Start deleting user informations
            # * deleting user info
            with st.spinner("Deleting user data..."):
                SheetManager.acquire_lock(SheetManager.extract_sheet_id(st.secrets["gsheet-urls"]["user"]),
                                        "user_info")
                st.session_state['user_info'] = SheetManager.fetch(
                    SheetManager.extract_sheet_id(st.secrets["gsheet-urls"]["user"]), "user_info")
                user_idx = st.session_state['user_info'][st.session_state['user_info']['_userId'] == st.session_state['user_id']].index.tolist()
                SheetManager.delete_row(
                    SheetManager.extract_sheet_id(st.secrets["gsheet-urls"]["user"]), "user_info", user_idx)
                SheetManager.release_lock(
                    SheetManager.extract_sheet_id(st.secrets["gsheet-urls"]["user"]), "user_info")
            
            # * ! Documents, Tags and Chat histories are stored in Self-management database. So the deletion of the account does not delete these data in decentralized settings!!
            # # * deleting user docs
            # with st.spinner("Deleting documents..."):
            #     SheetManager.acquire_lock(st.session_state["sheet_id"],
            #                             "user_docs")
            #     st.session_state['user_docs'] = SheetManager.fetch(st.session_state["sheet_id"], "user_docs")
            #     user_docs_idxs = st.session_state['user_docs'][st.session_state['user_docs']['_userId'] == st.session_state['user_id']].index.tolist()
            #     SheetManager.delete_row(st.session_state["sheet_id"], "user_docs", user_docs_idxs)
            #     SheetManager.release_lock(st.session_state["sheet_id"],
            #                             "user_docs")
                
            # # * deleting user tags
            # with st.spinner("Deleting labels..."):
            #     SheetManager.acquire_lock(st.session_state["sheet_id"],
            #                             "user_tags")
            #     st.session_state['user_tags'] = SheetManager.fetch(st.session_state["sheet_id"], "user_tags")
            #     user_tags_idxs = st.session_state['user_tags'][st.session_state['user_tags']['_userId'] == st.session_state['user_id']].index.tolist()
            #     SheetManager.delete_row(st.session_state["sheet_id"], "user_tags", user_tags_idxs)
            #     SheetManager.release_lock(st.session_state["sheet_id"],
            #                             "user_tags")
            
            st.success("Your account has been deleted！")
            time.sleep(1.5)
            for session in ["user_email", "user_id", "_registerTime"]:
                del st.session_state[session]
            st.session_state['logged_in'] = False
            st.rerun()


    

