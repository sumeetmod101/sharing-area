import glob
import csv
import os

CSV_PATH = "./S2_A/goldesp.csv"
STAGING_FILE_OUTPUT="s-out"
MISSING_TABLE_FILE="missing-table"
def readS2A():
    entities = dict()
    # read in csv file
    with open(CSV_PATH, "r") as file:
        # read as dict
        csv_file = csv.DictReader(file)
        for col in csv_file:
            table_name = col["TABLE_NAME"]
            # create entity if needed
            if table_name not in entities:
                entities[table_name] = {
                    "cols": []
                }
            # add column
            e = entities.get(table_name)
            e["cols"].append({
                "name": col["COLUMN_NAME"],
                "type": col["DATA_TYPE"],
                "len": col["DATA_LENGTH"]
            })
        return entities;

def generateMissingTables(dataFrameEntities):
    files = [os.path.basename(file) for file in glob.glob(f"{STAGING_FILE_OUTPUT}/*")]
    missingTables = []
    tablesToMissingColumnsList = list()
    for tableName in files:
        if tableName not in dataFrameEntities:
            missingTables.append(tableName)
        else:
            tableToMissingColumnsList = getMissingColumnForTable(tableName,dataFrameEntities)
            tablesToMissingColumnsList.append(tableToMissingColumnsList)
            
    createMissingTablesFile(missingTables);  
    generateCSV(tablesToMissingColumnsList)      
    return missingTables         

def getMissingColumnForTable(tableName,dataFrameEntities):
    tableToMissingColumnTupleList = list()
    with open(f"{STAGING_FILE_OUTPUT}/{tableName}", "r") as file:
        # read as dict
        csv_file = csv.DictReader(file)
        for col in csv_file:
            column_name = col["column"]
            column_type= col["type"]
            isExist = isColumnExistInS2ATable(column_name,dataFrameEntities.get(tableName))
            if not isExist:
                tableToMissingColumnTupleList.append((tableName,column_name,column_type))
            
            print(f"Column: {column_name} exist :{isExist}")
        return  tableToMissingColumnTupleList   
def isColumnExistInS2ATable(column_name,tableEntity):
        collist=tableEntity.get("cols")
        for tup in collist:
            if(column_name == tup.get("name")):
                return True 
        return False 



def generateCSV(missingColumnsList):
    with open("missing-columns.csv", 'w') as csvfile: 
        writer = csv.writer(csvfile)
        writer.writerow(['table','column','type' ])
        flattendList = [ item for missingSubList in missingColumnsList  for item in missingSubList ]
        for row in flattendList:
            writer.writerow(row)
      
def createMissingTablesFile(missingTablesList):
    print(f"Missing {len(missingTablesList)} Tables")
    with open("missing-table.txt","w") as file:
        file.write("\n".join(missingTablesList))

def generateMissingAttribute():
    dataFrameEntities = readS2A()
    print(f"Read {len(dataFrameEntities)} Tables from S2_A")
    missingTables = generateMissingTables(dataFrameEntities)
   
    
    

if __name__ == "__main__":
    generateMissingAttribute();
    print("Successfully Generated")