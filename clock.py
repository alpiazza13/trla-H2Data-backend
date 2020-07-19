from apscheduler.schedulers.blocking import BlockingScheduler
import pandas as pd
from sqlalchemy import create_engine
engine = create_engine('postgres://txmzafvlwebrcr:df20d17265cf81634b9f689187248524a6fd0d56222985e2f422c71887ec6ec0@ec2-34-224-229-81.compute-1.amazonaws.com:5432/dbs39jork6o07d')

sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=2)
def timed_job():
    df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    now = str(datetime.datetime.now())
    df.to_sql('now', engine, if_exists='replace', index=False)

# @sched.scheduled_job('cron', day_of_week='mon-fri', hour=17)
# def scheduled_job():
#     print('This job is run every weekday at 5pm.')

sched.start()
