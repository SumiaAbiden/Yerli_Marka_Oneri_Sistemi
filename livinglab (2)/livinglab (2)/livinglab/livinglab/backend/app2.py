# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from transformers import pipeline
# import csv
# import random
# 
# app = Flask(__name__)
# CORS(app)
# 
# # Hugging Face zero-shot classification pipeline
# classifier = pipeline(
#     "zero-shot-classification",
#     model="joeddav/xlm-roberta-large-xnli",
#     tokenizer="joeddav/xlm-roberta-large-xnli"
# )
# 
# # Main categories
# category_labels = ["gıda", "elektronik", "otomotiv", "temizlik"]
# 
# # Subcategories
# alt_category_labels = {
#     "gıda": ["İçecek",  'Atıştırmalık', "Yağ",  "Kahvaltılık", 'Yoğurt', 'Et', "Diğer Gıda"],
#     "elektronik": ["Beyaz Eşya", "Televizyon", "Ses Sistemi / Kulaklık", "Küçük Ev Aletleri",
#                    "Küçük Mutfak Aletleri", "Klima", "Diğer Elektronik"],
#     "temizlik": ["Çamaşır Temizliği", "Kişisel Temizlik", 'Banyo Temizliği', "Oda Kokusu", "Bulaşık Temizliği",
#                  "Yüzey Temizliği", 'Makine Temizleyici', 'Mutfak', 'Temizlik bezi/Süngeri/Paspas',
#                  'Genel Temizlik', "Diğer Temizlik"],
#     "otomotiv": ["Otomotiv / Savunma"]
# }
# 
# alt_category_labels2 = {
#     "İçecek" : ["Süt", "Su", "Sıcak İçecek", "Soğuk İçecek"],
#     "Atıştırmalık": ["Çikolata", "Kraker", "Bisküvi", "Kek", "Dondurma", "Şekerleme"]
# }
# 
# alt_category_labels3 = {
#     "Soğuk İçecek" : ["Meyve Suyu", 'Soğuk çay', "Soda", 'Enerji İçeceği', "Gazlı İçecek"],
#     "Sıcak İçecek": ["Kahve", "Çay"]
# }
# 
# 
# 
# 
# # Load product data
# def load_data(filename="scraped_data_with_subcategories.csv"):
#     product_data = []
#     with open(filename, mode="r", encoding="utf-8") as file:
#         reader = csv.reader(file)
#         next(reader)  # Skip header
#         for row in reader:
#             product_data.append((row[0], row[1], row[2], row[3]))  # name, brand, category, subcategory
#     return product_data
# 
# 
# product_data = load_data()
# 
# 
# 
# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# 
# def send_email(subject, body, to_email):
#     sender_email = "yerlikesif@gmail.com"
#     app_password = "hmrb bbzs qrrp nlxo"  # Google’dan aldığın uygulama şifresi
# 
#     msg = MIMEMultipart() #MIME çok parçalı mesaj
#     msg["From"] = sender_email
#     msg["To"] = to_email
#     msg["Subject"] = subject
#     msg.attach(MIMEText(body, "plain")) #plain:HTML değil
# 
#     with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:  #465: SMTP protokolü için güvenli (şifreli) bağlantı kurulan port numarasıdır.
#         server.login(sender_email, app_password)
#         server.sendmail(sender_email, to_email, msg.as_string())
# 
# 
# @app.route('/contact', methods=['POST'])
# def contact():
#     try:
#         data = request.get_json()
# 
#         name = data.get("name")
#         email = data.get("email")
#         phone = data.get("phone")
#         subject = data.get("subject")
#         message = data.get("message")
# 
#         # Veriyi terminalde göster (test için)
#         print(f"İletişim mesajı:\nAd: {name}\nEmail: {email}\nTelefon: {phone}\nKonu: {subject}\nMesaj: {message}")
# 
#         # CSV’ye kaydetmek
#         with open("contact_messages.csv", "a", newline="", encoding="utf-8") as file:  #a: append: sonuna ekle olanlara dokunma
#             writer = csv.writer(file)
#             writer.writerow([name, email, phone, subject, message])
# 
#         full_message = (
#             f"İsim: {name}\n"
#             f"Email: {email}\n"
#             f"Telefon: {phone}\n"
#             f"Konu: {subject}\n\n"
#             f"Mesaj:\n{message}"
#         )
#         send_email(subject=f"Yeni İletişim: {subject}",
#                    body=full_message,
#                    to_email="yerlikesif@gmail.com")
#         return jsonify({"message": "Mesaj başarıyla gönderildi ve e‑posta yollandı!"}), 200
# 
#     except Exception as e:
#         print("Hata:", e)
#         return jsonify({"error": "Bir hata oluştu."}), 500
# 
# 
# 
# 
# @app.route('/process', methods=['POST'])
# def process():
#     try:
#         user_input = request.json.get('input', '').strip()
#         if not user_input:
#             return jsonify({"message": "Lütfen geçerli bir girdi sağlayın."}), 400
# 
#         # Predict main category
#         category_result = classifier(user_input, category_labels)
#         top_category = category_result["labels"][0].lower()
# 
#         # Predict subcategory
#         alt_labels = alt_category_labels.get(top_category, [])
#         alt_category_result = classifier(user_input, alt_labels)
#         top_alt_category = alt_category_result["labels"][0]
# 
#         # Alt kategori 2 ve 3 için ortak değişken kullan
#         current_subcategory = top_alt_category
# 
#         # İkinci seviye alt kategori
#         if current_subcategory in alt_category_labels2:
#             sub_labels2 = alt_category_labels2[current_subcategory]
#             if sub_labels2:  # Liste boş mu kontrol et
#                 sub_category_result2 = classifier(user_input, sub_labels2)
#                 current_subcategory = sub_category_result2["labels"][0]
# 
#         # Üçüncü seviye alt kategori
#         if current_subcategory in alt_category_labels3:
#             sub_labels3 = alt_category_labels3[current_subcategory]
#             if sub_labels3:
#                 sub_category_result3 = classifier(user_input, sub_labels3)
#                 current_subcategory = sub_category_result3["labels"][0]
# 
#         top_alt_category = current_subcategory  # En son kategoriyi güncelle
# 
# 
#         # Filter matching products
#         matched = [
#             {"product": p[0], "brand": p[1], "subcategory": p[3]}
#             for p in product_data
#             if top_category in p[2].lower() and top_alt_category in p[3]
#         ]
# 
#         random.shuffle(matched)
#         unique_products = list({item["product"] for item in matched[:10]})
# 
#         if unique_products:
#             message = (
#                 f"En iyi kategori: {top_category.capitalize()}\n"
#                 f"Alt kategori: {top_alt_category}\n"
#             )
#         else:
#             message = (
#                 f"En iyi kategori: {top_category.capitalize()} - Alt kategori: {top_alt_category}.\n"
#                 "Bu kategoriye uygun ürün bulunamadı."
#             )
# 
#         return jsonify({
#             "message": message,
#             "products": unique_products,
#             "category": top_category.capitalize(),
#             "subcategory": top_alt_category
#         })
# 
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500
# 
# 
# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import pipeline
from functools import lru_cache
import csv, random, re

app = Flask(__name__)
CORS(app)

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^\w\sçğıöşü]', '', text)
    return text.strip()

# Zero-shot classification with Turkish prompt support
classifier = pipeline(
    "zero-shot-classification",
    model="joeddav/xlm-roberta-large-xnli",
    tokenizer="joeddav/xlm-roberta-large-xnli",
    hypothesis_template="Bu ürün {} kategorisine ait olabilir mi?"
)

@lru_cache(maxsize=128)
def classify_with_cache(text, labels_tuple):
    return classifier(text, list(labels_tuple))

# Categories (same as your original)
category_labels = ["gıda", "elektronik", "otomotiv", "temizlik"]
alt_category_labels = {
    "gıda": ["İçecek", "Atıştırmalık", "Yağ", "Kahvaltılık", "Yoğurt", "Et", "Diğer Gıda"],
    "elektronik": ["Beyaz Eşya", "Televizyon", "Ses Sistemi / Kulaklık", "Küçük Ev Aletleri", "Küçük Mutfak Aletleri", "Klima", "Diğer Elektronik"],
    "temizlik": ["Çamaşır Temizliği", "Kişisel Temizlik", "Banyo Temizliği", "Oda Kokusu", "Bulaşık Temizliği", "Yüzey Temizliği", "Makine Temizleyici", "Mutfak", "Temizlik bezi/Süngeri/Paspas", "Genel Temizlik", "Diğer Temizlik"],
    "otomotiv": ["Otomotiv / Savunma"]
}
alt_category_labels2 = {
    "İçecek": ["Süt", "Su", "Sıcak İçecek", "Soğuk İçecek"],
    "Atıştırmalık": ["Çikolata", "Kraker", "Bisküvi", "Kek", "Dondurma", "Şekerleme"]
}
alt_category_labels3 = {
    "Soğuk İçecek": ["Meyve Suyu", "Soğuk çay", "Soda", "Enerji İçeceği", "Gazlı İçecek"],
    "Sıcak İçecek": ["Kahve", "Çay"]
}

def load_data(filename="scraped_data_with_subcategories.csv"):
    product_data = []
    with open(filename, encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            product_data.append((row[0], row[1], row[2], row[3]))
    return product_data

product_data = load_data()

@app.route('/process', methods=['POST'])
def process():
    try:
        user_input = request.json.get('input', '').strip()
        if not user_input:
            return jsonify({"message": "Lütfen geçerli bir girdi sağlayın."}), 400

        user_input = clean_text(user_input)
        category_result = classify_with_cache(user_input, tuple(category_labels))
        top_category = category_result["labels"][0].lower()

        alt_labels = alt_category_labels.get(top_category, [])
        alt_category_result = classify_with_cache(user_input, tuple(alt_labels))
        current_subcategory = alt_category_result["labels"][0]

        if current_subcategory in alt_category_labels2:
            sub_labels2 = alt_category_labels2[current_subcategory]
            if sub_labels2:
                result2 = classify_with_cache(user_input, tuple(sub_labels2))
                current_subcategory = result2["labels"][0]

        if current_subcategory in alt_category_labels3:
            sub_labels3 = alt_category_labels3[current_subcategory]
            if sub_labels3:
                result3 = classify_with_cache(user_input, tuple(sub_labels3))
                current_subcategory = result3["labels"][0]

        top_alt_category = current_subcategory

        matched = [
            {"product": p[0], "brand": p[1], "subcategory": p[3]}
            for p in product_data
            if top_category in p[2].lower() and top_alt_category in p[3]
        ]
        random.shuffle(matched)
        unique_products = list({item["product"] for item in matched[:10]})

        message = f"En iyi kategori: {top_category.capitalize()}\nAlt kategori: {top_alt_category}" \
            if unique_products else f"{top_category.capitalize()} - {top_alt_category}: ürün bulunamadı."

        return jsonify({
            "message": message,
            "products": unique_products,
            "category": top_category.capitalize(),
            "subcategory": top_alt_category
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
