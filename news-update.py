from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import psycopg2

# Postgrsql connection
conn = psycopg2.connect(
    host="localhost",
    database="news",
    user="user",
    password="user"
)


def footballNews():
    path = "Documents/Projects/News-update/chromedriver_linux64"
    website = "https://www.thesun.co.uk/sport/football/"
    service = Service(executable_path=path)
    driver = webdriver.Chrome(service=service)
    driver.get(website)

    sport_news = driver.find_elements(by='xpath', value='//div [@class="teaser__copy-container"')
    for item in sport_news:
        headline = item.find_element(by='xpath',value='./a/h3').text
        deck = item.find_element(by='xpath',value='./a/p').text
        link = item.find_element(by='xpath',value='./a').get_attribute('href')
        
        cur = conn.cursor()
        cur.execute("""
                CREATE TABLE IF NOT EXISTS Football (
                    Headline VARCHAR(255),
                    Deck VARCHAR(255),
                    Link VARCHAR(255),
                );
            """)
        cur.execute("INSERT INTO Football(Headline,Deck,Link,Region) VALUES(%s,%s,%s)",
            (headline,deck,link)
        )
        conn.commit()
        cur.close()

conn.close()

