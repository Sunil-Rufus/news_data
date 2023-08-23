import requests
from bs4 import BeautifulSoup
import schedule
import time
from datetime import datetime, timezone

def scrape_world_news():
    url = 'https://www.nbcnews.com/world'
    html = requests.get(url)

    s = BeautifulSoup(html.content, 'html.parser')
    articles = s.find_all('article', class_='tease-card')

    with open('world_news_nbc.txt', 'a', encoding='utf-8') as file:  # Using 'a' mode to append to the file
        current_datetime_utc = datetime.now(timezone.utc)
        current_day = current_datetime_utc.strftime("%A")
        current_time = current_datetime_utc.time()

        file.write(f"Scraped on {current_day}, {current_datetime_utc.strftime('%Y-%m-%d')} at {current_time}\n")

        for article in articles:
            headline = article.find('span', class_='tease-card__headline')
            if headline:
                article_url = article.a['href']
                article_html = requests.get(article_url)
                article_soup = BeautifulSoup(article_html.content, 'html.parser')

                article_title = article_soup.find('h1', class_='article-header__title')
                article_content = article_soup.find('div', class_='article-body__content')

                file.write("Headline: " + headline.text.strip() + "\n")
                if article_title:
                    file.write("Article Title: " + article_title.text.strip() + "\n")
                file.write("Article Content:\n")
                if article_content:
                    paragraphs = article_content.find_all('p')
                    for paragraph in paragraphs:
                        file.write(paragraph.get_text().strip() + "\n")
                file.write("-" * 50 + "\n")

# def schedule_scraping():
#     # Schedule scraping to run daily at 5 AM
#     schedule.every().day.at("05:00").do(scrape_world_news)

#     while True:
#         schedule.run_pending()
#         time.sleep(1)

# # Check if the current time is 5 AM, if so, start scraping immediately
# current_time = datetime.now().time()
# if current_time.hour == 5 and current_time.minute == 0:
scrape_world_news()

# Start scheduling for daily scraping at 5 AM
# schedule_scraping()
