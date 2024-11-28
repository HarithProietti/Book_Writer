### This file is responsible for creating the description of the main character

import os
from langchain.document_loaders import PyPDFLoader
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain

class MainCharacterChain:

    PROMPT = """
    You are provided with the wikipedia page of a famous person. Please generate a concise summary of the person's profile (5-6 sentences maximum).
    Don't forget to include the person's name inside the summary.

    Person's profile: {text}

    Profile summary: """

    def __init__(self):
        self.llm = ChatOpenAI()
        self.chain = LLMChain.from_string(
            llm=self.llm,
            template=self.PROMPT
        )
        self.chain.verbose = True # can't pass it directly inside the from_string method

    def load_character_description(self, file_name):
        folder = './docs'
        file_path = os.path.join(folder, file_name)
        loader = PyPDFLoader(file_path)
        docs = loader.load_and_split()  # contains the list of pages extracted from the file name
        return docs
    
    def run(self, file_name):
        # load the resume
        # generate a summary
        docs = self.load_character_description(file_name)
        description = '\n\n'.join([doc.page_content for doc in docs])
        return self.chain.run(description)