
import pymssql
import boto3

# Configurable parameters
backup_file = '20240108_DFND.bak' # The file name for the .bak file to read into the DB
new_database = 'umms_dfnd_db' # The name of the database to read into (note this shouldnt be master)
bucket_name = 'stratcom-bmfs-datacl-gold' # Select the bucket you wish to get the backup file from
folder_name = 'temp/umms-backup' # Choose a name for a folder for the file to go into in S3
no_recovery = True # (either True or False)

# Static connection parameters
host = 'stratcom-bmfs-datacl-app-sql.crxozx5jspo3.eu-west-2.rds.amazonaws.com' # Update
database = 'master'
user = 'stratcombmfsdatacl'
port = '1433'
secret_name = 'stratcom-bmfs-datacl-app-sql-database-52spP'
driver = '{ODBC Driver 17 for SQL Server}'
kms_key = 'arn:aws:secretsmanager:eu-west-2:647585978221:secret:stratcom-bmfs-datacl-app-sql-database-52spP-fyfESY'

# Retrieve your password from AWS Secretmanager
client = boto3.client('secretsmanager')
response = client.get_secret_value(SecretId = secret_name)
password = response['SecretString']

# Create a connection object
conn = pymssql.connect(
    f"SERVER={host};DATABASE={database};UID={user};PWD={password}", 
    autocommit=True,
)

# Create a cursor object
cursor = conn.cursor()

# Create the restore query
query = f"""exec msdb.dbo.rds_restore_database
	@restore_db_name='{new_database}',
	@s3_arn_to_restore_from='arn:aws:s3:::{bucket_name}/{folder_name}/{backup_file}',
	@with_norecovery={int(no_recovery)},
	@kms_master_key_arn='{kms_key}',
    @type='FULL';
"""

# Execute the restore query
try:
    cursor = cursor.execute(query)
    print("Restore operation successful!")
except:
    print(f"An error occurred: ")

finally:
    # Close the connection
    if 'conn' in locals() and conn:
        conn.close()

