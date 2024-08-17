import json
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate


# Specify the directory path
directory_path = 'scripts\CVE_Database\CVE_JSON'
target_path = 'scripts\CVE_Database\CVE_MD'
file_list = os.listdir(directory_path)

# Load API keys
load_dotenv()

def set_up_LLMs():
    llm = ChatOpenAI(temperature=0)
    prompt = ChatPromptTemplate.from_messages(
        [("user", "You are an assistant that describes JSON objects in English. The results must not exceed 1000 characters and does not include any URL or links. \
          when you receive json input, I want you to describe it in the format below. This is THE TEMPLATE:\
            CVE ID: [cveId]\
            Title: [title]\
            Published Date: [datePublished]\
            Last Updated: [dateUpdated]\
            Affected Product: [affected.Product]\
            Metrics and Score Level: [metrics]\
            Credit: [credits]\
            Description: [descriptions]\
            Here is the JSON object I want to be converted: {JSON_file}")],
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