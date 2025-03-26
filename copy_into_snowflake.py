import snowflake.connector as connector
import configparser
import os.path as path

"""
VARIABLES
"""
# list of table names in sql server
table_names = ["actor", "address", "category", "city", "country", "customer", "film", "film_actor",
"film_category", "inventory", "language", "payment", "rental", "staff", "store"]

suffix = "extract.csv"


"""
CONNECT TO SNOWFLAKE DATABASE
"""
# getting snowflake configuration
parser = configparser.ConfigParser()
parser.read(path.dirname(__file__) + "\..\pipeline.conf")
user = parser.get("snowflake_config", "user")
password = parser.get("snowflake_config", "password")
account = parser.get("snowflake_config", "account")

# establish connection to snowflake
conn = connector.connect(
    user=user,
    password=password,
    account=account
)

if conn is None:
    print("Could not connect to Snowflake.")
else:
    print("Connection established!")

# get cursor
cursor = conn.cursor()

# copy data into each table in snowflake
cursor.execute("USE SCHEMA raw.dvdrental")
for i in range(len(table_names)):
    query = """
    COPY INTO raw.dvdrental.{0}
    FROM @dvdrental_s3_stage
    FILES = ('{0}_{1}')
    """.format(table_names[i], suffix)

    cursor.execute(query)

# close
cursor.close()
print("Completed!")




