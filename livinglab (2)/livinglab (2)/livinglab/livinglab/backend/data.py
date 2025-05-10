import pandas as pd
import re

# Dosyayı oku
df = pd.read_csv("scraped_data.csv")
df['Kategori'] = df['Kategori'].str.strip()

def belirle_alt_kategori(row):
    urun = row['Ürün İsmi'].lower()
    kategori = row['Kategori'].lower()
    urun_kelime_listesi = re.findall(r'\b\w+\b', urun)

    if kategori == 'gıda ürünleri':
        if any(x in urun_kelime_listesi for x in ['didi','soğuk', 'ice', 'tea']):
            return ['Soğuk çay', 'Soğuk İçecek']
        elif any(x in urun_kelime_listesi for x in ['gazoz', 'kola', 'fanta', 'sprite', 'gazlı', 'gazozu']):
            return ['Gazlı İçecek', 'Soğuk İçecek', 'içecek']
        elif any(x in urun_kelime_listesi for x in ['enerji']):
            return ['Enerji İçeceği', 'Soğuk İçecek', 'içecek']
        elif any(x in urun_kelime_listesi for x in ['frutti', 'aromalı', 'suyu', "sıkma", 'meyvelim']):
            return ['Meyve Suyu', 'İçecek']
        elif any(x in urun_kelime_listesi for x in ["limonata", 'şerbet', 'şerbeti','nektar', 'nektarı', 'içecek', 'içeceği', 'ayran']):
            return ['İçecek']
        elif any(x in urun_kelime_listesi for x in ['kraker']):
            return ['Kraker', 'Atıştırmalık']
        elif any(x in urun_kelime_listesi for x in ['bisküvi', 'kurabiye', 'goffret', 'gofret', 'jöleli', 'çikolatam', 'bisküvisi']):
            return ['Bisküvi', 'Atıştırmalık']
        elif any(x in urun_kelime_listesi for x in ['kek', 'cake', 'topkek', 'popkek', 'paykek']):
            return ['Kek', 'Atıştırmalık']
        elif any(x in urun_kelime_listesi for x in ['fresca', 'dondurma']):
            return ['Dondurma', 'Atıştırmalık']
        elif any(x in urun_kelime_listesi for x in ['çikolata', 'banada', 'frema', 'nuga']):
            return ['Çikolata', 'Atıştırmalık']
        elif any(x in urun_kelime_listesi for x in ['şeker', 'bonbon', 'şekeri']):
            return ['Şekerleme', 'Atıştırmalık']
        elif any(x in urun_kelime_listesi for x in ['zeytin', 'peynir', 'yumurta', 'peyniri', 'kaşar', 'kahvaltılık',
                                                    'sosis', 'salam', 'sucuk', 'kavurma','bal', 'balı', 'ezmesi',
                                                    'kreması', 'helva', 'helvası', 'jambon']):
            return ['Kahvaltılık']
        elif any(x in urun_kelime_listesi for x in ['turta', 'cipsi', 'kompostosu', 'burçak', 'lifalif']):
            return ['Atıştırmalık']
        elif any(x in urun_kelime_listesi for x in ['zeytinyağı', 'yağ', 'yağı', 'tereyağı', 'margarin']):
            return ['Yağ']
        elif any(x in urun_kelime_listesi for x in ['et', 'tavuk']):
            return ['Et']
        elif any(x in urun_kelime_listesi for x in ['yoğurt']):
            return ['Yoğurt']
        elif any(x in urun_kelime_listesi for x in ['süt']):
            return ['Süt', 'Kahvaltılık']
        elif any(x in urun_kelime_listesi for x in ['kahve', 'nescafe', '3ü1', 'coffee', 'cafe', 'coffeeto', 'espresso', 'kahvesi']):
            return ['Kahve', 'Sıcak İçecek', 'içecek']
        elif any(x in urun_kelime_listesi for x in ['çay', 'çayı']):
            return ['Çay', 'Sıcak İçecek', 'içecek']
        elif any(x in urun_kelime_listesi for x in ['maden suyu', 'soda']):
            return ['Soda', 'Soğuk İçecek']
        elif any(x in urun_kelime_listesi for x in ['su', 'premium']):
            return ['Su', 'içecek']
        else:
            return ['Diğer Gıda']

    elif kategori == 'elektronik ürün':
        if any(x in urun_kelime_listesi for x in ['televizyon', 'tv']):
            return ['Televizyon']
        elif any(x in urun_kelime_listesi for x in ['kulaklık', 'hoparlör']):
            return ['Ses Sistemi / Kulaklık']
        elif any(x in urun_kelime_listesi for x in ['klima']):
            return ['Klima']
        elif any(x in urun_kelime_listesi for x in ['saç', 'ütü', 'sebili', 'tartı', 'süpürge', 'ütüler']):
            return ['Küçük Ev Aletleri']
        elif any(x in urun_kelime_listesi for x in ['mikrodalga', 'mikseri','çay', 'kahve', 'tost', 'meyve', 'ekmek',
                                                    'ızgara', 'blenderı', 'kıyma', 'yoğurt', 'mutfak', 'süt']):
            return ['Küçük Mutfak Aletleri']
        elif any(x in urun_kelime_listesi for x in ['kızartma', 'fritöz']):
            return ['Fritöz', 'Küçük Mutfak Aletleri']
        elif any(x in urun_kelime_listesi for x in ['blender', 'mikser']):
            return ['Blender', 'Küçük Mutfak Aletleri']
        elif any(x in urun_kelime_listesi for x in ['çamaşır']):
            return ['Çamaşır Makinesi', 'Beyaz Eşya']
        elif any(x in urun_kelime_listesi for x in ['bulaşık']):
            return ['Bulaşık Makinesi', 'Beyaz Eşya']
        elif any(x in urun_kelime_listesi for x in ['buzdolabı']):
            return ['Buzdolabı', 'Beyaz Eşya']
        elif any(x in urun_kelime_listesi for x in ['çamaşır', 'bulaşık', 'kurutma', 'buzdolabı', 'fırın']):
            return ['Beyaz Eşya']
        elif any(x in urun_kelime_listesi for x in ['su']):
            return ['Su ısıtıcı']
        else:
            return ['Diğer Elektronik']

    elif kategori == 'temizlik ürünü':
        if any(x in urun_kelime_listesi for x in ['deterjan', 'çamaşır', 'yumuşatıcı', 'matik']):
            return ['Çamaşır Temizliği']
        elif any(x in urun_kelime_listesi for x in ["krem", 'sabun', 'şampuan', 'el', 'duş', 'sabunu', 'kulak']):
            return ['Kişisel Temizlik']
        elif any(x in urun_kelime_listesi for x in ['bulaşık', 'tableti']):
            return ['Bulaşık Temizliği']
        elif any(x in urun_kelime_listesi for x in ['cam', 'yüzey', 'yer', 'ahşap']):
            return ['Yüzey Temizliği']
        elif any(x in urun_kelime_listesi for x in ['banyo', 'kireç', 'lavabo']):
            return ['Banyo Temizliği']
        elif any(x in urun_kelime_listesi for x in ['oda', 'ortam', 'koku', 'kokusu']):
            return ['Oda kokusu']
        elif any(x in urun_kelime_listesi for x in ['makine', 'parlatıcı']):
            return ['Makine Temizleyici']
        elif any(x in urun_kelime_listesi for x in ['bez', 'bezi', 'süngeri', 'sünger', 'paspas', 'mop']):
            return ['Temizlik bezi/Süngeri/Paspas']
        elif any(x in urun_kelime_listesi for x in ['leke', 'tüy', 'genel', 'çok', 'amaçlı']):
            return ['Genel Temizlik']
        elif any(x in urun_kelime_listesi for x in ['eldiven', 'poşeti', 'çöp', 'folyo', 'pişirme', 'streç']):
            return ['Mutfak']
        else:
            return ['Diğer Temizlik']

    elif kategori == 'otomotiv / savunma sanayii ürünleri':
        return ['Otomotiv / Savunma']

    else:
        return ['Bilinmeyen']

# Alt kategorileri liste olarak al
df['Alt Kategoriler'] = df.apply(belirle_alt_kategori, axis=1)

# Maksimum kaç alt kategori varsa o kadar sütun oluştur
max_alt_kat = df['Alt Kategoriler'].apply(len).max()



# Kaydet
df.to_csv("scraped_data_with_subcategories.csv", index=False)
print("Alt kategoriler dosyaya kaydedildi.")
