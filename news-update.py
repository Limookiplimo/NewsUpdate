import requests
from bs4 import BeautifulSoup
import psycopg2

# Postgrsql connection
conn = psycopg2.connect(host="localhost",database="news",user="user",password="user")
cur = conn.cursor()

def footballNews():
    website = "https://www.thesun.co.uk/sport/football/"
    page = requests.get(website)
    soup = BeautifulSoup(page.content, "html.parser")
    elements = soup.find_all("div", class_="teaser__copy-container")

    for element in elements:
        
        headline = element.find("h3", class_="teaser__headline").text.strip()
        deck = element.find("p", class_="teaser__subdeck").text.strip()
        link = element.find("a", class_="text-anchor-wrap")['href']

        cur.execute("""
                CREATE TABLE IF NOT EXISTS Football (
                    Headline VARCHAR(255),
                    Deck VARCHAR(255),
                    Link VARCHAR(255)
                );
            """)
        cur.execute("INSERT INTO Football (headline, deck, link) VALUES (%s, %s, %s)", (headline, deck, link))
        conn.commit()

def startupsNews():

    website = "https://techcrunch.com/category/startups/"
    page = requests.get(website)
    soup = BeautifulSoup(page.content, "html.parser")
    elements = soup.find_all("header", class_="post-block__header")

    for element in elements:
        title=element.find("h2", class_="post-block__title").text.strip()
        link=element.find("a", class_="post-block__title__link")["href"]
        author=element.find("span", class_="river-byline__authors").text.strip()
        date=element.find("time")["datetime"]

        cur.execute("""
                CREATE TABLE IF NOT EXISTS Startups (
                    Title VARCHAR(255),
                    Link VARCHAR(255),
                    Author VARCHAR(255),
                    Date DATE
                );
            """)
        cur.execute("INSERT INTO Startups (title,link,author,date) VALUES(%s,%s,%s,%s)",(title, link, author, date))
        conn.commit()

def politicsNews():
    website = "https://www.tuko.co.ke/politics/"
    page = requests.get(website)
    soup = BeautifulSoup(page.content, "html.parser")
    items = soup.find_all("article", class_="c-article-card-no-border")

    for item in items:
        headline = item.find("a", class_="c-article-card-no-border__headline").text.strip()
        link = item.find("a")["href"]
        date = item.find("time")["datetime"]

        cur.execute("""
                CREATE TABLE IF NOT EXISTS Politics (
                    Headline VARCHAR(255),
                    Link VARCHAR(255),
                    Date DATE
                );
            """)
        cur.execute("INSERT INTO Politics(Headline,Link,Date) VALUES(%s,%s,%s)",(headline, link, date))
        conn.commit()

cur.close()
conn.close()

