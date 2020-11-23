import helpers
from helpers import make_query, get_database_engine, myprint
import pandas as pd
from dotenv import load_dotenv
load_dotenv()

engine = get_database_engine(force_cloud=False)

def manage_worksites(worksites, year, quarter):

    worksites = worksites.rename(columns={"PLACE_OF_EMPLOYMENT_ADDRESS1": "WORKSITE_ADDRESS",
                                          "PLACE_OF_EMPLOYMENT_ADDRESS2": "WORKSITE_ADDRESS2",
                                          "PLACE_OF_EMPLOYMENT_CITY": "WORKSITE_CITY",
                                          "PLACE_OF_EMPLOYMENT_STATE": "WORKSITE_STATE",
                                          "PLACE_OF_EMPLOYMENT_POSTAL_CODE": "WORKSITE_POSTAL_CODE"})

    worksites = helpers.fix_zip_code_columns(worksites, ["WORKSITE_POSTAL_CODE"])
    worksites["table"], worksites["Source"], worksites["fy"] = "dol_w", "DOL", f"{year}Q{quarter}"

    return worksites

def add_worksites_to_postgres():
    file_path, year, quarter = "dol_data/H-2A_AddendumB_Employment_FY2020.xlsx", 2020, 4
    worksites = pd.read_excel(file_path)

    worksites = manage_worksites(worksites, year, quarter)
    myprint(f"Adding {len(worksites)} rows to additional_worksites table.")

    # for i, job in worksites.iterrows():
    #     job_df = pd.DataFrame(job.to_dict(), index=[0])
    #     job_df.to_sql("additional_worksites", engine, if_exists='append', index=False)
    #     if i % 100 == 0:
    #         print(f"added {i} rows so far")


    worksites.to_sql("additional_worksites", engine, if_exists='append', index=False)

    if quarter != 1:
        make_query(f"""DELETE FROM additional_worksites WHERE fy = '{year}Q{quarter - 1}'""")

if __name__ == "__main__":
   add_worksites_to_postgres()