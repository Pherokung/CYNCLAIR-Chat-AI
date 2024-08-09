import json
import os
from dotenv import load_dotenv
from langchain_openai import OpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate


# Specify the directory path
directory_path = 'CVE_Database\CVE_JSON'
target_path = 'CVE_Database\CVE_MD'
file_list = os.listdir(directory_path)

# Load API keys
load_dotenv()

def set_up_LLMs():
    llm = OpenAI(temperature=0.2)
    prompt = ChatPromptTemplate.from_messages(
        [("user", "Convert the given JSON object into an unstructured, readable single paragraph within 1000 characters. Always show its CVE_ID first. JSON: {JSON_file}")],
    )
    chain = prompt | llm | StrOutputParser()
    
    convert_files(chain)


def convert_files(chain):
    
    for file_name in file_list:
        source_file_path = os.path.join(directory_path, file_name)
    
        new_file_name = file_name.split('.')[0] + ".md"
        target_file_path = os.path.join(target_path, new_file_name)

        # Load JSON data from file
        with open(source_file_path, 'r') as file:
            data = json.load(file)

        markdown_content = chain.invoke({'JSON_file':data})

        # Write Markdown content to file
        with open(target_file_path, 'w') as file:
            file.write(markdown_content)

        print("Markdown file generated successfully!")
        

if __name__ == "__main__":
    set_up_LLMs()