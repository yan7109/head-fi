from nltk.corpus import stopwords
import string
from fuzzywuzzy import fuzz
from lxml import html
import requests


cached_stop_words = stopwords.words("english") + ['fs', 'sold', 'withdrawn', 'delete', 'pending', 'payment', 'price', 'drop', 'dropped', 'icon', 'sale', 'anymore', 'good', 'used', 'condition', 'like', 'new', 'accessories', 'international', 'int', 'headphones', 'headphone', 'earphone', 'earphones', 'black', 'white', 'red', 'chance', 'buy', 'free', 'shipping']

def remove_punctuations(text):
    return text.translate(string.maketrans("",""), string.punctuation)
    
def remove_stop_words(text):
    return ' '.join([word for word in text.split() if word not in cached_stop_words])

def get_product_id(known_abr_products, product, unknown_product_id):
    # Map the given product to an existing product
    max_like_ratio = 80 # The words must be 80% similar
    max_like_index = 0
    for known_product in known_abr_products.iterkeys():
        like_ratio = fuzz.ratio(known_product, product)
        if like_ratio >= max_like_ratio:
            max_like_ratio = like_ratio
            max_like_index = known_abr_products[known_product]

    if max_like_ratio > 80:
        product_id = max_like_index
    else:
        product_id = unknown_product_id

    return product_id

def get_url_from_thread_id(thread_id):
    return "http://www.head-fi.org/t/" + str(thread_id) + "/"

def is_active_thread(active_product_thread):
    url = get_url_from_thread_id(active_product_thread)
    page = requests.get(url)
    tree = html.fromstring(page.text)

    active = True
    closed = tree.xpath('//div[@class="closed"]/text()')
    if closed != []: active = False

    return active

