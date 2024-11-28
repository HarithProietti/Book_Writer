### Base class to instance llm chain from prompt (cf __init__). Other classes will inherit this one.

import os
from langchain.document_loaders import PyPDFLoader
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain

# This class is created for overall content like main plot, character's description, chapter's plots as it has a relatively low context window (4k).
# For more detailed events (actual paragraphs and chapters content), we will use 
class BaseStructureChain:

    PROMPT = ""

    def __init__(self):
        self.llm = ChatOpenAI()
        self.chain = LLMChain.from_string(
            llm=self.llm,
            template=self.PROMPT
        )
        self.chain.verbose = True # can't pass it directly inside the from_string method


# This class is used when we want very detailed prompts and examples (especially for the actual content of stories/chapters), as we will use a model with more context window (16k vs 4k for the default model)
class BaseEventChain:

    PROMPT = ""

    def __init__(self):
        self.llm = ChatOpenAI(model_name='gpt-3.5-turbo-16k')
        self.chain = LLMChain.from_string(
            llm=self.llm,
            template=self.PROMPT
        )
        self.chain.verbose = True # can't pass it directly inside the from_string method