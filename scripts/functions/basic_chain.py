import os

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_community.llms import HuggingFaceHub
from langchain_community.chat_models.huggingface import ChatHuggingFace

from dotenv import load_dotenv

MISTRAL = "mistralai/Mistral-7B-Instruct-v0.1"
ZEPHYR = "HuggingFaceH4/zephyr-7b-beta"
CHATGPT = "ChatGPT"

def get_model(model_ID=CHATGPT, **kwargs):
    if model_ID == CHATGPT:
        chat_model = ChatOpenAI(model="gpt-4o", temperature=0.3, **kwargs)
    else:
        huggingfacehub_api_token = kwargs.get("HUGGINGFACEHUB_API_TOKEN", None)
        if not huggingfacehub_api_token:
            huggingfacehub_api_token = os.environ.get("HUGGINGFACEHUB_API_TOKEN", None)
        os.environ["HF_TOKEN"] = huggingfacehub_api_token
        
        llm = HuggingFaceHub(
            repo_id=model_ID,
            task="text-generation",
            model_kwargs={
                "max_new_tokens": 512,
                "top_k": 30,
                "temperature": 0.1,
                "repetition_penalty": 1.03,
                "huggingfacehub_api_token": huggingfacehub_api_token,
            })
        chat_model = ChatHuggingFace(llm=llm)
    return chat_model


def basic_chain(model=None, prompt=None):
    if not model:
        model = get_model(ZEPHYR)
    if not prompt:
        prompt = ChatPromptTemplate.from_template("Tell me the most noteworthy books by the author {author}")

    chain = prompt | model
    return chain


def main():
    load_dotenv()

    prompt = ChatPromptTemplate.from_template("Tell me the most noteworthy books by the author {author}")
    chain = basic_chain(prompt=prompt) | StrOutputParser()

    results = chain.invoke({"author": "William Faulkner"})
    print(results)


if __name__ == '__main__':
    main()