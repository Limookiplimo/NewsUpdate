import os
import psycopg2
from smtplib import SMTP
from email.mime.text import MIMEText
import configs


# Establish db connections and execute queries
def db_conn():
    with psycopg2.connect(host=configs.host, database=configs.database, user=configs.user, password=configs.password) as conn:
        return conn

def db_query(cursor, query):
    cursor.execute(query)
    return cursor.fetchall()

# Mail configuration
def submit_mail(from_adr,to_adr, subject, body, token):
    #server config
    server = SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(from_adr, token)
    #message config
    message = MIMEText(body)
    message["Subject"] = subject
    message["From"] = from_adr
    message["To"] = to_adr
    #send mail
    server.sendmail(from_adr, to_adr, message.as_string())
    #close server conn
    server.quit()

# Format extracted data
def format_message(rows):
    formated_message = ""
    for row in rows:
        formated_row = " ".join(str(item) for item in row)
        formated_message += formated_row + "\n\n"
    return formated_message

# News update
def mail_update():
    #apply mail credentials
    token = os.environ.get("smtp_news_token")
    sender = configs.sender
    recipient = configs.recipient
    #establish database connection
    conn = db_conn()
    cur = conn.cursor()
    #create sql queries
    sports_query = "select subtitle, link from football limit 3"
    startups_query = "select title, link from startups limit 3"
    politics_query = "select headline, link from politics limit 3"
    #execute sql query
    sports_data = db_query(cur, sports_query)
    startups_data = db_query(cur, startups_query)
    politics_data = db_query(cur, politics_query)
    #format data
    sports_msg = format_message(sports_data)
    startups_msg = format_message(startups_data)
    politics_msg = format_message(politics_data)
    #mail format
    subject = "Top Stories today"
    body = " On the headlines \n\n"
    body += "SPORTS \n"+ sports_msg + "STARTUPS \n" + startups_msg + "POLITICS \n" + politics_msg
    #send mail
    submit_mail(sender, recipient, subject, body, token)
    
mail_update()
