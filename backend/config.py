import os
import json
import streamlit as st

print("✅ [config] Başladı")

key_path = "/tmp/gcp_key.json"

if "gcp_service_account" in st.secrets:
    print("🔑 [config] GCP servis hesabı bulundu, dosya yazılıyor...")
    with open(key_path, "w") as f:
        json.dump(dict(st.secrets["gcp_service_account"]), f)
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = key_path
    print(f"📄 [config] GOOGLE_APPLICATION_CREDENTIALS ayarlandı: {key_path}")
else:
    print("⚠️ [config] st.secrets içinde gcp_service_account bulunamadı")

# Diğer env değişkenlerini de ayarlayalım
for key in ["PINECONE_API_KEY", "PINECONE_ENV", "VERTEX_PROJECT_ID", "VERTEX_REGION"]:
    if key in st.secrets:
        os.environ[key] = st.secrets[key]
        print(f"✅ [config] {key} yüklendi.")
    else:
        print(f"⚠️ [config] st.secrets içinde {key} eksik.")
