import os
import json
import streamlit as st
from dotenv import load_dotenv

print("✅ [config] Başlatılıyor...")

# .env varsa localde yükle
load_dotenv()

# GCP servis hesabı dosyasını secrets içinden al
key_path = "/tmp/gcp_key.json"
if "gcp_service_account" in st.secrets:
    print("🔐 [config] GCP servis hesabı bulundu, dosya yazılıyor...")
    with open(key_path, "w") as f:
        json.dump(dict(st.secrets["gcp_service_account"]), f)
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = key_path
    print(f"✅ [config] GOOGLE_APPLICATION_CREDENTIALS ayarlandı: {key_path}")
else:
    print("⚠️ [config] GCP service account bulunamadı.")

# Diğer environment key'leri ayarla
for key in ["PINECONE_API_KEY", "PINECONE_ENV", "VERTEX_PROJECT_ID", "VERTEX_REGION"]:
    if key in st.secrets:
        os.environ[key] = st.secrets[key]
        print(f"✅ [config] {key} ayarlandı.")
    else:
        print(f"⚠️ [config] {key} eksik.")

# Python değişkeni olarak erişilebilir hale getir
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENV = os.getenv("PINECONE_ENV", "us-east-1")
PROJECT_ID = os.getenv("VERTEX_PROJECT_ID")
REGION = os.getenv("VERTEX_REGION", "us-central1")


