# Flask kütüphanesinden gerekli modüller içe aktarılıyor
from flask import Flask, request, jsonify

# CORS (Cross-Origin Resource Sharing) desteği ekleniyor
from flask_cors import CORS

# Hugging Face transformers kütüphanesinden pipeline fonksiyonu içe aktarılıyor
from transformers import pipeline

# CSV dosyalarıyla çalışmak için
import csv

# Liste elemanlarını karıştırmak için
import random

# Flask uygulaması başlatılıyor
app = Flask(__name__)

# CORS desteği ekleniyor (frontend ile backend arasında veri paylaşımına izin verir)
CORS(app)

# Zero-shot classification modeli tanımlanıyor
classifier = pipeline(
    "zero-shot-classification",  # Görev türü
    model="joeddav/xlm-roberta-large-xnli",  # Kullanılan transformer modeli
    tokenizer="joeddav/xlm-roberta-large-xnli"  # Aynı modelin tokenizer’ı
)

# Ana kategoriler (ilk sınıflandırmada kullanılacak)
category_labels = ["gıda", "elektronik", "otomotiv", "temizlik"]

# Subcategories
alt_category_labels = {
    "gıda": ["İçecek",  'Atıştırmalık', "Yağ",  "Kahvaltılık", 'Yoğurt', 'Et', "Diğer Gıda"],
    "elektronik": ["Beyaz Eşya", "Televizyon", "Ses Sistemi / Kulaklık", "Küçük Ev Aletleri", "Fritöz", "Blender",
                   "Küçük Mutfak Aletleri", "Klima","Çamaşır Makinesi", "Bulaşık Makinesi", "buzdolabı" "Diğer Elektronik"],
    "temizlik": ["Çamaşır Temizliği", "Kişisel Temizlik", 'Banyo Temizliği', "Oda Kokusu", "Bulaşık Temizliği",
                 "Yüzey Temizliği", 'Makine Temizleyici', 'Mutfak', 'Temizlik bezi/Süngeri/Paspas',
                 'Genel Temizlik', "Diğer Temizlik"],
    "otomotiv": ["Otomotiv / Savunma"]
}

alt_category_labels2 = {
    "İçecek" : ["Süt", "Su", "Sıcak İçecek", "Soğuk İçecek"],
    "Atıştırmalık": ["Çikolata", "Kraker", "Bisküvi", "Kek", "Dondurma", "Şekerleme"]
}

alt_category_labels3 = {
    "Soğuk İçecek" : ["Meyve Suyu", 'Soğuk çay', "Soda", 'Enerji İçeceği', "Gazlı İçecek"],
    "Sıcak İçecek": ["Kahve", "Çay"]
}

# Ürün verilerini CSV dosyasından okur
def load_data(filename="scraped_data_with_subcategories.csv"):
    product_data = []
    with open(filename, mode="r", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader)  # Başlık satırını atla
        for row in reader:
            product_data.append((row[0], row[1], row[2], row[3]))  # Ürün İsmi, Marka, Ana Kategori, Alt Kategori
    return product_data

# Veriler yükleniyor
product_data = load_data()

# E-posta gönderimi için gerekli modüller
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# E-posta gönderme fonksiyonu
def send_email(subject, body, to_email):
    sender_email = "yerlikesif@gmail.com"  # Gönderen e-posta
    app_password = "hmrb bbzs qrrp nlxo"  # Google uygulama şifresi

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    # SMTP ile gönderim
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, app_password)
        server.sendmail(sender_email, to_email, msg.as_string())

# İletişim formundan gelen verileri işler
@app.route('/contact', methods=['POST'])
def contact():
    try:
        data = request.get_json()  # JSON verisini al

        # Form alanlarını ayıkla
        name = data.get("name")
        email = data.get("email")
        phone = data.get("phone")
        subject = data.get("subject")
        message = data.get("message")

        # Konsola yazdır
        print(f"İletişim mesajı:\nAd: {name}\nEmail: {email}\nTelefon: {phone}\nKonu: {subject}\nMesaj: {message}")

        # CSV dosyasına yaz
        with open("contact_messages.csv", "a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([name, email, phone, subject, message])

        # E-posta gönder
        full_message = (
            f"İsim: {name}\nEmail: {email}\nTelefon: {phone}\nKonu: {subject}\n\nMesaj:\n{message}"
        )
        send_email(subject=f"Yeni İletişim: {subject}", body=full_message, to_email="yerlikesif@gmail.com")

        return jsonify({"message": "Mesaj başarıyla gönderildi ve e‑posta yollandı!"}), 200

    except Exception as e:
        print("Hata:", e)
        return jsonify({"error": "Bir hata oluştu."}), 500

# AI ile kategori tahmini ve öneri döndüren endpoint
@app.route('/process', methods=['POST'])
def process():
    try:
        user_input = request.json.get('input', '').strip()
        if not user_input:
            return jsonify({"message": "Lütfen geçerli bir girdi sağlayın."}), 400

        # Ana kategori tahmini
        category_result = classifier(user_input, category_labels)
        top_category = category_result["labels"][0].lower()

        # 1. seviye alt kategori tahmini
        alt_labels = alt_category_labels.get(top_category, [])
        alt_category_result = classifier(user_input, alt_labels)
        top_alt_category = alt_category_result["labels"][0]

        current_subcategory = top_alt_category  # Şu anki kategori

        # 2. seviye varsa tahmin et
        if current_subcategory in alt_category_labels2:
            sub_labels2 = alt_category_labels2[current_subcategory]
            if sub_labels2:
                sub_category_result2 = classifier(user_input, sub_labels2)
                current_subcategory = sub_category_result2["labels"][0]

        # 3. seviye varsa tahmin et
        if current_subcategory in alt_category_labels3:
            sub_labels3 = alt_category_labels3[current_subcategory]
            if sub_labels3:
                sub_category_result3 = classifier(user_input, sub_labels3)
                current_subcategory = sub_category_result3["labels"][0]

        # Güncel kategori ile devam
        top_alt_category = current_subcategory

        # Uygun ürünleri filtrele
        matched = [
            {"product": p[0], "brand": p[1], "subcategory": p[3]}
            for p in product_data
            if top_category in p[2].lower() and top_alt_category in p[3]
        ]

        # Karıştır ve maksimum 10 ürün seç
        random.shuffle(matched)
        unique_products = list({item["product"] for item in matched[:10]})

        # Mesaj hazırla
        if unique_products:
            message = (
                f"En iyi kategori: {top_category.capitalize()}\n"
                f"Alt kategori: {top_alt_category}\n"
            )
        else:
            message = (
                f"En iyi kategori: {top_category.capitalize()} - Alt kategori: {top_alt_category}.\n"
                "Bu kategoriye uygun ürün bulunamadı."
            )

        # JSON cevap döndür
        return jsonify({
            "message": message,
            "products": unique_products,
            "category": top_category.capitalize(),
            "subcategory": top_alt_category
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Flask sunucusunu başlat
if __name__ == '__main__':
    app.run(debug=True)
