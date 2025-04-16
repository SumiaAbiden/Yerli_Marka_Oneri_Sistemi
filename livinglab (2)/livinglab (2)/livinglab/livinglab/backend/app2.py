from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import pipeline
import csv
import random

app = Flask(__name__)
CORS(app)

# Hugging Face zero-shot classification pipeline
classifier = pipeline(
    "zero-shot-classification",
    model="joeddav/xlm-roberta-large-xnli",
    tokenizer="joeddav/xlm-roberta-large-xnli"
)

# Main categories
category_labels = ["gıda", "elektronik", "otomotiv", "temizlik"]

# Subcategories
alt_category_labels = {
    "gıda": ["Meyve Suyu / İçecek", "Çikolata", "Kraker / Bisküvi", "Şekerleme", "Su", "Kahve", "Kahvaltılık", "Sıcak İçecek", "Çay", "Gazlı İçecek", "Diğer Gıda"],
    "elektronik": ["Telefon", "Beyaz Eşya", "Televizyon", "Ses Sistemi / Kulaklık", "Diğer Elektronik"],
    "temizlik": ["Çamaşır Temizliği", "Kişisel Temizlik", "Bulaşık Temizliği", "Yüzey Temizliği", "Diğer Temizlik"],
    "otomotiv": ["Otomotiv / Savunma"]
}

# Load product data
def load_data(filename="scraped_data_with_subcategories.csv"):
    product_data = []
    with open(filename, mode="r", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            product_data.append((row[0], row[1], row[2], row[3]))  # name, brand, category, subcategory
    return product_data

product_data = load_data()

@app.route('/process', methods=['POST'])
def process():
    try:
        user_input = request.json.get('input', '').strip()
        if not user_input:
            return jsonify({"message": "Lütfen geçerli bir girdi sağlayın."}), 400

        # Predict main category
        category_result = classifier(user_input, category_labels)
        top_category = category_result["labels"][0].lower()

        # Predict subcategory
        alt_labels = alt_category_labels.get(top_category, [])
        alt_category_result = classifier(user_input, alt_labels)
        top_alt_category = alt_category_result["labels"][0]

        # Filter matching products
        matched = [
            {"product": p[0], "brand": p[1], "subcategory": p[3]}
            for p in product_data
            if top_category in p[2].lower() and top_alt_category in p[3]
        ]

        random.shuffle(matched)
        unique_products = list({item["product"] for item in matched[:10]})

        if unique_products:
            message = (
                f"En iyi kategori: {top_category.title()}\n"
                f"Alt kategori: {top_alt_category}\n"
                # "Önerilen ürünler:\n" +
                # "\n".join([f"- {product}" for product in unique_products])
            )
        else:
            message = (
                f"En iyi kategori: {top_category.title()} - Alt kategori: {top_alt_category}.\n"
                "Bu kategoriye uygun ürün bulunamadı."
            )

        return jsonify({
            "message": message,
            "products": unique_products,
            "category": top_category,
            "subcategory": top_alt_category
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
