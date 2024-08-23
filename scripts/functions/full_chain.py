import os

from dotenv import load_dotenv
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate

from functions.basic_chain import get_model
from functions.ensemble import ensemble_retriever_from_docs
from functions.loader import load_md_files
from functions.memory import create_memory_chain
from functions.rag_chain import make_rag_chain


def create_full_chain(retriever, openai_api_key=None, chat_memory=ChatMessageHistory(), mode="CVEbot"):
    model = get_model("ChatGPT", openai_api_key=openai_api_key)
    
    if mode == "CVEbot":
        system_prompt = """You are a helpful AI assistant for busy Cybersecurity professionals trying to find the problem in their softwares. 
        You are provided CVEs ID and details to answer users question about their related or similar problem.
        Use the following context and the users' chat history to help the user:
        If you don't know the answer, just say that there is no relevant information in the database. 
        
        Context: {context}
        
        Question: """

    elif mode == "Reportbot":
        system_prompt = """You are a helpful AI assistant for busy Cybersecurity professionals trying to write a report outline. 
        You are provided the conversation between the user and AI to make a cybersecurity report outline. 
        You are required to answer in this template:

        Incident Details:

        Type of Incident: 
        
        Description of Incident: 
        
        Affected Systems or Data:
        
        Potential Impact:
        
        Evidence and Logs:
        
        Actions Taken:
        
        Security Improvements: 
        
        Lessons Learned:
        
        
        Here is the Context: {context}
        
        Question: """


    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", "{question}"),
        ]
    )
    
    rag_chain = make_rag_chain(model, retriever, rag_prompt=prompt)
    chain = create_memory_chain(model, rag_chain, chat_memory)
    return chain


def ask_question(chain, query):
    response = chain.invoke(
        {"question": query},
        config={"configurable": {"session_id": "foo"}}
    )
    return response


def main():
    load_dotenv()

    from rich.console import Console
    from rich.markdown import Markdown
    console = Console()

    docs = load_md_files()
    ensemble_retriever = ensemble_retriever_from_docs(docs)
    chain = create_full_chain(ensemble_retriever)

    queries = [
        "What is a CVE and how it is used in the Cybersecurity?"
    ]

    for query in queries:
        response = ask_question(chain, query)
        console.print(Markdown(response.content))

if __name__ == '__main__':
    # this is to quiet parallel tokenizers warning.
    os.environ["TOKENIZERS_PARALLELISM"] = "false"
    main()