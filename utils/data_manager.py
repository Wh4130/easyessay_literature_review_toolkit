import streamlit as st
from pypdf import PdfReader
import json
import base64
import string
import random
import pandas as pd
import io

class DataManager:

    @staticmethod
    @st.dialog("請上傳欲處理的檔案（pdf）")
    def FORM_pdf_input():
        pdf_uploaded = st.file_uploader("**請上傳 pdf 檔案（支援多檔案上傳）**", accept_multiple_files = True)
        language = st.selectbox("請選擇摘要語言", ["Traditional Chinese", "English", "Japanese"])
        tag = st.selectbox("請選擇文件類別標籤", st.session_state["user_tags"]["_tag"].tolist())
        instructions = st.text_area("請輸入額外的摘要提示（Optional）")
        if st.button("確認"):
            if language is None:
                st.warning("請選擇語言")
                st.stop()
            if pdf_uploaded:
                for file in pdf_uploaded:
                    if file.name not in st.session_state["pdfs_raw"]["filename"]:
                        pdf_in_messages = DataManager.load_pdf(file)
                        st.session_state["pdfs_raw"].loc[len(st.session_state["pdfs_raw"]), ["filename", "content", "tag", "language", "selected", "additional_prompt"]] = [file.name, pdf_in_messages, tag, language, False, instructions]
                st.session_state["lang"] = language
                st.session_state["other_prompt"] = instructions if instructions else "None"
                st.session_state["tag"] = tag
            else:
                st.warning("請上傳檔案")
                st.stop()
            st.rerun()

    @staticmethod
    @st.cache_data
    def load_pdf(uploaded):

        '''load pdf data from user upload with caching'''
        reader = PdfReader(uploaded)
        number_of_pages = len(reader.pages)
        texts = []
        for i in range(number_of_pages):
            page = reader.pages[i]
            texts.append(f"【page {i}】\n" + page.extract_text())

        return "\n".join(texts)
    
    @staticmethod
    def find_json_object(input_string):
        '''catch the JSON format from LLM response'''

        # Match JSON-like patterns
        input_string = input_string.replace("\n", '').strip()
        input_string = input_string.encode("utf-8").decode("utf-8")
        start_index = input_string.find('{')
        end_index = input_string.rfind('}')

        if start_index != -1 and end_index != -1:
            json_string = input_string[start_index:end_index+1]
            try:
                json_object = json.loads(json_string)
                return json_object
            except json.JSONDecodeError:
                return "DecodeError"
        # st.write(json_string)

        return None  # Return None if no valid JSON is found
    
    # --- Transform Picture to Base64
    @staticmethod
    def image_to_b64(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode("utf-8")
    
    # --- Generate a random index for document
    def generate_random_index():
        characters = string.ascii_letters + string.digits  # a-z, A-Z, 0-9
        return ''.join(random.choices(characters, k = 8))
    
    # --- Compile all chat histories for all literatures
    # def compile_chat_histories(chat_histories: dict[dict]) -> pd.DataFrame:
    #     output = io.BytesIO()

    #     with pd.ExcelWriter(output, engine = "openpyxl") as writer:
    #         for doc_id, doc_data in chat_histories.items():
    #             if doc_data["chat_history"] != []:
    #                 sheet_name = str(doc_data["doc_name"]).replace('/', '_').replace('\\', '_')[:31]
    #                 result_df = pd.DataFrame(columns = ["role", "content"])
                    
    #                 for chat_object in doc_data["chat_history"]:
    #                     result_df.loc[len(result_df), ["role", "content"]] = [
    #                         chat_object["role"],
    #                         chat_object["content"]
    #                     ]
    #                 result_df.to_excel(writer, sheet_name = sheet_name, index = False)

    #     output.seek(0)

    #     return output
    
    def compile_chat_histories(chat_histories: dict[dict]) -> io.BytesIO:
        output = io.BytesIO()
        
        # 檢查是否有任何非空的聊天歷史
        has_chat_data = any(
            doc_data.get("chat_history", []) 
            for doc_data in chat_histories.values()
        )
        
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            sheets_created = 0
            
            for doc_id, doc_data in chat_histories.items():
                chat_history = doc_data.get("chat_history", [])
                
                if chat_history:  # 只處理非空的聊天歷史
                    sheet_name = str(doc_data.get("doc_name", f"Doc_{doc_id}")).replace('/', '_').replace('\\', '_')[:31]
                    
                    # 創建 DataFrame
                    result_df = pd.DataFrame(columns=["role", "content", "time", "model"])
                    
                    # 填充數據
                    for chat_object in chat_history:
                        if isinstance(chat_object, dict) and "role" in chat_object and "content" in chat_object:
                            result_df.loc[len(result_df)] = [
                                chat_object["role"],
                                chat_object["content"],
                                chat_object["time"],
                                chat_object["model"]
                            ]
                    
                    # 寫入工作表
                    result_df.to_excel(writer, sheet_name=sheet_name, index=False)
                    sheets_created += 1
            
            # 如果沒有創建任何工作表，創建一個空的佔位符工作表
            if sheets_created == 0:
                placeholder_df = pd.DataFrame({
                    "Message": ["No chat history available"],
                    "Note": ["All chat histories are empty"]
                })
                placeholder_df.to_excel(writer, sheet_name="No_Data", index=False)
        
        output.seek(0)
        return output

