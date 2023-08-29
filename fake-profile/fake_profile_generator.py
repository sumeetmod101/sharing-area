from faker import Faker
from faker.providers import DynamicProvider
from datetime import datetime
import csv
import random

# run_id , run_time , db, table ,status ,suite_name , 
# check_level , check_status ,constraint , constraint_message , constraint_status
CSV_FILE_PATH="combined_verification_result.csv"
TOTAL_JOB_RUNS=8
TOTAL_RECORDS_FOR_EACH_RUN=100

faker = Faker()



def add_providers(providers):
    for provider in providers:
        faker.add_provider(provider)



def get_providers():
    check_level_provider = DynamicProvider(
        provider_name="check_level",
        elements=["ERROR", "WARNING"],
        )
    check_status_provider = DynamicProvider(
        provider_name="check_status",
        elements=["SUCCESS","ERROR", "WARNING"],
    )

    constraint_status_provider = DynamicProvider(
        provider_name="constraint_status",
        elements=["True","False"],
    )
    constraint_message_provider = DynamicProvider(
        provider_name="constraint_message",
        elements=["Input data not in correct Format","Unique Constraint Failure","Value cannot be null","Value doesnot meet constraint requirement"],
    )
    constraint_name_provider = DynamicProvider(
        provider_name="constraint_name",
        elements=["CompletnessConstraint(Completness(id,None))","CompletnessConstraint(Completness(User,id,None))","NonNegativeConstraint","IsContainedInConstraint","HasDataTypeConstraints","UniquenessConstraint(Uniqueness(List(ITEM_ID),None))","ComplianceConstraint"],
    )    
    check_suite_name_provider = DynamicProvider(
        provider_name="check_suite_name",
        elements=["BASIC","Completness","Uniqueness","Compliance"],
    )    
    
    check_provider = DynamicProvider(
        provider_name="check",
        elements=["VERSION_NUMBER,None","ITEM_ID,None","PENALTY_VALUE,None","TASK_CODE,None","PENALTY_MARK,None","VERSION_NUMBER>1,None","BUYER_CODE","DESCRIPTION"],
    )  
    
    db_provider = DynamicProvider(
        provider_name="db",
        elements=["GoldESP"],
    )
    table_provider = DynamicProvider(
     provider_name="table_name",
     elements=["TASK_PENALTIES", "BUYERS","PRICE","USER_REF1","ASSET_REQUIRED_ON_RECEIPT"],
    )
    
    return [db_provider,table_provider,check_level_provider,check_status_provider,constraint_status_provider,constraint_message_provider,constraint_name_provider,check_suite_name_provider,check_provider]

def get_run_id():
    return random.randint(100, 2000)

def get_db():
    return faker.db()

def get_check_status():
    return faker.check_status()

def get_table_name():
    return faker.table_name()

def configureProviders():
    add_providers(get_providers())

def get_check_level():
    return faker.check_level()

def get_status_level():
    return faker.check_status()

def get_constraint_status():
    return faker.constraint_status()

def get_constraint_message():
    return faker.constraint_message()

def get_date_time():
    return faker.iso8601()

def get_constraint_name():
    return faker.constraint_name()

def get_check_suite_name():
    return faker.check_suite_name()

def get_check():
    return faker.check()


def generate_record_for_timestamp(runId, timestamp):
    db=get_db()
    table=get_table_name()
    success=get_constraint_status()
    kind=get_check_suite_name()
    check=get_check()
    severity=get_check_level()
    constraint=get_constraint_name()
    errorMessage=get_constraint_message() if success=="False" else ""
    return [runId,timestamp,db,table,constraint,kind,check,severity,errorMessage,success]
    
def generateCSV():
    with open(CSV_FILE_PATH, 'w') as csvfile: 
        writer = csv.writer(csvfile)
        writer.writerow(['jobRunId','ts','dbName','tableName','specification','kind', 'check', 'severity', 'errorMessage','success' ])
        for runId in range(100,TOTAL_JOB_RUNS+100):
            timestamp=get_date_time()
            for _ in range(0, TOTAL_RECORDS_FOR_EACH_RUN):
                writer.writerow(generate_record_for_timestamp(runId,timestamp))
    
if __name__ == "__main__":
    configureProviders();
    generateCSV()
    print(f"Successful Generated")    