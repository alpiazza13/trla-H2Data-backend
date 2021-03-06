import pandas as pd
from helpers import get_database_engine
engine = get_database_engine(force_cloud=True)

def check_for_new_columns(file_name, table_name):
    postgres_columns = set(pd.read_sql(f"""SELECT "column_name" FROM information_schema.columns WHERE table_name = '{table_name}'""", con=engine)["column_name"].tolist())

    file_columns = pd.read_excel(f"dol_data/{file_name}").columns
    assert len(set(file_columns)) == len(file_columns), "There are duplicate column names in the excel file, which is bad."

    columns_in_file_but_not_postgres = set(file_columns) - postgres_columns
    print(f"Columns in new {file_name} file but not {table_name}:\n {columns_in_file_but_not_postgres}\n")
    return columns_in_file_but_not_postgres



# reports any columns in the H2A additional_worksites, H2B additional_housings, H2A disclosure, and
# H2B disclosure files that are not in these files' corresponding tables in Postgres. Edit `table_file_names_map`
# accordingly based on file names. Assumes all files are located in a folder named dol_data which is in this directory.
if __name__ == "__main__":

    files_table_map = {"H-2A_Disclosure_Data_FY2020.xlsx": "job_central",
                            "H2b_Disclosure_Data_FY2020.xlsx": "job_central",
                            "dol_data/H-2A_AddendumB_Housing_FY2020.xlsx": "additional_housing",
                            "H-2A_AddendumB_Employment_FY2020.xlsx": "additional_worksites"}

    for file in file_tables_map:
        check_for_new_columns(file, files_table_map[file])
