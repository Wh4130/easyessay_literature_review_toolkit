
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import streamlit as st 
import pandas as pd
import time
import json

class SheetManager:

    @staticmethod
    def authenticate_google_sheets():
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_dict(json.loads(st.secrets['gsheet-conn']['credits']), scope)
        client = gspread.authorize(creds)
        return client
    
    @staticmethod
    def extract_sheet_id(sheet_url):
        try:
            return sheet_url.split("/d/")[1].split("/")[0]
        except IndexError:
            st.error("無效的試算表連結，請檢查 URL 格式。")
            return None
        
    @staticmethod
    def fetch(sheet_id, worksheet):
        if sheet_id:
            client = SheetManager.authenticate_google_sheets()
            try:
                sheet = client.open_by_key(sheet_id)
                ws = sheet.worksheet(worksheet)
                
                # 手動獲取所有值
                all_values = ws.get_all_values()
                
                if not all_values:
                    st.write("No data found in worksheet")
                    return pd.DataFrame()
                
                # 第一行作為 headers
                headers = all_values[0]
                
                # 其餘行作為 data
                data_rows = all_values[1:] if len(all_values) > 1 else []
                
                # 創建 DataFrame 並設置 columns
                df = pd.DataFrame(data_rows, columns=headers)
                
                return df
                
            except Exception as e:
                st.write(f"Connection Failed: {e}")
                return pd.DataFrame()

    @staticmethod
    def insert(sheet_id, worksheet, row: list):
        if sheet_id:
            client = SheetManager.authenticate_google_sheets()
            try:
                sheet = client.open_by_key(sheet_id)
                worksheet = sheet.worksheet(worksheet)
                worksheet.freeze(rows = 1)
                worksheet.append_row(row)

                records = worksheet.get_all_records()
                
            except Exception as e:
                st.write(f"Connection Failed: {e}")

    @staticmethod
    def update(sheet_id, worksheet_name, row_idxs, column, values):
        mapping = {
            "user_docs": {
                "_fileId": "A",
                "_fileName": "B", 
                "_summary": "C",
                "_generatedTime": "D",
                "_length": "E",
                "_tag": "F"  
            },
            "user_tags": {
                "_tagId": "A",
                "_tag": "B" 
            },
            "user_info": {
                "_dbURL": "F"
            }
        }
        if sheet_id:
            client = SheetManager.authenticate_google_sheets()
            for idx, value in zip(row_idxs, values):
                try:
                    sheet = client.open_by_key(sheet_id)
                    worksheet = sheet.worksheet(worksheet_name)
                    pos = f"{mapping[worksheet_name][column]}{idx + 2}"
                    worksheet.update_acell(pos, value)
                    
                except Exception as e:
                    st.write(f"Connection Failed: {e}")

    @staticmethod
    def delete_row(sheet_id, worksheet_name, row_idxs: list):

        if not sheet_id:
            st.write("No sheet_id provided!")
            return
        
        while True:
            try:
                client = SheetManager.authenticate_google_sheets()

                sheet = client.open_by_key(sheet_id)
                worksheet = sheet.worksheet(worksheet_name)

                if SheetManager.acquire_lock(sheet_id, worksheet_name):
                    for idx in sorted(row_idxs, reverse = True):
                        worksheet.delete_rows(idx + 2)
                    break
                else:
                    pass


            except Exception as e:
                st.write(f"Failed to delete row: {e}")
                break

    @staticmethod
    def acquire_lock(sheet_id, worksheet_name, timeout = 10):
        lock_maps = {
            "user_info": "G1",
            "user_docs": "G1",
            "user_tags": "C1",
            "user_chats": "F1"
        }

        """
        Acquire a lock before editing.
        :param worksheet: The gspread worksheet object.
        :param lock_pos: the position of the cell that stores the lock status
        :param timeout: Max time (in seconds) to wait for lock.
        :return: True if lock acquired, False otherwise.
        """
        start_time = time.time()
        client = SheetManager.authenticate_google_sheets()
        sheet = client.open_by_key(sheet_id)
        worksheet = sheet.worksheet(worksheet_name)
        with st.spinner("Waiting for lock..."):
            while time.time() - start_time < timeout:
                lock_status = worksheet.acell(lock_maps[worksheet_name]).value

                if lock_status == "Unlocked":
                    # Acquire the lock
                    worksheet.update_acell(lock_maps[worksheet_name], st.session_state["user_id"])
                    
                    return True
                
                elif lock_status == st.session_state["user_id"]:
                    # Already locked by the same user
                    return True
                
                time.sleep(0.5)

        return False
    
    @staticmethod
    def release_lock(sheet_id, worksheet_name):
        """
        Release the lock after editing.
        :param worksheet: The gspread worksheet object.
        :param user_email: The email of the user trying to release the lock.
        :return: True if lock released, False otherwise.
        """
        lock_maps = {
            "user_info": "G1",
            "user_docs": "G1",
            "user_tags": "C1",
            "user_chats": "F1"
        }

        client = SheetManager.authenticate_google_sheets()
        sheet = client.open_by_key(sheet_id)
        worksheet = sheet.worksheet(worksheet_name)
        lock_status = worksheet.acell(lock_maps[worksheet_name]).value

        if lock_status == st.session_state["user_id"]:
            worksheet.update_acell(lock_maps[worksheet_name], "Unlocked")
            return True
        else:
            st.write("Lock is not held by you!")
            return False
        
    
    

class GoogleSheetDB(SheetManager):

    @staticmethod
    def delete_default_worksheet(sheet_id):
        """
        Delete the default "Untitled spreadsheet" worksheet
        
        Args:
            sheet_id (str): Google Sheet ID
        """
        try:
            client = GoogleSheetDB.authenticate_google_sheets()
            sheet = client.open_by_key(sheet_id)
            
            # Get all worksheets
            worksheets = sheet.worksheets()
            
            # Find default worksheet (usually the first one)
            default_worksheet_names = ["Untitled spreadsheet", "Sheet1", "工作表1", "未命名的工作表"]
            
            for worksheet in worksheets:
                if worksheet.title in default_worksheet_names:
                    # Ensure it's not the only worksheet
                    if len(worksheets) > 1:
                        st.info(f"Deleting default worksheet: {worksheet.title}")
                        sheet.del_worksheet(worksheet)
                        st.success(f"✅ Deleted default worksheet: {worksheet.title}")
                        return True
                    else:
                        st.warning("⚠️ Cannot delete the only worksheet, please create other worksheets first")
                        return False
            
            st.info("ℹ️ No default worksheet found")
            return True
            
        except Exception as e:
            st.error(f"❌ Error deleting default worksheet: {str(e)}")
            return False

    @staticmethod
    def setup_database_schema(sheet_id, reset_existing=False, delete_default=True):
        """
        Set up Google Sheet database schema
        Create necessary worksheets and header rows
        
        Args:
            sheet_id (str): Google Sheet ID
            reset_existing (bool): Whether to reset existing worksheets
            delete_default (bool): Whether to delete default "Untitled spreadsheet"
        """
        
        # Define database schema
        schema = {
            "user_docs": {
                "headers": ["_fileId", "_fileName", "_summary", "_generatedTime", "_length", "_tag"],
                "lock_cell": "G1", 
                "description": "User documents table"
            },
            "user_tags": {
                "headers": ["_tagId", "_tag"],
                "lock_cell": "C1",
                "description": "User tags table"
            },
            "user_chats": {
                "headers": ["_fileId", "_role", "_content", "_model", "_time"],
                "lock_cell": "F1",
                "description": "User chat history table"
            }
        }
        
        if not sheet_id:
            st.error("No sheet_id provided!")
            return False
        
        try:
            client = GoogleSheetDB.authenticate_google_sheets()
            sheet = client.open_by_key(sheet_id)
            
            # Iterate through all worksheet schemas
            with st.status(f"Setting up Database"):

                for worksheet_name, config in schema.items():
                    try:
                        st.write(f"Setting up worksheet: {worksheet_name} ({config['description']})")
                        
                        # Check if worksheet exists
                        try:
                            worksheet = sheet.worksheet(worksheet_name)
                            if reset_existing:
                                st.warning(f"Worksheet {worksheet_name} already exists, resetting...")
                                worksheet.clear()
                            else:
                                st.info(f"Worksheet {worksheet_name} already exists, skipping creation")
                                continue
                        except gspread.WorksheetNotFound:
                            st.info(f"Creating new worksheet: {worksheet_name}")
                            worksheet = sheet.add_worksheet(
                                title=worksheet_name,
                                rows=1000,  # Default row count
                                cols=20     # Default column count
                            )
                            
                        
                        # Set header row
                        worksheet.update('A1', [config['headers']])
                        
                        # Freeze first row
                        worksheet.freeze(rows=1)
                        
                        # Initialize lock status
                        worksheet.update_acell(config['lock_cell'], "Unlocked")
                        
                        # Format header row (bold)
                        worksheet.format('A1:Z1', {
                            "textFormat": {
                                "bold": True
                            },
                            "backgroundColor": {
                                "red": 0.9,
                                "green": 0.9,
                                "blue": 0.9
                            }
                        })
                            
                        
                    except Exception as e:
                        st.error(f"❌ Error setting up worksheet {worksheet_name}: {str(e)}")
                        continue
            
            # Delete default worksheet (if needed)
            if delete_default:
                GoogleSheetDB.delete_default_worksheet(sheet_id)
            
            st.success("🎉 Database schema setup completed!")
            return True
            
        except Exception as e:
            st.error(f"❌ Error setting up database schema: {str(e)}")
            return False
        

    @staticmethod
    @st.dialog("Set up your own literature database")
    def update_user_db_url():
        input_ = st.text_input("Input the google sheet link...")
        if st.button("Create Database Schema"):
            user_infos = (SheetManager
                            .fetch(
                                SheetManager
                                .extract_sheet_id(st.secrets['gsheet-urls']['user']), "user_info"
                                    ))

            # Verify whether the link exists already
            if input_ in user_infos['_dbURL']:
                st.warning("This URL is used. Please create a new empty google sheet, make it publicly editable, and paste the link here.")
            sheet_id = SheetManager.extract_sheet_id(input_)
            if sheet_id == None:
                st.stop()
            else:
                GoogleSheetDB.setup_database_schema(sheet_id)

            # Update the link to meta database
            SheetManager.update(
                SheetManager.extract_sheet_id(st.secrets['gsheet-urls']['user']),
                "user_info",
                user_infos[user_infos["_userId"] == st.session_state["user_id"]].index,
                column = "_dbURL",
                values = [input_]
            )
            st.session_state["_dbURL"] = input_
            st.rerun()