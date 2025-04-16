import pandas as pd
import re

# Dosyayı oku (kendi dosya adını buraya yaz)
df = pd.read_csv("scraped_data.csv")

# Kategori sütunundaki baştaki boşlukları temizle
df['Kategori'] = df['Kategori'].str.strip()

# Alt kategori belirleme fonksiyonu
def belirle_alt_kategori(row):
    urun = row['Ürün İsmi'].lower()
    kategori = row['Kategori'].lower()

    urun_kelime_listesi = re.findall(r'\b\w+\b', urun)

    if kategori == 'gıda ürünleri':
        if any(x in urun_kelime_listesi for x in ['frutti', 'aromalı', 'meyve suyu', 'ice tea', 'soğuk çay']):
            return 'Meyve Suyu / İçecek'
        elif 'çikolata' in urun_kelime_listesi:
            return 'Çikolata'
        elif any(x in urun_kelime_listesi for x in ['kraker', 'bisküvi', 'kurabiye', 'goffret']):
            return 'Kraker / Bisküvi'
        elif any(x in urun_kelime_listesi for x in ['zeytin', 'peynir', 'yumurta']):
            return 'Kahvaltılık'
        elif any(x in urun_kelime_listesi for x in ['şeker', 'bonbon']):
            return 'Şekerleme'
        elif any(x in urun_kelime_listesi for x in ['çay', 'salep']):
            return 'Sıcak İçecek'
        elif any(x in urun_kelime_listesi for x in ['kahve', 'nescafe', '3ü1', 'coffee', 'cafe']):
            return 'Kahve', 'Sıcak İçecek'
        elif any(x in urun_kelime_listesi for x in ['gazoz', 'kola', 'fanta', 'sprite']):
            return 'Gazlı İçecek'
        elif any(x in urun_kelime_listesi for x in ['su']):
            return 'Su'
        else:
            return 'Diğer Gıda'

    elif kategori == 'elektronik ürün':
        if any(x in urun_kelime_listesi for x in ['telefon', 'iphone', 'samsung', 'xiaomi']):
            return 'Telefon'
        elif any(x in urun_kelime_listesi for x in ['çamaşır', 'bulaşık', 'buzdolabı']):
            return 'Beyaz Eşya'
        elif any(x in urun_kelime_listesi for x in ['televizyon', 'tv']):
            return 'Televizyon'
        elif any(x in urun_kelime_listesi for x in ['kulaklık', 'hoparlör']):
            return 'Ses Sistemi / Kulaklık'
        else:
            return 'Diğer Elektronik'

    elif kategori == 'temizlik ürünü':
        if any(x in urun_kelime_listesi for x in ['deterjan', 'çamaşır suyu', 'yumuşatıcı']):
            return 'Çamaşır Temizliği'
        elif any(x in urun_kelime_listesi for x in ['sabun', 'şampuan', 'el sabunu', 'duş jeli']):
            return 'Kişisel Temizlik'
        elif any(x in urun_kelime_listesi for x in ['bulaşık deterjanı', 'bulaşık tableti']):
            return 'Bulaşık Temizliği'
        elif any(x in urun_kelime_listesi for x in ['cam temizleyici', 'yüzey temizleyici']):
            return 'Yüzey Temizliği'
        else:
            return 'Diğer Temizlik'

    elif kategori == 'otomotiv / savunma sanayii ürünleri':
        return 'Otomotiv / Savunma'

    else:
        return 'Bilinmeyen'

# Yeni sütunu oluştur
df['Alt Kategori'] = df.apply(belirle_alt_kategori, axis=1)

# Yeni CSV olarak kaydet
df.to_csv("scraped_data_with_subcategories.csv", index=False)

print("Alt kategori eklendi ve dosya 'scraped_data_with_subcategories.csv' olarak kaydedildi.")
