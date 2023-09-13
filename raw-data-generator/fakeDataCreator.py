"""
This script populate Fake data for missing columns in table and Get data for existing columns in table from View(which has all data)
"""
from faker import Faker
import pandas as pd
from pyspark.sql import DataFrame
from pyspark.sql import SparkSession
from pyspark.sql.types import (StructField , StructType,StringType,IntegerType,DateType,Row)


spark = (SparkSession.builder.appName("testingMissingColumn")
         .master("local")
         .config("spark.jars.packages", "com.amazon.deequ:deequ:2.0.3-spark-3.3,io.delta:delta-core_2.12:2.4.0")
         .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
         .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog").getOrCreate())

faker=Faker()


def createTableSchema(dfView:DataFrame,dfTable:DataFrame) -> StructType:
    """
    Get missing columns(which is not in View) in Table and assign default datatype of StringType if table column exist in View get datatype from table itself
    :param dfView:
    :param dfTable:
    :return:StructType
    """
    structs = list()
    missingColumnList = get_missing_column_list(dfView,dfTable)

    for index, row in dfTable.iterrows():
        if row["column"] in missingColumnList:
             structs.append(StructField(row["column"], StringType()))
        else:
            structs.append(StructField(row["column"], get_type_from_dataType(row["type"])))
    return StructType(structs);


def get_missing_column_list(dfView:DataFrame,dfTable:DataFrame)-> list:
    tableColumnList = dfTable['column'].tolist()
    viewSchema: StructType = dfView.schema
    viewColumnList = viewSchema.fieldNames()
    missingColumnList = [col for col in tableColumnList if col not in viewColumnList]
    return missingColumnList


def get_type_from_dataType(dataType: str):
    if "NUMBER" in dataType:
        return IntegerType()
    if "DATE" in dataType:
        return DateType()
    else:
       return StringType();

def getView_df(tablename:str) -> DataFrame:
    dfView = spark.sparkContext.parallelize([
        Row(productName="thingA", VERSION_NUMBER="13.0", SEGREGATION_CODE="IN_TRANSIT", valuable="true"),
        Row(productName="thingA", VERSION_NUMBER="5", SEGREGATION_CODE="DELAYED", valuable="false"),
        Row(productName="thingB", VERSION_NUMBER=None, SEGREGATION_CODE="DELAYED", valuable=None),
        Row(productName="thingC", VERSION_NUMBER=None, SEGREGATION_CODE="IN_TRANSIT", valuable="false"),
        Row(productName="thingD", VERSION_NUMBER="1.0", SEGREGATION_CODE="DELAYED", valuable="true"),
        Row(productName="thingC", VERSION_NUMBER="7.0", SEGREGATION_CODE="UNKNOWN", valuable=None),
        Row(productName="thingC", VERSION_NUMBER="20", SEGREGATION_CODE="UNKNOWN", valuable=None),
        Row(productName="thingE", VERSION_NUMBER="20", SEGREGATION_CODE="DELAYED", valuable="false")]).toDF()

    return dfView

def registerUdf():
    spark.udf.register("fake_varchar_udf", fake_varchar,StringType())

def fake_varchar():
    return "FAKE_" + faker.name()

def createSelectExpressionForMissingColumn(missingColumnList:list):
    columnExpressionList= [f"fake_varchar_udf() as {column}" for column in missingColumnList]
    return ','.join("'" + item + "'" for item in columnExpressionList)

def createSelectExpressionForAvailableColumn(availableColumnList:list):
    return ','.join("'" + item + "'" for item in availableColumnList)

def createSelectExpression(dfView:DataFrame,dfTable:DataFrame):
    viewSchema : StructType = dfView.schema
    tableSchema : StructType = createTableSchema(dfView,dfTable)

    viewColumnList=viewSchema.fieldNames()
    tableColumnList=tableSchema.fieldNames()

    missingColumnList = [ col for col in tableColumnList if col not in viewColumnList]
    availableColumnList: list = [col for col in tableColumnList if col in viewColumnList]

    columnExpressionList= [f"fake_varchar_udf() as {column}" for column in missingColumnList]

    return availableColumnList + columnExpressionList

def execute(dfTable,tablename:str):
    dfView = getView_df(tablename)
    dfView.selectExpr(createSelectExpression(dfView,dfTable)).show()
def getMissingTables()->list:
    file_path = "./missing/missing-tables"
    return open(file_path,'r').readline()
def generate_fake_data():
    missingTables = getMissingTables()
    dir_path = "./files"
    from os import listdir
    from os.path import isfile, join
    files = [f for f in listdir(dir_path) if isfile(join(dir_path, f))]
    for filename in files:
        dfTable = pd.read_csv(join(dir_path, filename))
        if filename not in missingTables:
            execute(dfTable,filename)
        else:
            print(f"Skipping Fake Data Generating for table {filename}")

registerUdf()
generate_fake_data()