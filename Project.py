
import requests
import pandas as pd
from bs4 import BeautifulSoup
import mysql.connector as mysql
import smtplib 
import json
import schedule
import time

from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email import encoders

from numpy import insert
from pandas import DataFrame


# List the user-agent of personal browser in order to automatically open the target webpage regularly from this browser
headers = {"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36"}

# Use web scraper to get current weather info
def getWeather():
    self_url = "https://www.wetter.com/deutschland/duesseldorf/DE0001855.html#" # List the target weather website 
    page = requests.get(self_url,headers = headers) # Use the requests library to extract the target html 
    soup = BeautifulSoup(page.content,"html.parser")# Beautiful Soup is a Python package to creates a parse tree of parsed pages for extracting data from HTML

    # After analysing page source to figure out that current weather info is within the class of "forecast-navigation-grid"
    table = soup.find_all("div",class_="forecast-navigation-grid")
    for item in table: # Use for loop store and find items for maximum temperature, minimum temperature and possibility of rainfall
        maxtem = item.find(class_='forecast-navigation-temperature-max').text # Get maximal temperature
        mintem = item.find(class_='forecast-navigation-temperature-min').text # Get minimal temperature
        rainy = item.find(class_='forecast-navigation-precipitation-probability').text # Get rainy rate
        return maxtem,mintem,rainy

# Accquire bundesliga score table, selecht the store of the Fortuna Düsseldorf team and transfer into csv file
def getTable():
    url = "https://www.kicker.de/2-bundesliga/tabelle" # List the target bundesliga score website 
    response = requests.get(url) # Use the requests library to get the target bundesliga url 
    tabelle = pd.read_html(response.content, header=0)[0] 
    # Pandas is a data analysis package of python. Here is used to read the bundlesliga score table in tabular form with column data.
    select * from tabeblle  
    where Verein = "Düsseldorf (A)  Fortuna Düsseldorf (A)"
    # SELECT is a command used to query column data in a table. Here is used with conditional clauses (where) to obtain query results.
    fortuna.to_csv("fortuna.csv")  # Transfer the query results into .csv file 

## Connecting to the database using 'connect()' method
## It takes 3 required parameters 'host', 'user', 'passwd'
def getDB():
    print("read DBdata...")
    with open("Database.json")as r_file: # Database info incl.host, user, password und database for security reason is saved externally in a .JSON file
        DBMelissaZY = json.load(r_file) # Read Database.json in order to prepare next step to connect and login Database
    db = mysql.connect(DBMelissaZY) # Connecting to the database using 'connect()' method
    cursor = conn.cursor() # Create an instance of 'cursor' class which is used to execute the 'SQL' statements in 'Python'
    sql = """ 
    create table if not exists fortuna_score(
        Verein varchar(255),
        Pl. varchar(255),
        Tore Varchar(255),
        Punkte Varchar(255)
    """
    cursor.execute(sql) # Create a new tabel names "fortuna_score" with four columns which are identical with the some of the columns of "fortuna.csv"

    for score in scores: # Insert existing the four columns from "fortuna.csv" to the new tabel "fortuna_score" of database "MelissaZY"  
        val = SELECT ("Verein","Pl.","Tore","Punkte") FROM "fortuna.csv" INTO "fortuna_score" IN "MelissaZY"
        sql = "insert into fortuna_score(Verein,Pl.,Tore,Punkte) values((%s, %s, %s, %s)"
        Verein = score[0]
        Pl.= score[1]
        Tore= score[2]
        Punkte= score[3]
        cursor.execute(sql,val)

    conn.commit()
    conn.close()



## Set the parameters required by smtplib
def sendEmail():
    print ("read Emaildata...")
    with open ("Email.json")as read_file: # Sender information incl.Email address and Email password for security reason is saved externally in a .JSON file  
        sender = json.load(read_file) # Read the Email.json file in order to login into sender account 
    
      
    receiver_adress = "melle.yue.zhao@gmail.com"
    subject = "Fortuna-News and weather. Today the rainfall is" +rainy, " the temperatur is from" +maxitem-mintem
    # Edit the subject,here the variables are the real-time weather information extracted from afromentioned function 
   
    message = MIMEMultipart()  # Construct object of MIMEMultipart
    message["subject"] = subject
    message["from"] = sender_adress
    message["to"] = receiver_adress

    # Add email contents
    mail_content = MIMEText( 
        """Hi,How are you?
        Please find the attached file and link about Fortuna Düsseldorf score and News!
        https://www.kicker.de/fortuna-duesseldorf/info
        I wish you have a nice week!
    
        Best Regards""",
        "plain"
    )

    # Add HTML function
    html = MIMEText(
         """
        <html>
            <body>
                <h1>
                    Week Plan
                </h1>
                <h2>
                    Studying
                </h2>
                <h3>
                    Studying
                </h3>
                <p>
                    Studying
                </p>
            </body>
        </html>
        """,
        "html"
    )

    message.attach(mail_content)
    message.attach(html)
    
    # Add above updated fortuna.csv as an attchment into Email 
    csvfile = "fortuna.csv"
    with open(csvfile) as file:
        Attachment = MIMEBase("application", "octet-steam")
        Attachment.set_payload(file.read())
    # Set parameter of this attachment
    encoders.encode_base64(Attachment)
    Attachment.add_header(
        "Content-Disposition",
        f"attachment; csvfile = {csvfile}",
    )
    message.attach(Attachment)

    # Add Fortuna Log as pictures into this email
    imagefile = open('Fortuna.png', 'rb')
    image = MIMEImage(imagefile.read(), _subtype="png")
    image.add_header('Content-ID', '<image1>')
    image["Content-Disposition"] = 'attachment; filename="Fortuna.png"'
    message.attach(image)

    # Login the email and send the email 
    session = smtplib.SMTP("smtp.gmail.com", 587) # Smtplib is a built-in library of python, so there is no need to install with pip
    session.starttls()  # enale security
    session.login(sender["adress"], sender["password"])
    text = message.as_string()
    session.sendmail(sender["adress"], receiver_adress, text)
    session.quit()
    print('Mail Sent')

# scheduling every monday automatically to send the mail
def job():
    print("start")
    weatherandfortuna = weatherandnews_spider()
    send_email(weatherandfortuna)
    print("end")

schedule.every().monday.at("07:30").do(job)
while True:
    schedule.run_pending()
    time.sleep(1)
