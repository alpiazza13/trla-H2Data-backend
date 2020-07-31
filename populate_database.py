import pandas as pd
import numpy as np
import math
from sqlalchemy import create_engine
import psycopg2
from geocodio import GeocodioClient
import numpy as np
client = GeocodioClient("454565525ee5444fefef2572155e155e5248221")
engine = create_engine('postgres://txmzafvlwebrcr:df20d17265cf81634b9f689187248524a6fd0d56222985e2f422c71887ec6ec0@ec2-34-224-229-81.compute-1.amazonaws.com:5432/dbs39jork6o07d')

# excel_sheet = input("Type the file name of an excel spreadsheet with your data - make sure this sheet this sheet is in the same folder as this script. \n")
# df = pd.read_excel(excel_sheet)
df = pd.read_excel("DOL Data.xlsx")
df["fixed"] = None
df["housing_fixed_by"] = None
df["worksite_fixed_by"] = None



def create_address_from(address, city, state, zip):
    try:
        return address + ", " + city + " " + state + " " + str(zip)
    except:
        return ""

def geocode_table(worksite_or_housing):

    if worksite_or_housing == "worksite":
        addresses = df.apply(lambda job: create_address_from(job["Worksite address"], job["Worksite address city"], job["Worksite address state"], job["Worksite address zip code"]), axis=1).tolist()
    elif worksite_or_housing == "housing":
        addresses = df.apply(lambda job: create_address_from(job["Housing Info/Housing Address"], job["Housing Info/City"], job["Housing Info/State"], job["Housing Info/Postal Code"]), axis=1).tolist()
    else:
        print("worksite_or_housing should be either `worksite` or `housing`")

    coordinates, accuracies, accuracy_types, failures = [], [], [], []
    failures_count, count = 0, 0
    for address in addresses:
        try:
            geocoded = client.geocode(address)
            accuracy_types.append(geocoded["results"][0]["accuracy_type"])
            coordinates.append(geocoded.coords)
            accuracies.append(geocoded.accuracy)
        except:
            coordinates.append(None)
            accuracies.append(None)
            accuracy_types.append(None)
            failures.append(address)
            failures_count += 1
        count += 1
        print(f"There have been {failures_count} failures out of {count} attempts")
    print(len(coordinates), len(accuracies), len(df), len(accuracy_types))
    df[f"{worksite_or_housing} coordinates"] = coordinates
    df[f"{worksite_or_housing} accuracy"] = accuracies
    df[f"{worksite_or_housing} accuracy type"] = accuracy_types
    print(f"There were {failures_count} failures out of {count} attempts")

geocode_table("worksite")
geocode_table("housing")


# table_name = input('Type the name of the PostgreSQL table into which to put the data. If it already exists, it will be replaced, otherwise it will be created.')
# df.to_sql(table_name, engine, if_exists='replace')

# idea here, to use at top
# for index, row in df.iterrows():
#     print(index)
#     print(row)

df.to_sql("todays_tests", engine, if_exists='replace')