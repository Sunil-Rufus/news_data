import requests
from bs4 import BeautifulSoup
import urllib.parse

def scrape_bbc_news():
    base_url = 'https://www.bbc.com'
    news_url = base_url + '/news/world'
    html = requests.get(news_url)

    s = BeautifulSoup(html.content, 'html.parser')
    articles = s.find_all('div', class_='gs-c-promo-body')

    with open('bbc_news.txt', 'w', encoding='utf-8') as file:
        for article in articles:
            headline = article.find('h3', class_='gs-c-promo-heading__title')
            article_href = article.a['href']
            article_url = urllib.parse.urljoin(base_url, article_href)
            article_html = requests.get(article_url)
            article_soup = BeautifulSoup(article_html.content, 'html.parser')

            article_title = article_soup.find('h1', class_='gel-trafalgar-bold qa-story-headline')
            paragraphs = article_soup.find_all('p', class_='ssrcss-1q0x1qg-Paragraph e1jhz7w10')
            date = article_soup.find('time', class_='qa-status-date-output')

            if headline:
                file.write("Headline: " + headline.text.strip() + "\n")
            if article_title:
                file.write("Article Title: " + article_title.text.strip() + "\n")
            if date:
                file.write("Date: " + date['datetime'] + "\n")
            file.write("Article Content:\n")
            if paragraphs:
                for paragraph in paragraphs:
                    file.write(paragraph.get_text().strip() + "\n")
            else:
                file.write("Sorry, I could not find the article content for this headline.\n")
            file.write("-" * 50 + "\n")

scrape_bbc_news()
