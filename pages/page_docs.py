import streamlit as st
import pandas as pd
import time
from utils.data_manager import DataManager
from utils.llm_manager import Summarizor
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

if "sheet_id" not in st.session_state:
    st.session_state["sheet_id"] = SheetManager.extract_sheet_id(st.session_state['_dbURL'])

if "user_docs" not in st.session_state:
    st.session_state['user_docs'] = SheetManager.fetch(st.session_state["sheet_id"], "user_docs")

if "user_tags" not in st.session_state:
    st.session_state["user_tags"] = SheetManager.fetch(st.session_state["sheet_id"], "user_tags")

# * - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# *** Sidebar Config
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

# * - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# *** HTML & CSS
st.html("""<style>
div.stButton > button {
    width: 100%;  /* 設置按鈕寬度為頁面寬度的 60% */
    height: 50px;
    margin-left: 0;
    margin-right: auto;
}
</style>
""")



# * - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# *** Main
def main():
    st.title("Literature Management")
    
    # * Render user name and refresh button after logged in
    with st.sidebar:
        if st.button("Refresh", key = "reload", icon = ":material/refresh:"):
            del st.session_state["user_docs"]
            del st.session_state["user_tags"]
            st.rerun()
    
        st.caption(f"Logged in as: **{st.session_state['user_id']}**")

    # * Define primary tabs: Literature Summary / Literature Lists / Manage your Tags
    TAB_READ, TAB_EDIT, TAB_TAGS = st.tabs(["Literature Summary", "Literature Lists", "Manage your Tags"])
            

    # *** Literature Summary ***
    with TAB_READ:
        read_c1, read_c2 = st.columns(2)
        with read_c1:
            selected_tag = st.selectbox("Select a tag", [key.replace(" ", "_") for key in st.session_state['user_tags']['_tag']])
        XOR = st.session_state['user_docs']["_tag"] == selected_tag                       
        with read_c2:
            selected_file = st.selectbox("Select a paper", [key.replace(" ", "_") for key in st.session_state['user_docs'][XOR]['_fileName']])
        
        with st.spinner("loading"):
            try:
                res = st.session_state['user_docs'].loc[st.session_state['user_docs']['_fileName'] == selected_file, '_summary'].tolist()[0]
                st.markdown(res, unsafe_allow_html = True, help = "hah")
            except:
                st.warning("""There is no literature under the selected tag.

Please upload a new literature at **Upload & Summarize Literature** page.""")
                if st.button("Upload & Summarize Literature", icon = ":material/edit_square:"):
                    st.switch_page("page_upload.py")
    
    # *** 文獻摘要一覽 & 編輯 ***
    with TAB_EDIT:
        st.session_state['user_docs']["_selected"] = False
        st.session_state['user_docs']['_tagModified'] = False    # * add a column to check whether '_tag' column is modified
        edit_files = st.data_editor(
            st.session_state['user_docs'],
            disabled = ["_fileId", "_fileName", "_length"],
            column_order = ["_selected", "_fileId", "_fileName", "_tag", "_length"],
            width = 1000,
            hide_index = True,
            column_config = {
                "_selected": st.column_config.CheckboxColumn(
                    "Select",
                    width = "small"
                ),
                "_fileId": st.column_config.TextColumn(
                    "Literature ID",
                    width = "small"
                ),
                "_fileName": st.column_config.TextColumn(
                    "Title",
                    width = "medium"
                ),
                "_length": st.column_config.ProgressColumn(
                    "Summary Length",
                    width = "small",
                    min_value = 0,
                    format="%f",
                    max_value = 30000
                ),
                "_tag": st.column_config.SelectboxColumn(
                    "Tag",
                    help = "The class label for the literature (editable)",
                    options = st.session_state['user_tags']['_tag'].tolist(),
                    required = True
                ),
                "_summary": None,
                "_generatedTime": None,
                "_userId": None
            })

        c_del, c_update = st.columns(2)

        # ** Button for deleting files from the database **
        # * First check if there's any file to be deleted
        with c_del:
            @st.dialog("Are you sure?")
            def FORM_delete():
                st.info("This action is not revertable.")
                l, r = st.columns(2)
                with l:
                    if st.button("Confirm"):
                        st.session_state['delete'] = True
                        st.rerun()
                with r:
                    if st.button("Cancel"):
                        st.rerun()

            if st.button("Delete Literature", key = "delete_literature", icon = ":material/delete_forever:"):
                if len(edit_files[edit_files['_selected'] == True]) == 0:
                    st.warning("Please select the literatures that you want to delete")
                    time.sleep(1)
                    st.rerun()
                
                FORM_delete()

            if "delete" in st.session_state:
                with st.spinner("Deleting..."):

                    # * Acqcuire lock for the user first, before deletion
                    SheetManager.acquire_lock(st.session_state["sheet_id"], "user_docs")
                    
                    # * Reload the user_docs data before deletion, after lock
                    st.session_state["user_docs"] = SheetManager.fetch(st.session_state["sheet_id"], "user_docs")

                    # * Delete the file in the selected
                    SheetManager.delete_row(
                        sheet_id = st.session_state["sheet_id"],
                        worksheet_name = "user_docs",
                        row_idxs = st.session_state["user_docs"][[ True if id in edit_files[edit_files['_selected']]['_fileId'].tolist() else False for id in st.session_state["user_docs"]["_fileId"]]].index
                    )

                    # * Release the lock
                    SheetManager.release_lock(st.session_state["sheet_id"], "user_docs")

                # * Reset session state
                st.success("Deleted")
                time.sleep(1)
                del st.session_state['user_docs']
                del st.session_state["delete"]
                st.rerun()

        # ** Button for updating tags **
        with c_update:
            update_dict = {}
            if not len(edit_files) == 0:
                edit_files['_modified'] = st.session_state['user_docs']['_tag'] != edit_files['_tag']
                # id: new tag
                update_dict = {row["_fileId"]: row["_tag"] for _, row in edit_files.iterrows() if row['_modified']} 
            if st.button("Save Changes of Tags" , icon = ":material/save:"):
                if update_dict == {}:
                    st.warning("No pending changes")
                    time.sleep(1.5)
                    st.rerun()
                with st.spinner("Updating..."):
                    # * Acqcuire lock for the user first, before deletion
                    SheetManager.acquire_lock(st.session_state["sheet_id"], "user_docs")
                    
                    # * Reload the user_docs data before deletion, after lock
                    st.session_state["user_docs"] = SheetManager.fetch(st.session_state["sheet_id"], "user_docs")

                    # * Update
                    SheetManager.update(st.session_state["sheet_id"],
                                        "user_docs",
                                        st.session_state["user_docs"][st.session_state["user_docs"]['_fileId'].isin(update_dict.keys())].index,
                                        "_tag",
                                        [update_dict[i] for i in st.session_state["user_docs"][st.session_state["user_docs"]['_fileId'].isin(update_dict.keys())]['_fileId'].tolist()]
                                        )
                
                    # * Release the lock
                    SheetManager.release_lock(st.session_state["sheet_id"], "user_docs")

                # * Reset session state
                st.success("Updated!")
                del st.session_state['user_docs']
                time.sleep(1.5)
                st.rerun()

    # *** Manage your tags ***
    with TAB_TAGS:
        c1, c2, c3 = st.columns(3)

        # ** Add new tag **
        with c1:
            tag_to_add = st.text_input("Add new tag", key = "add_tag")

            if st.button("Add", icon = ":material/new_label:"):
                if tag_to_add:
                    if tag_to_add in st.session_state["user_tags"]["_tag"].tolist():
                        st.warning("This tag already exists")
                    else:
                        with st.spinner("Adding"):
                            # * acquire lock
                            if SheetManager.acquire_lock(st.session_state['sheet_id'], "user_tags") == False:
                                st.warning("Try again")
                                time.sleep(1.5)
                                st.rerun()
                            
                            # * conduct insertion
                            SheetManager.insert(
                                st.session_state['sheet_id'], 
                                "user_tags", 
                                [DataManager.generate_random_index(), tag_to_add])
                            
                            # * release lock
                            SheetManager.release_lock(st.session_state['sheet_id'], "user_tags")
                            del st.session_state["user_tags"]
                            st.rerun()
                else:
                    st.warning("Please input the name of tag that you want to add")
        
        # ** Delete tags **
        with c2:
            available_tags = st.session_state["user_tags"]["_tag"].tolist()
            available_tags.remove("default")
            tags_to_delete = st.multiselect("Delete a Tag", available_tags)
            if st.button("Delete", icon = ":material/delete_forever:"):
                if not tags_to_delete:
                    st.warning("Please select the tag that you want to delete")
                    time.sleep(1)
                    st.rerun()
                
                with st.spinner("Deleting"):

                    # * Acqcuire lock for the user first, before deletion
                    if SheetManager.acquire_lock(st.session_state["sheet_id"], "user_tags") == False:
                        st.warning("Try again")
                        time.sleep(1)
                        st.rerun()

                    # * Reload tag data after acquireing lock, before deletion
                    st.session_state["user_tags"] = SheetManager.fetch(st.session_state["sheet_id"], "user_tags")

                    # * Delete the selected tags
                    SheetManager.delete_row(
                                sheet_id = st.session_state["sheet_id"],
                                worksheet_name = "user_tags",
                                row_idxs = st.session_state["user_tags"][
                                            (st.session_state["user_tags"]["_tag"].isin(tags_to_delete))
                                        ].index
                                )
                    # * Update the tag for all files of the deleted tag to "default"
                    SheetManager.update(
                        sheet_id = st.session_state["sheet_id"],
                        worksheet_name = "user_docs",
                        row_idxs = st.session_state["user_docs"][
                                    (st.session_state["user_docs"]["_tag"].isin(tags_to_delete))
                                ].index,
                        column = "_tag",
                        values = ["default" for _ in st.session_state["user_docs"][
                                    (st.session_state["user_docs"]["_tag"].isin(tags_to_delete))
                                ].index]
                        
                    )
                    
                    # * Release the lock
                    SheetManager.release_lock(st.session_state["sheet_id"], "user_tags")

                    del st.session_state["user_tags"]
                    del st.session_state["user_docs"]
                    time.sleep(1)
                    st.rerun()

        # ** Tag Database **
        with c3:
            user_tags = st.session_state["user_tags"]["_tag"]
            user_docs = st.session_state["user_docs"]
            user_docs_grouped = pd.merge(user_tags, user_docs, how = "left", on = '_tag').groupby("_tag").agg({"_fileName": "count"})
            st.data_editor(user_docs_grouped, width = 500,
                           disabled = ["_tag", "_fileName"],
                           hide_index = True,
                           column_config = {
                               "_tag": st.column_config.TextColumn(
                                   "Tag"
                               ),
                               "_fileName": st.column_config.ProgressColumn(
                                   "Number of Literatures",
                                    min_value = 0,
                                    format="%f",
                                    max_value = 50,
                                    width = "small"
                               )
                           })


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