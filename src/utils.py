### Base class to instance llm chain from prompt (cf __init__). Other classes will inherit this one.

import os
from langchain.document_loaders import PyPDFLoader
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain

class BaseStructureChain:

    PROMPT = ""

    def __init__(self):
        self.llm = ChatOpenAI()
        self.chain = LLMChain.from_string(
            llm=self.llm,
            template=self.PROMPT
        )
        self.chain.verbose = True # can't pass it directly inside the from_string method