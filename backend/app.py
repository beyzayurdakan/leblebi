from . import config  # config.py içindeki loglar da çalışır
from langchain_google_vertexai import VertexAI
from .rag_pipeline import augment_prompt, load_preprocess_prompt, format_chat_history
import json
import re
from html import unescape

def get_llm_model():
    print("🧠 [app] VertexAI modeli başlatılıyor...")
    return VertexAI(
        model_name="gemini-2.0-flash-001",
        temperature=0.2,
        max_output_tokens=1024
    )

def clean_llm_output_full(raw_text: str):
    print("🧪 [app] clean_llm_output_full çağrıldı")
    try:
        if raw_text.strip().startswith("```"):
            raw_text = "\n".join(
                line for line in raw_text.splitlines() if not line.strip().startswith("```")
            )
        text = re.sub(r"<br\s*/?>", "\n", raw_text)
        text = re.sub(r"<.*?>", "", text)
        parsed = json.loads(unescape(text).strip())
        print("✅ [app] JSON parse başarılı")
        return parsed
    except Exception as e:
        print(f"❌ [app] JSON parse hatası: {e}")
        return {"error": "parse_error", "raw": raw_text[:200]}

def ask(query: str, chat_history=None) -> tuple:
    print("🟡 [app] ask() fonksiyonu başladı")
    preprocess_prompt_template = load_preprocess_prompt()
    preprocess_prompt = preprocess_prompt_template.replace("{{query}}", query)

    if chat_history and len(chat_history) > 0:
        history_text = format_chat_history(chat_history)
        preprocess_prompt = preprocess_prompt.replace("{{chat_history}}", history_text)
    else:
        preprocess_prompt = preprocess_prompt.replace("{{chat_history}}", "No previous conversation.")

    print("📨 [app] Preprocess prompt oluşturuldu, LLM çağrılıyor...")
    preprocessed_output = get_llm_model().invoke(preprocess_prompt)
    print("📬 [app] Preprocess yanıtı alındı")
    preprocessed_query = clean_llm_output_full(preprocessed_output)

    print("📦 [app] Augmented prompt hazırlanıyor...")
    augmented_prompt = augment_prompt(preprocessed_query, chat_history)

    print("🤖 [app] Final LLM çağrısı yapılıyor...")
    final_output = get_llm_model().invoke(augmented_prompt)

    print("✅ [app] ask() tamamlandı")
    return final_output.strip(), preprocessed_query
