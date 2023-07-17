from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from urllib import parse
import pandas as pd
import pickle
# from get_products import get_products

cookie = ''



header = {
  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36',
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
  'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
  'Accept-Encoding': 'none',
  'Accept-Language': 'en-US,en;q=0.8',
  'Connection': 'keep-alive',
  'refere': 'https://example.com',
  'cookie': cookie
}


# with open("soup", "wb") as f:
#     pickle.dump(soup, f)

# with open("soup", 

def get_categoreis():
    url = "https://www.capterra.com/categories/"

    req = Request(url, headers=header)
    webpage = urlopen(req).read()


    soup = BeautifulSoup(webpage, "html.parser")

    categories = []
    category_links = []
    for tag in soup.find_all('a'):
        try:
            # is it a category link?
            str(tag).index("sb color-mode-light link font-bold block no-underline")
            href_link = str(tag['href'])
            category = href_link.replace("/", "").replace("-", " ")


            category_links.append("https://www.capterra.com"+href_link)
            categories.append(category)
        except:
            pass
    
    return categories, category_links
print(get_categoreis())
