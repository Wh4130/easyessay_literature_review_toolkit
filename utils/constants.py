import streamlit as st 
from utils.data_manager import DataManager




class Consts:

    model_list = [
        "gpt-oss-120b",
        "llama-3.3-70b"
    ]

    page_helps = {
        "index": "",
        "page_account": "",
        "page_chat": "",
        "page_docs": ""
    }

    

    demo_embed_html = """<div>
  <script async src="https://js.storylane.io/js/v2/storylane.js"></script>
  <div class="sl-embed" style="position:absolute;top:0;left:0;width:100vw!important;height:100vw!important;padding-bottom:calc(100% + 25px);width:100%;height:1200px;transform:scale(1)">
    <iframe loading="lazy" class="sl-demo" src="https://app.storylane.io/demo/qbcm12pavvyo?embed=inline" name="sl-embed" allow="fullscreen" allowfullscreen style="position:absolute;top:0;left:0;width:100%!important;height:100%!important;border:1px solid rgba(63,95,172,0.35);box-shadow: 0px 0px 18px rgba(26, 19, 72, 0.15);border-radius:10px;box-sizing:border-box;"></iframe>
  </div>
</div>
"""


   
