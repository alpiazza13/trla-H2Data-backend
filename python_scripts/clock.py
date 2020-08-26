from apscheduler.schedulers.blocking import BlockingScheduler
import os
import pandas as pd
from sqlalchemy import create_engine
import geocodio
client = geocodio.GeocodioClient("454565525ee5444fefef2572155e155e5248221")

def get_secret_variables():
    if os.getenv("LOCAL_DEV") == "true":
        import secret_variables
        return secret_variables.DATABASE_URL, secret_variables.GEOCODIO_API_KEY
    return os.getenv("DATABASE_URL"), os.getenv("GEOCODIO_API_KEY")

def scheduled_job():
    print('and again...')
    geocoded_location = client.geocode("42370 Bob Hope Drive, Rancho Mirage CA")
    print(geocoded_location.coords)

sched = BlockingScheduler()
# change minutes=2 to days=1
sched.add_job(scheduled_job, 'interval', seconds=5, start_date='2020-08-25 22:10:00', timezone='US/Eastern')

sched.start()
