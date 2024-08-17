# CYNCLAIR-Chat-AI

1. To install requirements
```
pip install -r requirements.txt
```

2. Create a file name ".env" in the folder "/scripts". The file content:
```
OPENAI_API_KEY = "sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
HUGGINGFACEHUB_API_TOKEN = "hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```
You need to use your own API key.


3. To run the server
```
streamlit run .\scripts\app.py
```