import psycopg2
import configs
import requests
from bs4 import BeautifulSoup

# Establish db connection and create table
def create_table(table_name, columns):
    with psycopg2.connect(host=configs.host, database=configs.database, user=configs.user, password=configs.password) as conn:
        with conn.cursor() as cur:
            cur.execute(f"""
                create table if not exists {table_name}(
                {','.join(columns)})""")

# Insert data into db
def populate_table(table_name, data):
    with psycopg2.connect(host=configs.host, database=configs.database, user=configs.user, password=configs.password) as conn:
        with conn.cursor() as cur:
            cur.executemany(f"""
                insert into {table_name} values(
                    {', '.join(['%s'] * len(data[0]))})""", data)

            conn.commit()

# Scrape the sun website
def scrape_sports():
    website = "https://www.thesun.co.uk/sport/football/"
    page = requests.get(website)
    soup = BeautifulSoup(page.content, "html.parser")
    elements = soup.find_all("div", class_="teaser__copy-container")

    sports_data = []
    for element in elements:
        title = element.find("h3",class_="teaser__headline").text.strip()
        subtitle = element.find("p", class_="teaser__subdeck").text.strip()
        link = element.find("a", class_="text-anchor-wrap")['href']
        sports_data.append((title, subtitle, link))

    create_table("Football", ["Headline VARCHAR(255)","Deck VARCHAR(255)", "Link VARCHAR(255)"])
    populate_table("Football", sports_data)

# Scrape techcrunch
def scrape_startups():
    website = "https://techcrunch.com/category/startups/"
    page = requests.get(website)
    soup = BeautifulSoup(page.content, "html.parser")
    elements = soup.find_all("header", class_="post-block__header")

    startups_data = []
    for element in elements:
        title = element.find("h2", class_="post-block__title").text.strip()
        link = element.find("a", class_="post-block__title__link")["href"]
        author = element.find("span", class_="river-byline__authors").text.strip()
        date = element.find("time")["datetime"]
        startups_data.append((title, link, author, date))
    
    create_table("Startups", ["Title VARCHAR(255)","Link VARCHAR(255)","Author VARCHAR(255)","Date DATE"])
    populate_table("Startups", startups_data)

# Scrape tuko news
def scrape_politics():
    website = "https://www.tuko.co.ke/politics/"
    page = requests.get(website)
    soup = BeautifulSoup(page.content, "html.parser")
    elements = soup.find_all("article", class_="c-article-card-no-border")

    politics_data = []
    for element in elements:
        title = element.find("a", class_="c-article-card-no-border__headline").text.strip()
        link = element.find("a")["href"]
        date = element.find("time")["datetime"]  
        politics_data.append((title, link, date))
    
    create_table("Politics", ["Headline VARCHAR(255)","Link VARCHAR(255)","Date DATE"])
    populate_table("Politics", politics_data)


