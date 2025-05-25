import os
from dotenv import load_dotenv
import streamlit as st
import json

load_dotenv()

key_path = "/tmp/gcp_key.json"

with open(key_path, "w") as f:
    json.dump(dict(st.secrets["gcp_service_account"]), f)

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = key_path


os.environ["PINECONE_API_KEY"] = st.secrets["PINECONE_API_KEY"]
os.environ["PINECONE_ENV"] = st.secrets["PINECONE_ENV"]
os.environ["VERTEX_PROJECT_ID"] = st.secrets["VERTEX_PROJECT_ID"]
os.environ["VERTEX_REGION"] = st.secrets["VERTEX_REGION"]


PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENV = os.getenv("PINECONE_ENV", "us-east-1")
PROJECT_ID = os.getenv("VERTEX_PROJECT_ID")
REGION = os.getenv("VERTEX_REGION", "us-central1")
