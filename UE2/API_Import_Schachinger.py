import psycopg2
import requests
import json
from psycopg2.extras import Json

#--------------------Review

url = "https://api.nytimes.com/svc/mostpopular/v2/viewed/30.json?api-key=eX4qBYG8AUGOanGSvqUGJFCi5hUoxSSB"

payload={}
headers = {
  'Accept': 'application/json'
}

response_viewed = requests.request("GET", url, headers=headers, data=payload)

#---------------------emailed
url = "https://api.nytimes.com/svc/mostpopular/v2/emailed/30.json?api-key=eX4qBYG8AUGOanGSvqUGJFCi5hUoxSSB"

payload={}
headers = {
  'Accept': 'application/json'
}

response_email = requests.request("GET", url, headers=headers, data=payload)

#----------data
data_viewed = response_viewed.json()
data_email = response_email.json()

data_viewed_res = data_viewed['results']
data_email_res = data_email['results']

#------------------------SQL Connection

conn = psycopg2.connect(host="mds-dsi-db.postgres.database.azure.com",
                        port="5432",
                        database="nyt_import",
                        user="ds22m017",
                        password="SchachingeR14",
                        connect_timeout=3)
cur = conn.cursor()
print("con done")

#-----------------------CREATE TABLES


tables = ['ds22m017_emailed','ds22m017_viewed']
for table in tables:
    cur.execute(f"DROP TABLE IF EXISTS {table} CASCADE;")
    cur.execute(f"CREATE TABLE IF NOT EXISTS {table} (id serial, body JSONB);")
conn.commit()
print("create done")


for res in data_email_res:
    val=Json(res)
    cur.execute(f"INSERT INTO ds22m017_emailed (body) VALUES (%s)", [val])
conn.commit() 
    

for res in data_viewed_res:
    val=Json(res)
    cur.execute(f"INSERT INTO ds22m017_viewed (body) VALUES (%s)", [val])
conn.commit() 
    
    