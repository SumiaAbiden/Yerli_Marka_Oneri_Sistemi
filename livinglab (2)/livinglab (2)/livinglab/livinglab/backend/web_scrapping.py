from bs4 import BeautifulSoup
import requests

# Global değişkenler
base_url = "https://www.yerlituket.com/gida-c-513&type=1&s="
base_url2 = "https://www.yerlituket.com/gida-c-513&type=2&s="
base_url3 = "https://www.yerlituket.com/elektronik-c-515&s="
base_url4 = "https://www.yerlituket.com/temizlik-c-541&s="
markalist = []
productlist = []
productbrandlist = []



def scrape_brandse(start_page=1, end_page=20):
    global markalist
    global kategori  # Kategori bilgisini global yapıyoruz
    for page_num in range(start_page, end_page):
        url = f"{base_url3}{page_num}"
        html_text = requests.get(url).text
        soup = BeautifulSoup(html_text, 'lxml')

        # Markaları bul ve listeye ekle
        brands = soup.find_all('span', class_='woocommerce-Price-amount amount')
        for brand in brands:
            brand_link = brand.find('a')
            if brand_link:
                brand_name = brand.text.strip()
                markalist.append(brand_name)
        markalist = list(set(markalist))


        # Kategoriyi al
        breadcrumbs = soup.find('div', class_='breadcrumbs')
        if breadcrumbs:
            kategori_linkleri = breadcrumbs.find_all('a')
            kategori = kategori_linkleri[-1].text.strip()  # Sonuncu kategoriyi alıyoruz
        else:
            kategori = "Kategori bulunamadı"

scrape_brandse()


def display_brands():
    for brand in markalist:
        print(f'''
        Marka İsmi: {brand}
        Kategori: {kategori}
        ''')

display_brands()

markalist = []
productlist = []
def scrape_brandsk(start_page=1, end_page=36):
    global markalist
    global kategori  # Kategori bilgisini global yapıyoruz
    for page_num in range(start_page, end_page):
        url = f"{base_url4}{page_num}"
        html_text = requests.get(url).text
        soup = BeautifulSoup(html_text, 'lxml')

        # Markaları bul ve listeye ekle
        brands = soup.find_all('span', class_='woocommerce-Price-amount amount')
        for brand in brands:
            brand_link = brand.find('a')
            if brand_link:
                brand_name = brand.text.strip()
                markalist.append(brand_name)
        markalist = list(set(markalist))


        # Kategoriyi al
        breadcrumbs = soup.find('div', class_='breadcrumbs')
        if breadcrumbs:
            kategori_linkleri = breadcrumbs.find_all('a')
            kategori = kategori_linkleri[-1].text.strip()  # Sonuncu kategoriyi alıyoruz
        else:
            kategori = "Kategori bulunamadı"

scrape_brandsk()


def display_brands():
    for brand in markalist:
        print(f'''
        Marka İsmi: {brand}
        Kategori: {kategori}
        ''')

display_brands()


def scrape_brands(start_page=1, end_page=33):
    global markalist
    global kategori  # Kategori bilgisini global yapıyoruz
    for page_num in range(start_page, end_page):
        url = f"{base_url}{page_num}"
        html_text = requests.get(url).text
        soup = BeautifulSoup(html_text, 'lxml')

        # Markaları bul ve listeye ekle
        brands = soup.find_all('span', class_='woocommerce-Price-amount amount')
        for brand in brands:
            brand_name = brand.text.strip()
            markalist.append(brand_name)
        markalist = list(set(markalist))

        # Kategoriyi al
        breadcrumbs = soup.find('div', class_='breadcrumbs')
        if breadcrumbs:
            kategori_linkleri = breadcrumbs.find_all('a')
            kategori = kategori_linkleri[-1].text.strip()  # Sonuncu kategoriyi alıyoruz
        else:
            kategori = "Kategori bulunamadı"








markalist = []
productlist = []
def scrape_products(start_page=1, end_page=64):
    global productlist
    for page_num in range(start_page, end_page):
        url = f"{base_url2}{page_num}"
        html_text = requests.get(url).text
        soup = BeautifulSoup(html_text, 'lxml')

        # Ürünleri bul ve listeye ekle
        products = soup.find_all('span', class_='woocommerce-Price-amount amount')
        for product in products:
            product_name = product.text.strip()
            productlist.append(product_name)
        # Tekrarlayanları kaldır
        productlist = list(set(productlist))

def match_products_to_brands():
    for product in productlist:
        for word in product:
            if word in markalist:
                productbrandlist.append(word)



def display_products():
    for product in productlist:
        brand = find_brand_for_product(product)
        print(f'''
        Ürün İsmi: {product}
        Marka: {brand}
        Kategori: {kategori}
        ''')

def find_brand_for_product(product):
    # Ürüne karşılık gelen markayı bul
    product = product.lower()
    for brand in markalist:
        brand_lower = brand.lower()  # Markayı küçük harfe çeviriyoruz
        if brand_lower in product:
            return brand

# Fonksiyonları kullanarak işlemi başlatıyoruz
scrape_brands()
scrape_products()

# Ürünleri markalarla eşleştir
match_products_to_brands()

# Markaları ve ürünleri göster
display_brands()
display_products()