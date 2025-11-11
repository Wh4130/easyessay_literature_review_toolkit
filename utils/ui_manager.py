import streamlit as st 
from utils.data_manager import DataManager
from utils.others import Others
import streamlit.components.v1 as components
import requests


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

            backend_health_check = requests.get("https://easyessaybackend.onrender.com/health")
            if backend_health_check.status_code != 200:
                st.warning("Backend server collapsed! Please try again later.")
            else:
                st.caption("Backend server is healthy.")
            

    @staticmethod
    def show_fullscreen_demo():
        demo_html = """
        <div>
        <script async src="https://js.storylane.io/js/v2/storylane.js"></script>
        <div class="sl-embed" style="width:100%;height:75vh;position:relative;">
            <iframe loading="lazy" 
                    class="sl-demo" 
                    src="https://app.storylane.io/demo/qbcm12pavvyo?embed=inline" 
                    name="sl-embed" 
                    allow="fullscreen" 
                    allowfullscreen 
                    style="position:absolute;top:0;left:0;width:100%;height:100%;border:none;border-radius:10px;box-sizing:border-box;">
            </iframe>
        </div>
        </div>
        """
        
        components.html(demo_html, height=600, scrolling=False)

    index_explanation_text = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>EasyEssay Literature Review Tool</title>
    <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Libertinus+Mono&family=Noto+Serif+TC:wght@200..900&display=swap" rel="stylesheet">
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}     
        /* 不要設置 body，而是設置你的容器 */
        .welcome-container {{
            font-family: "Noto Serif TC", serif !important;
            padding: 20px;
            border-radius: 6px;
            margin: 0 auto;
            background: linear-gradient(135deg, #F4F4F2, #FBE7F0);
        }}
        
        /* 對所有子元素設置字體 */
        .welcome-container, 
        .welcome-container h1, 
        .welcome-container h2, 
        .welcome-container h3, 
        .welcome-container p, 
        .welcome-container span:not(.material-symbols-outlined) {{
            font-family: "Noto Serif TC", serif !important;
        }}
        .material-symbols-outlined {{
            font-family: 'Material Symbols Outlined' !important;
            font-size: 48px;
            color: #3f429d;
        }} 
        .header {{
            text-align: center;
            margin-bottom: 30px;
        }}
        .title {{
            font-size: 2.5rem;
            font-weight: 600;
            color: #2c3e50;
            margin-bottom: 8px;
            letter-spacing: -0.02em;
        }}
        .title-with-icon {{
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 12px;
            margin-bottom: 8px;
        }}
        .title-icon {{
            width: 100px;
            height: 100px;
        }}
        .title:hover {{
            color: navy;
        }}
        .title-accent {{
            color: #656566;
        }}
        .title-accent:hover {{
            color: #BE6B6B;
        }}
        .subtitle {{
            font-size: 1.2rem;
            color: #6c757d;
            font-weight: 400;
        }}
        .subtitle:hover {{
            background: linear-gradient(135deg, blue, orange);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
            font-weight: 400;
        }}
        .description {{
            text-align: center;
            font-size: 1.1rem;
            color: #495057;
            margin-bottom: 40px;
            line-height: 1.6;
        }}
        .description:hover {{
            background: linear-gradient(135deg, blue, orange);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
        }}
        .section {{
            margin-bottom: 40px;
        }}
        .section-title {{
            font-size: 1.5rem;
            font-weight: 600;
            color: #2c3e50;
            margin-bottom: 20px;
            text-align: center;
            letter-spacing: -0.01em;
        }}
        .features {{
            display: grid;
            grid-template-columns: repeat(1, 1fr);
            gap: 24px;
            margin-bottom: 40px;
        }}
        .feature-item {{
            background: #fafbfc;
            border-radius: 5px;
            padding: 24px;
            text-align: center;
            border: 1px solid #e9ecef;
            transition: all 0.2s ease;
        }}
        .feature-item:nth-child(1):hover {{
            background: linear-gradient(135deg, #FF9A8B, #A8E6CF);
            color: white;
        }}
        
        .feature-item:nth-child(2):hover {{
            background: linear-gradient(135deg, #84FAB0, #8FD3F4);
            color: white;
        }}
        
        .feature-item:nth-child(3):hover {{
            background: linear-gradient(135deg, #7393E1, #EC7A77);
            color: white;
        }}
        
        .feature-item:nth-child(4):hover {{
            background: linear-gradient(135deg, #FFD3A5, #FD9853);
            color: white;
        }}
        
        .feature-item:hover .feature-title {{
            color: inherit;
        }}
        
        .feature-item:hover .feature-description {{
            color: inherit;
            opacity: 0.9;
        }}
        
        .feature-item:hover .feature-icon {{
            color: inherit;
        }}
        
        
        .feature-icon {{
            font-size: 2.2rem;
            margin-bottom: 12px;
            display: block;
            color: #8FA4B0;
        }}

        .feature-title {{
            font-size: 1.1rem;
            font-weight: 500;
            color: #2c3e50;
            margin-bottom: 8px;
        }}

        .feature-description {{
            color: #6c757d;
            line-height: 1.5;
            font-size: 0.9rem;
        }}
        .pages-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 20px;
        }}
        .page-item {{
            background: white;
            border-radius: 8px;
            padding: 20px;
            border: 1px solid #dee2e6;
            transition: all 0.2s ease;
        }}
        .page-item:hover {{
            border-color: #8FA4B0;
            box-shadow: 0 2px 8px rgba(143, 164, 176, 0.1);
        }}
        .page-header {{
            display: flex;
            align-items: center;
            margin-bottom: 12px;
        }}
        .page-icon {{
            font-size: 1.5rem;
            color: #8FA4B0;
            margin-right: 12px;
        }}
        .page-title {{
            font-size: 1rem;
            font-weight: 500;
            color: #2c3e50;
        }}
        .page-description {{
            color: #6c757d;
            line-height: 1.5;
            font-size: 0.85rem;
        }}
        @media (max-width: 768px) {{
            .welcome-container {{
                padding: 30px 20px;
                margin: 10px;
            }}
            .features {{
                grid-template-columns: 1fr;
                gap: 20px;
            }}
            .pages-grid {{
                grid-template-columns: 1fr;
            }}
            .title {{
                font-size: 2rem;
            }}
        }}
    </style>
</head>
<body>
    <div class="welcome-container">
        <div class="header">
            <div class="title-with-icon">
                <img src="data:image/png;base64,{DataManager.image_to_b64("./pics/icon.png")}" 
                    alt="EasyEssay Logo" 
                    class="title-icon">
                <h1 class="title">Easy<span class="title-accent">Essay</span></h1>
            </div>
            <p class="subtitle">AI-Powered Literature Review Companion</p>
        </div>
        <div class="description">
            Upload documents to organize, summarize, and interact with your academic literature seamlessly.
        </div>
        <div class="section">
            <h2 class="section-title">Core Features</h2>
            <div class="features">
                <div class="feature-item">
                    <span class="material-symbols-outlined">newsstand</span>
                    <h3 class="feature-title">Smart Organization</h3>
                    <p class="feature-description">
                        Organize papers with intelligent tagging and categorization systems.
                    </p>
                </div>
                <div class="feature-item">
                    <span class="material-symbols-outlined">motion_photos_auto</span>
                    <h3 class="feature-title">AI Summaries</h3>
                    <p class="feature-description">
                        Get instant, comprehensive summaries powered by advanced language models.
                    </p>
                </div>
                <div class="feature-item">
                    <span class="material-symbols-outlined">forum</span>
                    <h3 class="feature-title">Interactive Chat</h3>
                    <p class="feature-description">
                        Ask questions and explore documents through RAG-powered conversations.
                    </p>
                </div>
                <div class="feature-item">
                    <span class="material-symbols-outlined">admin_panel_settings</span>
                    <h3 class="feature-title">Private Database</h3>
                    <p class="feature-description">
                        Your own Google Sheets database ensures complete privacy and data ownership.
                    </p>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
"""