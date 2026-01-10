<div id="top">

<!-- HEADER STYLE: CLASSIC -->
<div align="center">

<img src="pics/icon.png" width="30%" style="position: relative; top: 0; right: 0;" alt="Project Logo"/>

# EASYESSAY

<em>A RAG-based Literature Information System.</em>

<!-- BADGES -->
<img src="https://img.shields.io/github/last-commit/Wh4130/EasyEssay?style=default&logo=git&logoColor=white&color=0080ff" alt="last-commit">
<img src="https://img.shields.io/github/languages/top/Wh4130/EasyEssay?style=default&color=0080ff" alt="repo-top-language">
<img src="https://img.shields.io/github/languages/count/Wh4130/EasyEssay?style=default&color=0080ff" alt="repo-language-count">

<!-- default option, no dependency badges. -->


<!-- default option, no dependency badges. -->

</div>
<br>



## Overview

**Why EasyEssay?**

This project transforms the literature review process by making academic research more accessible and interactive. The core features include:

> - **📚 Streamlined Literature Review:** Accelerate your research process with organized literature management by tags and languages, making it easier to navigate and synthesize multiple sources.
> - **🤖 RAG-Powered Interactive Literature Chat:** Engage directly with your literature through an intelligent chat interface. Ask questions, extract insights, and explore concepts within your documents using advanced RAG (Retrieval-Augmented Generation) technology that prevents AI hallucination.
> - **⚡ Flexible AI Model Selection:** Choose from two AI models (llama-3.3-70b and gpt-oss-120b) based on your needs.
> - **👤 Personalized Research Environment:** Maintain your own secure account with personalized literature collections and chat histories.

**Transform your literature review from a tedious process into an interactive, AI-enhanced research experience that helps you understand and synthesize academic content more effectively.**

---
## Technology
| Aspect | Technology |
| --- | --- |
| Frontend | [Streamlit](https://streamlit.io/) |
| Backend | [Render](https://render.com/) |
| Vector Database | [Pinecone](https://www.pinecone.io/) | 
| Database | Google Sheets|
| LLM Provider | [Cerebras](https://cloud.cerebras.ai/) |
| Model | Llama-3.3-70b / GPT-OSS-120b |

---




## Architecture

### Literature Upload

```mermaid
flowchart LR
U(((User)))

subgraph UI ["User Interface"]
	p[[page_upload.py]]
end

U -->|Upload| p

p -->|vectorize| VDB[("Vector Database (Pinecone)")]

subgraph Backend ["Backend"]
	LLM(["Language Model Summarization"])
end


p -->|invoke & summarize| LLM
LLM --> DB[("Google Sheet")]

```

### Chat with Literature


```mermaid
flowchart LR
U(((User)))

subgraph UI ["User Interface"]
	p[[Chatbox]]
	p2([Invoke AI Model with Context])
	i1([Question Context])
	i2([Literature Summary])
	i1 --> prompt[[Prompt]]
	i2 --> prompt[[Prompt]]
	prompt --> p2
end

U -->|Ask Questions| p

p -->|get context| VDB[("Vector Database (Pinecone)")]
VDB --> i1


p -->|get summary| DB[("Google Sheet")]
DB --> i2

p2 --> user(((user)))

```