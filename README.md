<div id="top">

<!-- HEADER STYLE: CLASSIC -->
<div align="center">

<img src="readmeai/assets/logos/purple.svg" width="30%" style="position: relative; top: 0; right: 0;" alt="Project Logo"/>

# EASYESSAY.GIT

<em>Crafting effortless literary insights for your success.</em>

<!-- BADGES -->
<img src="https://img.shields.io/github/license/Wh4130/EasyEssay?style=default&logo=opensourceinitiative&logoColor=white&color=0080ff" alt="license">
<img src="https://img.shields.io/github/last-commit/Wh4130/EasyEssay?style=default&logo=git&logoColor=white&color=0080ff" alt="last-commit">
<img src="https://img.shields.io/github/languages/top/Wh4130/EasyEssay?style=default&color=0080ff" alt="repo-top-language">
<img src="https://img.shields.io/github/languages/count/Wh4130/EasyEssay?style=default&color=0080ff" alt="repo-language-count">

<!-- default option, no dependency badges. -->


<!-- default option, no dependency badges. -->

</div>
<br>

---

## Table of Contents

- [EASYESSAY.GIT](#easyessaygit)
	- [Table of Contents](#table-of-contents)
	- [Overview](#overview)
	- [Project Structure](#project-structure)
		- [Project Index](#project-index)
	- [Acknowledgments](#acknowledgments)

---

## Overview

**Why EasyEssay?**

This project transforms the literature review process by making academic research more accessible and interactive. The core features include:

- **📚 Streamlined Literature Review:** Accelerate your research process with organized literature management by tags and languages, making it easier to navigate and synthesize multiple sources.

- **🤖 RAG-Powered Interactive Literature Chat:** Engage directly with your literature through an intelligent chat interface. Ask questions, extract insights, and explore concepts within your documents using advanced RAG (Retrieval-Augmented Generation) technology that prevents AI hallucination.

- **⚡ Flexible AI Model Selection:** Choose from multiple Gemini models (2.5-flash, 2.0-flash, etc.) based on your needs, ensuring optimal performance and cost-effectiveness for your specific use case.

- **👤 Personalized Research Environment:** Maintain your own secure account with personalized literature collections, chat histories, and research progress tracking.

**Transform your literature review from a tedious process into an interactive, AI-enhanced research experience that helps you understand and synthesize academic content more effectively.**

---

## Project Structure

```sh
└── EasyEssay/
    ├── index.py
    ├── managers.py
    ├── pages
    │   ├── page_account.py
    │   ├── page_chat.py
    │   └── page_docs.py
    ├── pics
    │   └── icon.png
    ├── requirements.txt
    ├── test.py
    └── utils
        ├── constants.py
        ├── data_manager.py
        ├── docs_manager.py
        ├── llm_manager.py
        ├── others.py
        ├── prompt_manager.py
        ├── sheet_manager.py
        └── user_manager.py
```

### Project Index

<details open>
	<summary><b><code>EASYESSAY.GIT/</code></b></summary>
	<!-- __root__ Submodule -->
	<details>
		<summary><b>__root__</b></summary>
		<blockquote>
			<div class='directory-path' style='padding: 8px 0; color: #666;'>
				<code><b>⦿ __root__</b></code>
			<table style='width: 100%; border-collapse: collapse;'>
			<thead>
				<tr style='background-color: #f8f9fa;'>
					<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
					<th style='text-align: left; padding: 8px;'>Summary</th>
				</tr>
			</thead>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/Wh4130/EasyEssay.git/blob/master/index.py'>index.py</a></b></td>
					<td style='padding: 8px;'>- The <code>index.py</code> file in the project serves as the main entry point for the Easy Essay-Literature Summary Database tool<br>- It manages user sessions, data storage, and interaction with various utility modules for document summarization and management<br>- The file orchestrates the generation of literature summaries, handles user authentication, and provides a user-friendly interface for navigating different tool functionalities<br>- It plays a crucial role in the overall functionality and user experience of the application.</td>
				</tr>
			</table>
		</blockquote>
	</details>
	<!-- utils Submodule -->
	<details>
		<summary><b>utils</b></summary>
		<blockquote>
			<div class='directory-path' style='padding: 8px 0; color: #666;'>
				<code><b>⦿ utils</b></code>
			<table style='width: 100%; border-collapse: collapse;'>
			<thead>
				<tr style='background-color: #f8f9fa;'>
					<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
					<th style='text-align: left; padding: 8px;'>Summary</th>
				</tr>
			</thead>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/Wh4130/EasyEssay.git/blob/master/utils/sheet_manager.py'>sheet_manager.py</a></b></td>
					<td style='padding: 8px;'>- Manage Google Sheets interactions by authenticating, extracting, fetching, inserting, updating, and deleting rows<br>- Acquire and release locks to ensure data integrity during edits<br>- This utility class streamlines access and manipulation of Google Sheets within the projects architecture.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/Wh4130/EasyEssay.git/blob/master/utils/user_manager.py'>user_manager.py</a></b></td>
					<td style='padding: 8px;'>- Manage user authentication, registration, and account deletion<br>- Handle password hashing, verification, and user data interactions<br>- Utilize Google Sheets for user data storage and retrieval<br>- Ensure secure login and registration processes<br>- Provide functionality for users to delete their accounts securely.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/Wh4130/EasyEssay.git/blob/master/utils/prompt_manager.py'>prompt_manager.py</a></b></td>
					<td style='padding: 8px;'>- The <code>PromptManager</code> class in <code>utils/prompt_manager.py</code> generates detailed summaries and answers based on provided literature, ensuring strict adherence to source materials and user-friendly explanations<br>- It facilitates precise summarization in JSON format, highlighting keywords and source page numbers<br>- Additionally, it assists in answering questions with comprehensive explanations, specific examples, and technical content, all while maintaining factual accuracy and user-friendly language.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/Wh4130/EasyEssay.git/blob/master/utils/docs_manager.py'>docs_manager.py</a></b></td>
					<td style='padding: 8px;'>- Manage Pinecone indexes, insert and search documents using Pinecone embeddings and text splitting<br>- Integrates with RAG structure for contextual information retrieval<br>- List namespaces, create indexes, insert and search documents based on specified queries<br>- Ideal for retrieving similar documents based on provided text inputs.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/Wh4130/EasyEssay.git/blob/master/utils/llm_manager.py'>llm_manager.py</a></b></td>
					<td style='padding: 8px;'>- Define classes for summarization and chatbot functionalities using the GenAI API<br>- The <code>Summarizor</code> class handles text summarization based on a specified model, while the <code>ChatBot</code> class facilitates interactive conversations with configurable parameters<br>- These classes encapsulate logic for generating content and managing AI models seamlessly within the project architecture.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/Wh4130/EasyEssay.git/blob/master/utils/data_manager.py'>data_manager.py</a></b></td>
					<td style='padding: 8px;'>- The <code>data_manager.py</code> file orchestrates PDF handling, JSON parsing, image conversion, and chat history compilation within the project<br>- It facilitates PDF uploads, language selection, and tag categorization, ensuring efficient data processing and storage<br>- Additionally, it offers functions for loading PDF content, extracting JSON objects, converting images to Base64, generating random indices, and compiling chat histories into Excel format.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/Wh4130/EasyEssay.git/blob/master/utils/constants.py'>constants.py</a></b></td>
					<td style='padding: 8px;'>Define constant variables, such as gemini model list, for the project architecture.</td>
				</tr>
			</table>
		</blockquote>
	</details>
	<!-- pages Submodule -->
	<details>
		<summary><b>pages</b></summary>
		<blockquote>
			<div class='directory-path' style='padding: 8px 0; color: #666;'>
				<code><b>⦿ pages</b></code>
			<table style='width: 100%; border-collapse: collapse;'>
			<thead>
				<tr style='background-color: #f8f9fa;'>
					<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
					<th style='text-align: left; padding: 8px;'>Summary</th>
				</tr>
			</thead>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/Wh4130/EasyEssay.git/blob/master/pages/page_chat.py'>page_chat.py</a></b></td>
					<td style='padding: 8px;'>- Set up a chat interface for interacting with literature summaries<br>- It manages user sessions, document selection, and chat history<br>- Users can select documents, ask questions, and receive responses based on AI models and document summaries<br>- The file also handles system prompts, model selection, and chat history downloads</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/Wh4130/EasyEssay.git/blob/master/pages/page_docs.py'>page_docs.py</a></b></td>
					<td style='padding: 8px;'>- SummaryThe <code>page_docs.py</code> file in the project serves as a central component for managing and displaying documentation related to the EasyEssay literature summary generator application<br>- It leverages Streamlit to create an interactive and user-friendly interface for users to access and interact with various documents and summaries<br>- The file integrates with different utility modules such as data management, summarization, prompts, and user management to provide a seamless experience<br>- Additionally, it includes configuration settings for the page layout and menu items, enhancing the overall usability of the application.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/Wh4130/EasyEssay.git/blob/master/pages/page_account.py'>page_account.py</a></b></td>
					<td style='padding: 8px;'>- The code in <code>pages/page_account.py</code> manages user authentication and account settings within the Easy Essay Literature Review Tool<br>- It handles user login, registration, account information display, and logout functionalities<br>- Additionally, it ensures a seamless user experience by maintaining session state and providing access to various tool features based on user authentication status.</td>
				</tr>
			</table>
		</blockquote>
	</details>
</details>

---
<!-- 
## Getting Started

### Prerequisites

This project requires the following dependencies:

- **Programming Language:** Python
- **Package Manager:** Pip

### Installation

Build EasyEssay.git from the source and intsall dependencies:

1. **Clone the repository:**

    ```sh
    ❯ git clone https://github.com/Wh4130/EasyEssay.git
    ```

2. **Navigate to the project directory:**

    ```sh
    ❯ cd EasyEssay.git
    ```

3. **Install the dependencies:**

SHIELDS BADGE CURRENTLY DISABLED
	[![pip][pip-shield]][pip-link]
	REFERENCE LINKS
	[pip-shield]: https://img.shields.io/badge/Pip-3776AB.svg?style={badge_style}&logo=pypi&logoColor=white
	[pip-link]: https://pypi.org/project/pip/

	**Using [pip](https://pypi.org/project/pip/):**

	```sh
	❯ pip install -r requirements.txt
	```

### Usage

Run the project with:

**Using [pip](https://pypi.org/project/pip/):**
```sh
python {entrypoint}
```

### Testing

Easyessay.git uses the {__test_framework__} test framework. Run the test suite with:

**Using [pip](https://pypi.org/project/pip/):**
```sh
pytest
``` -->

<!-- ---

## Roadmap

- [X] **`Task 1`**: <strike>Implement feature one.</strike>
- [ ] **`Task 2`**: Implement feature two.
- [ ] **`Task 3`**: Implement feature three.

---

## Contributing

- **💬 [Join the Discussions](https://github.com/Wh4130/EasyEssay.git/discussions)**: Share your insights, provide feedback, or ask questions.
- **🐛 [Report Issues](https://github.com/Wh4130/EasyEssay.git/issues)**: Submit bugs found or log feature requests for the `EasyEssay.git` project.
- **💡 [Submit Pull Requests](https://github.com/Wh4130/EasyEssay.git/blob/main/CONTRIBUTING.md)**: Review open PRs, and submit your own PRs.

<details closed>
<summary>Contributing Guidelines</summary>

1. **Fork the Repository**: Start by forking the project repository to your github account.
2. **Clone Locally**: Clone the forked repository to your local machine using a git client.
   ```sh
   git clone https://github.com/Wh4130/EasyEssay.git
   ```
3. **Create a New Branch**: Always work on a new branch, giving it a descriptive name.
   ```sh
   git checkout -b new-feature-x
   ```
4. **Make Your Changes**: Develop and test your changes locally.
5. **Commit Your Changes**: Commit with a clear message describing your updates.
   ```sh
   git commit -m 'Implemented new feature x.'
   ```
6. **Push to github**: Push the changes to your forked repository.
   ```sh
   git push origin new-feature-x
   ```
7. **Submit a Pull Request**: Create a PR against the original project repository. Clearly describe the changes and their motivations.
8. **Review**: Once your PR is reviewed and approved, it will be merged into the main branch. Congratulations on your contribution!
</details>

<details closed>
<summary>Contributor Graph</summary>
<br>
<p align="left">
   <a href="https://github.com{/Wh4130/EasyEssay.git/}graphs/contributors">
      <img src="https://contrib.rocks/image?repo=Wh4130/EasyEssay.git">
   </a>
</p>
</details>

---

## License

Easyessay.git is protected under the [LICENSE](https://choosealicense.com/licenses) License. For more details, refer to the [LICENSE](https://choosealicense.com/licenses/) file.

--- -->

## Acknowledgments

- Credit `contributors`, `inspiration`, `references`, etc.

<div align="right">

[![][back-to-top]](#top)

</div>


[back-to-top]: https://img.shields.io/badge/-BACK_TO_TOP-151515?style=flat-square


---
