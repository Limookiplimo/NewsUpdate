import requests
from bs4 import BeautifulSoup
import psycopg2

# Postgrsql connection
conn = psycopg2.connect(host="localhost",database="news",user="user",password="user")
cur = conn.cursor()

def footballNews():
    URL = "https://www.thesun.co.uk/sport/football/"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    items = soup.find_all("div", class_="teaser__copy-container")

    for item in items:
        headline = item.find("h3", class_="teaser__headline").text.strip()
        deck = item.find("p", class_="teaser__subdeck").text.strip()
        link = item.find("a", class_="text-anchor-wrap")['href']

        cur.execute("""
                CREATE TABLE IF NOT EXISTS Football (
                    Headline VARCHAR(255),
                    Deck VARCHAR(255),
                    Link VARCHAR(255)
                );
            """)
        cur.execute("INSERT INTO Football (headline, deck, link) VALUES (%s, %s, %s)", (headline, deck, link))
        conn.commit()


