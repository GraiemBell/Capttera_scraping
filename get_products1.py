from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from urllib import parse
import pandas as pd
import json
import regex
import pickle as pkl
import os
import time
import random


# cookie = ''

header = {
  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36',
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
  'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
  'Accept-Encoding': 'none',
  'Accept-Language': 'en-US,en;q=0.8',
  'Connection': 'keep-alive',
  'refere': 'https://example.com',
  'cookie': ''
}

def convert_match(match):
    x = str(match.group(0))
    x = x[:2]+x[2:-2].replace('\"', "\'")+x[-2:]
    # x.replace('\\', '')
    return x

def CoutomizedRequest(url):
    gotit = False

    while gotit == False:
        try:
            # load cookie
            with open("cookie1.txt", "r") as f:
                cookie = f.read()
            header["cookie"] = cookie
            
            time.sleep(2+random.random()*3)
            req = Request(url, headers=header)
            webpage = str(urlopen(req).read())
            gotit = True
        except:
            print("connect error")
            print(url)
            input()
    return webpage

def get_metadata(url):
    wepage = CoutomizedRequest(url)
    webpage = '{'+wepage[:-1]+'}'

    with open("review_page.txt", "w") as f:
        f.write(webpage)

    # with open("review_page.txt", "r") as f:
    #     webpage = f.read()

    # replace the elements that affects making json file
    # print(url)
    # try:
    
    metadata = '"hasFreeVersion"'+webpage.split('"reviews":[')[0].split('"hasFreeVersion"')[-1]
    # except:
    
    metadata = metadata.replace('\\', '').replace('class="', "class='").replace('">', "'>")   
    metadata = '{'+metadata[:-1]+'}'
    metadata = regex.sub(r':\"(.*?)\"[\},\,](?! )', convert_match, metadata)

    
    with open(f"metadata.txt", "w") as f:
        f.write(metadata)
    

    try:
        metadata = json.loads(metadata)
    except:
        print("metadata loads error")
        return {}
        # input()
        # with open("metadata.json", "r") as f:
        #     metadata = json.load(f)
        


    return metadata

def get_reviews(url):
    product_ID = url.split("/")[4]
    i = 0
    reviews = []

    while (i <= 99999):
        # try:
        url = f'https://www.capterra.com/spotlight/rest/reviews?apiVersion=2&productId={product_ID}&from=' + str(i)
        # req = Request(url, headers=header)
        webpage = CoutomizedRequest(url)
        webpage = webpage[2:-1]
        
        # webpage to json
        sub_reviews = webpage.replace('\\', '')
        sub_reviews = regex.sub(r':\"(.*?)\"[\},\,](?! )', convert_match, sub_reviews)

        with open('text/'+str(i) + '.txt', 'w') as outfile:
            outfile.write(sub_reviews)
            
        while True:
            try:
                sub_reviews = json.loads(sub_reviews)
                break
            except:
                print("json loads error")
                with open('error.txt', 'w') as outfile:
                    outfile.write(sub_reviews)
                input()
                with open("metadata.json", "r") as f:
                    sub_reviews = json.load(f)
                break
        
        
        sub_reviews = sub_reviews["hits"]

        if len(sub_reviews) > 0:
            reviews += sub_reviews
        else:
            break

        i += 50

        # except:
        #     with open(f"{i}.txt", "w") as f:
        #         f.write(sub_reviews)
        #     pass
    return reviews

# get product data, input: product url
def get_product_data(url):
    product_data = get_metadata(url)
    reviews = get_reviews(url)

    product_data["reviews"] = reviews

    return product_data

# get product urls, intput category url
def get_products(url):
    # req = Request(url, headers=header)
    # webpage = str(urlopen(req).read())
    
    webpage = CoutomizedRequest(url)

    soup = BeautifulSoup(webpage, "html.parser")

    with open("product_page.txt", "w") as f:
        f.write(webpage)
    with open("product_soup", "wb") as f:
        pkl.dump(soup, f)
    
    products = soup.find_all("script", type="application/ld+json")[3].contents[0]

    products = products.replace("\\n", "").replace('\\', '')
    
    # convert to json file
    products = json.loads(products)
    
    # get prodcuts name and urls
    products = products["itemListElement"]

    # for ele in soup.find_all("a", class_="nb-thumbnail nb-relative nb-thumbnail-medium nb-thumbnail-interactive"):
    #     products.append()

    return products

def get_pages(base_url):
    webpage = CoutomizedRequest(base_url)
    soup = BeautifulSoup(webpage, "html.parser")

    # get
    pages = soup.find_all("div", class_="nb-inline-flex nb-justify-center nb-italic nb-text-sm nb-tracking-md nb-text-gray-300")[0].contents[0]
    pages = pages.split(" ")[-1]
    # pages
    return pages

def get_info_products(base_url):
    # get the number of pages
    try:
        pages = int(get_pages(base_url))
    except:
        pages = 1
    print(pages)
    for page_id in range(pages):
        url = f"{base_url}?page={page_id+1}"
        print(url)
        products = get_products(url)
        for product in products:
            product_name = product["name"]
            product_url = product["url"]
            print(product_name)
            print(product_url)

            product_name = product_name.replace("\\", "&").replace("/", "&").replace("|", "&").replace(":", "&")

            if os.path.exists(f"products/{product_name}.json") == False:
                product_data = get_product_data(product_url)
                with open(f"products/{product_name}.json", "w") as f:
                    json.dump(product_data, f)
        
# get_product_data("https://www.capterra.com/p/131768/MemberPlanet/")