import json
import os
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, 'utils','data', 'real_estate_faq.json')
print("Looking for JSON at:", DATA_PATH)
try:
   with open(DATA_PATH, 'r') as f:
    faq_data = json.load(f)
except FileNotFoundError as e:
 print(" JSON file not found at:", DATA_PATH)
 raise e    


model_name = "google/flan-t5-small"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)


vectorizer = TfidfVectorizer().fit([item["question"] for item in faq_data])
faq_vectors = vectorizer.transform([item["question"] for item in faq_data])

def get_best_match(question):
    user_vec = vectorizer.transform([question])
    similarity = cosine_similarity(user_vec, faq_vectors)
    idx = similarity.argmax()
    return faq_data[idx]["question"], faq_data[idx]["answer"]

def generate_response(user_question):
    matched_q, matched_a = get_best_match(user_question)
    prompt = f"Answer based only on this information:\nQ: {matched_q}\nA: {matched_a}\n Q: {user_question}\nA:"
    inputs = tokenizer(prompt, return_tensors="pt")
    output = model.generate(**inputs, max_length=100)
    answer = tokenizer.decode(output[0], skip_special_tokens=True)
    return answer.strip()