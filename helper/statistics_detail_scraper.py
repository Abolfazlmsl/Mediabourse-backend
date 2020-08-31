import json
from bs4 import BeautifulSoup
from urllib.request import urlopen

url = "http://boursepress.ir/news/157400/%D9%BE%D8%B0%DB%8C%D8%B1%D8%B4-%D9%88-%D8%B9%D8%B1%D8%B6%D9%87-%D8%A7%D9%88%D9%84"

if 'boursepress.ir' in url:
    page = urlopen(url)

    html_bytes = page.read()
    html = html_bytes

    soup = BeautifulSoup(html, "html.parser")

    news = soup.find('div', {"class": "news"})

    image = news.find('div', {'class': 'news-img'}).find('img')['src']
    date = news.find('div', {'class': 'news-map'}).find_all('div')[2].get_text()
    title = news.find('h1').get_text()
    summary = news.find('div', {'class': 'news-lead'}).get_text()
    text_list = news.find('div', {'class': 'news-text'}).find_all('p')
    text_list.pop()
    text_list.pop()
    text = {}
    for i, j in enumerate(text_list):
        text[i+1] = j.get_text()
    short_title = news.find('div', {'class': 'short-title'}).get_text()

    result = {
        "title": title,
        "image": image,
        'short_title': short_title,
        "summary": summary,
        "text": text,
        "date": date,
    }

    with open('data1.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False)
