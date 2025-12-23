import streamlit as st
import pandas as pd
import time
from dotenv import dotenv_values
import json
import requests
import base64
import re 
import google.generativeai as genai
import datetime as dt
import random
import string
import json 
import os
import numpy as np
from utils.prompt_manager import PromptManager
from utils.docs_manager import PineconeManager
from litellm import completion
import litellm

litellm._turn_on_debug()

try: 
    os.environ["CEREBRAS_API_KEY"] = dotenv_values('.env')['CEREBRAS_API_KEY']
except:
    os.environ["CEREBRAS_API_KEY"] = st.secrets['credits']['CEREBRAS_API_KEY']




class Summarizor():
    """
    ! Depreciated, now document summarization is handled in another backend service.
    """

    def __init__(self, model_key = "gemini-2.5-flash", thinking_budget = 0, language = 'English', other_instruction = None):
        self.client = genai.Client(api_key = GEMINI_KEY)
        self.model_key = model_key
        self.system_prompt = PromptManager.summarize(lang = language, other_prompt = other_instruction)
        self.thinking_budget = thinking_budget
        self.config = types.GenerateContentConfig(
            system_instruction = self.system_prompt,
            max_output_tokens= 40000,
            top_k= 2,
            top_p= 0.5,
            temperature= 0,
            thinking_config = types.ThinkingConfig(thinking_budget=thinking_budget)
        )
        
    def changeModel(self, new_model_key):
        self.model_key = new_model_key
        
    def changeThinkingBudget(self, new_thinking_budget):
        self.thinking_budget = new_thinking_budget
        self.config = types.GenerateContentConfig(
            system_instruction = self.system_prompt,
            max_output_tokens= 40000,
            top_k= 2,
            top_p= 0.5,
            temperature= 0,
            thinking_config = types.ThinkingConfig(thinking_budget=self.thinking_budget)
        )
        
    
    def apiCall(self, in_message):

        return self.client.models.generate_content(
            model    = self.model_key,
            contents = in_message,
            config   = self.config
        ).text
    
    @staticmethod
    def find_json_object(input_string):
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
        return None
    
class ChatBot():

    def __init__(self, 
                 model_key = "gpt-oss-120b", 
                 temperature = 0,
                 RAG = True):
        
        self.pc              = PineconeManager()
        self.model_key       = model_key
        self.RAG             = RAG
        self.temperature     = temperature

    def _clean_content(self, text):
        """清洗層：移除 HTML 與特殊字元"""
        if not text: return ""
        # 1. 移除 HTML 標籤
        text = re.sub(r'<[^>]+>', '', text)
        # 2. 移除 BOM 和特殊 Unicode 空格
        text = text.replace('\ufeff', '').replace('\u202f', ' ').replace('\u00a0', ' ')
        # 3. 只保留可列印字元 (移除奇怪的控制字元)
        text = "".join(ch for ch in text if ch.isprintable() or ch == '\n')
        return text.strip()

    def changeTemperature(self, new_temperature):
        self.temperature = new_temperature


    def checkRagAvailability(self, doc_id):
        all_docIDs = self.pc.list_namespaces("easyessay")
        if doc_id not in all_docIDs:
            return False 
        else:
            return True
        
    def changeModel(self, new_model_key):
        self.model_key = new_model_key

    def apiCall(self, in_messages, similar_text_ls, doc_summary = None, additional_prompt = None):
        
        instruction = PromptManager.chat_rag(doc_summary, similar_text_ls)

        if additional_prompt:
            instruction += "\n\n" + additional_prompt

        instruction = self._clean_content(instruction)
        msgs = [
            {"role": "system", "content": instruction},
            *in_messages[-1:]
        ]


        # * Call API
        full_model_name = f"cerebras/{self.model_key}"
        response_stream = completion(
            model=full_model_name,
            messages=msgs,
            max_tokens=40000,
            stream = True,
            temperature=self.temperature,
            top_p=1
        )

        # # * Get Response
        for part in response_stream:

            content = part.choices[0].delta.content
            
            # * the last element in the stream may be None
            if content is not None:
                yield content

