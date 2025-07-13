import streamlit as st
import requests

class Others:

    @staticmethod
    def fetch_IP():
        response = requests.get("https://api.ipify.org?format=json")
        public_ip = response.json()["ip"]
        st.caption(f"Deployed IP Address: **:blue[{public_ip}]**")