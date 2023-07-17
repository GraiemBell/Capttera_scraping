from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from urllib import parse
import pandas as pd
import pickle as pkl

import json


cookie = '_gid=GA1.2.1289772216.1688417200; _gcl_au=1.1.1371632258.1688417201; return_user=1051986380.1688417200|Tue Jul 04 2023 05:46:41 GMT+0900 (Japan Standard Time); return_user_session=1051986380.1688417200|Tue Jul 04 2023 05:46:41 GMT+0900 (Japan Standard Time)|new; seerid=6e5b72d1-6264-470a-9c7a-a24e97b3b387; ELOQUA=GUID=CCDB78F86DAA48BBB9D44D28BD9D55C3; device=Desktop; country_code=HK; pxcts=bfaf6e57-19e2-11ee-8340-78706166444a; _pxvid=bfaf57e3-19e2-11ee-8340-3b962d4e71a2; AMCVS_04D07E1C5E4DDABB0A495ED1%40AdobeOrg=1; AMCV_04D07E1C5E4DDABB0A495ED1%40AdobeOrg=-637568504%7CMCIDTS%7C19542%7CMCMID%7C28523936498889248122922075540907390928%7CMCAAMLH-1689022011%7C3%7CMCAAMB-1689022011%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1688424411s%7CNONE%7CvVersion%7C5.1.1; SignUpShowingProductToSaveExperiment=f5017200-19e2-11ee-8b4e-ed5ff86848d2; uw_loginwithemail=false; experimentSessionId=d33b524c-f100-418d-81e7-4a04b705b210; rt_var=prd; uw_signedup=true; uw_identity_sync=true; _pxhd=O48S2JGAefnHj89pRXqlWWHrj-qpwuIfrGZmzWyPvSncTSkkYlEan1/zDwat89byYwricZkOwy8GtYzf23hI0A==:qX4mXtRp7mSS/o8Uizfh-EG1e05UejLDdQldOvr9/tiXp-znD3feiFIu-rwesvNrJOFN9Yzk6gZQZUBshFBoO479o5RUbSYBmABo0kDDYSA=; seerses=e; _px3=ca2d6464f22388180023c5c4a38a2749e5f4302f41248b4f71037eaec396e97f:2RHN8VJ3nFgFtDo/9SfLphvpLS3PYgpiPpY1fpH7H8F6epFZWTZw5hVBAdSDXRlENI4mHUnH39zI289QS35Iow==:1000:NtvZfEBnsGLuUM59PMduiJF4nb5F/GGzB6CiXOZPO20QSdLcVMKbfcEb3gTOZy4aN+J1V6fxgnhvyz3VT9/eTCWr9AtlkAUmEhEMm6goTnMGAXgAQWgykHQIj0cNWL5QfEt/ThUGNyfnCzj26qO6N3UMMDIZwpB3Ch2E+95dVCcVgW4uhKs57+fUVD70EXUO; _gat_UA-126190-1=1; fs_lua=1.1688452579027; fs_uid=#18VAT4#8e33a193-75b2-44fe-827a-c556e40ab77f:c04dd0b5-8172-44be-8c3e-c517d98a4776:1688451545347::2#/1719953202; _gat=1; OptanonConsent=isGpcEnabled=0&datestamp=Tue+Jul+04+2023+15%3A36%3A32+GMT%2B0900+(Japan+Standard+Time)&version=202301.2.0&isIABGlobal=false&hosts=&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1&AwaitingReconsent=false; _ga_T9V61700R6=GS1.1.1688448442.3.1.1688452591.45.0.0; _ga_M5DGBDHG2R=GS1.1.1688442371.4.1.1688452592.44.0.0; _uetsid=b6aeed1019e211ee8e74737688f861f9; _uetvid=b6aee5f019e211ee91a55d9a025b2054; _ga=GA1.2.1051986380.1688417200; _pxde=fa2cbcf8cb1ec47fc38ae58bbd55acaf178bc7f3bc6aa2686caef169c8170dfb:eyJ0aW1lc3RhbXAiOjE2ODg0NTI2MDAyMTEsImZfa2IiOjAsImlwY19pZCI6W119'

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

classnames = {
    "reviewer": "nb-flex nb-text-lg nb-items-center nb-mb-3xs",
    "reviewtitle": "nb-type-lg-bold nb-mt-2xl md:nb-mt-0",
    "reviewcontents": "nb-text-md nb-my-xl"
}


def analyze_reviewcontents(reviewcontents):
    contents_result = {}

    for content in reviewcontents:
        content_soup = BeautifulSoup(str(content), "html.parser")
        content_type = content_soup.find_all("strong")[0].contents[0]
        contents_result[content_type] = str(content_soup.find_all("div", class_=classnames["reviewcontents"])[0].contents[1])

    return contents_result




def extract_reviews(url):
    # scrap the whole webpage / HTML
    req = Request(url, headers=header)
    webpage = urlopen(req).read()

    # get the whole soup
    soup = BeautifulSoup(webpage, "html.parser")

    with open("review_page", "w") as f:
        f.write(str(webpage))

    # create the all reviews
    all_reviews = {}

    for tag in soup.find_all('div'):
        try:
            # check if it is review card
            if tag['data-test-id'] == 'review-card':
                
                # get the review card contents
                sub_html = contents = tag.contents[0]
                sub_soup = BeautifulSoup(str(sub_html), "html.parser")
                

                # get the review info.

                reviewer = sub_soup.find_all("div", class_=classnames["reviewer"])[0].contents[0]
                reviewtitle = sub_soup.find_all("div", class_=classnames["reviewtitle"])[0].contents[0][1:-1]
                reviewcontents = sub_soup.find_all("div", class_=classnames["reviewcontents"])

                # analyze the reviewc contents
                contents_result = analyze_reviewcontents(reviewcontents)

                # insert into the all reviews
                reviwe_content = {
                    "reviewtitle": reviewtitle,
                    "reviewcontents": contents_result
                }

                all_reviews[reviewer] = reviwe_content
        except:
                pass
    
    return all_reviews

# with open("review_soup", "rb") as f:
#     soup = pkl.load(f)




# url = "https://www.capterra.com/p/167338/Bonusly/"
# all_reviews = extract_reviews(url)


# with open("reviews.json", "w") as file:
#     json.dump(all_reviews, file)


extract_reviews("https://www.capterra.com/p/162035/Filestage/")