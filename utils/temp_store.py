import os
import pandas as pd

# tempolarily store metadata to Excel file
def store_metadata(metadata):
    # create database folder if it's doesn't exist
    temp_db = os.path.join("output")
    if not os.path.exists(temp_db):
        os.makedirs(temp_db)

    # create an excel file in the temporary db if it doesn't exit and add new metadata
    temp_db = os.path.join(temp_db, "metadata.xlsx")
    if not os.path.exists(temp_db):
        df = pd.DataFrame([metadata])
        df.to_excel(temp_db, index=False)

    # add metadata to the database
    else:
        df = pd.read_excel(temp_db)
        df = pd.concat([df, pd.DataFrame([metadata])], ignore_index=True)
        df.to_excel(temp_db, index=False)
