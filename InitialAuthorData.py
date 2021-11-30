# TEST DATA
#URL = 'http://books.toscrape.com/'

from requests.exceptions import HTTPError
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from urllib.parse import urljoin

EW_URL = 'https://quotes.toscrape.com'

def simple_get(url, *args, **kwargs):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        resp = requests.get(url, *args, **kwargs)
        # If the response was successful, no Exception will be raised
        resp.raise_for_status()

    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
        raise http_err
    except Exception as err:
        print(f'Other error occurred: {err}')
        raise err

    return resp

allpage=[]      
def get_allurl2(url):
    resp = simple_get(url, timeout=5)
    html = resp.text
    soup = BeautifulSoup(html, 'html.parser') 
    
    li = soup.find('li', class_='next')
    if li is not None:      
        pgurl = urljoin(url, li.a['href'])  
        allpage.append(pgurl)
        
        get_allurl2(pgurl)
    


def who_actors(allurl):
    
    author = []
    author_date = []
    author_location = []
    for url in allurl:
    
        resp = simple_get(url, timeout=5)
        html = resp.text

        soup = BeautifulSoup(html, 'html.parser')

        body_tag = soup.body


        tag = soup.find_all("div", class_="quote")

        for t in tag:
            a = t.find("small", class_="author")
            author.append(a.text)
            #print("author testing")
            #print(a.text)

            link = allurl[0]+ t.a["href"]
            #print(link)
            result = requests.get(link)
            soup_loop = BeautifulSoup(result.text, 'html.parser')
            auth_date = soup_loop.find("span", class_="author-born-date")
            author_date.append(auth_date.text)
            auth_location = soup_loop.find("span", class_="author-born-location")
            author_location.append(auth_location.text)

        #print(author)
        #print(author_date)
        #print(author_location)
    output = pd.DataFrame({'author': author, 'Author_Birth_Date': author_date,  "Author_Birth_Location": author_location})
    newoutput=output.drop_duplicates(subset='author', keep="last")
    newoutput.reset_index(drop=True)
    print(newoutput)

        #for p in soup.find_all("span", class_ = "author"):
            #print(p.text)

        #for img in soup.find_all('img', title=re.compile(r'^Slide\s+\d+:\s+[A-Z]')):
            #print("here is test2")
            #print(img)

        #print("here is testing")
        #print(soup.findAll("article", class_ = "product_pod"))

        #url_main_page = [EW_URL+x.div.a.get('href') for x in soup.findAll("article", class_ = "product_pod")]

    
def main():
    allpage.append(EW_URL)
    get_allurl2(EW_URL)
    #print(allpage)
    who_actors(allpage)
    
if __name__ == "__main__":
    main()
