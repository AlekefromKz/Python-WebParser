ufrom bs4 import BeautifulSoup as bsoup
import requests
import json
import re

def webparser(p_content):
    res = list()
    for each in p_content:

        href = each.find(
            "figure", class_="offer-thumb__image").find("a")['data-original']
        item_name = each.find('p')['title']

        price = each.find("span", class_="discount-price")
        
        #Checking price 

        if price != None:
            price = price.get_text()

        else:
            try:
                price = each.find(
                    "span", class_="price-cp").get_text()
            except AttributeError:
                try:
                    price = each.find("span", class_="price-bn-old").get_text()
                except AttributeError:
                    price = "not retrived"
            except AttributeError:
                price = "not retrived"

        PC_inf = {"Title": item_name,
                         "Price": price,
                         "Picture href": href}

        res.append(PC_inf)

    return res


link = ("https://www.osta.ee/en/category/computers/")


with open('./computers.json', 'a', newline='\n', encoding='utf8') as f_Write:

    if requests.get(link).status_code == 200:
        page = requests.get(link)
        p_content = page.content
        data = bsoup(p_content, 'html.parser')
        slides = data.find_all(class_="slide")
        parsed_content = webparser(slides)
        json.dump(parsed_content, f_Write, ensure_ascii=False)
        items = data.find_all("figure", class_=re.compile(
                "^offer-thumb has-footer new-th"))
        parsed_content = webparser(items)
        json.dump(parsed_content, f_Write, ensure_ascii=False)


    num = 2
    Error = 0

    while Error == 0:
        try:
            page = requests.get("%spage-%s" % (link, num))
            p_content = page.content
            data = bsoup(p_content, 'html.parser')
            items = data.find_all("figure", class_=re.compile(
                "^offer-thumb has-footer new-th"))
            parsed_content = webparser(items)

            if len(parsed_content) == 0:
                exit()
            json.dump(parsed_content, f_Write, ensure_ascii=False)

        except:
            Error = 1 

        num += 1 