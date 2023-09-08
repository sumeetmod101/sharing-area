"""
This script will Read V17-Attribute sheet in GOLDESP XLS file and extract
1)Where all ObjectType=Tables and Includeed/Excluded = Included
It will create file per table where file name will be same as TableName and will persist in s-out folder
"""

import pandas as pd
import csv
import os
import shutil
INPUT_XSL_FILE_PATH="./S/GOLDesp17.xlsx"
OUTPUT_DIRECTORY="s-out"


def logEntities(entities):
    print(f"===== {len(entities)} Tables Imported =====" )
    {print(f"Table:{k} No Of Columns {len(v)} ") for (k,v) in entities.items()}

def read_excel_file(file_path):
    try:
        # Read all sheets from the Excel file into a dictionary
        sheets_dict = pd.read_excel(file_path, sheet_name="V17-Attributes")
        return sheets_dict
    except Exception as e:
        print(f"Error occurred while reading the Excel file: {e}")
        return None 
    
def generateFiles(file_path):    
    sheet=read_excel_file(file_path)
    tableToColumnMapping=generateEntities(sheet)
    createFilePerTable(tableToColumnMapping); 


def createFilePerTable(tableToColumnMapping):
    shutil.rmtree(OUTPUT_DIRECTORY,ignore_errors=True)
    os.makedirs(OUTPUT_DIRECTORY)
    for tableName in tableToColumnMapping:
        print(tableName)
        generateCSV(tableName,tableToColumnMapping[tableName])
    print(f"Total File Generate : {len(tableToColumnMapping)}")

def generateCSV(tableName,columnDetails):
    with open(OUTPUT_DIRECTORY + "/" + tableName, 'w') as csvfile: 
        writer = csv.writer(csvfile)
        writer.writerow(['column','type'])
        for columnDetail in columnDetails["cols"]:
                writer.writerow((columnDetail["name"],columnDetail["type"]))
           

def generateEntities(sheet):
    filteredDF = sheet.query("ObjectType == 'TABLE' & IncludedExcluded == 'Include'")
    requiredDFColumns=filteredDF.get(["ObjectName","ObjectType", "Attribute","Type","IncludedExcluded"])
    return generateTableToColumnMapping(requiredDFColumns)
 

def generateTableToColumnMapping(entityDf):
    # Contains TableName to ColumnList mapping 
    entities = dict()
    for index , row in entityDf.iterrows():
        table_name = row["ObjectName"]

        # create entity if needed
        if table_name not in entities:
            entities[table_name] = {
                "cols": []
            }

        # add column
        e = entities.get(table_name)
        e["cols"].append({
            "name": row["Attribute"],
            "type": row["Type"]
        })
    return entities    

if __name__ == "__main__":
    generateFiles(INPUT_XSL_FILE_PATH)
    print(f"Successful Generated: {OUTPUT_DIRECTORY}")
    