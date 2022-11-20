import textwrap
import mysql.connector
from mysql.connector import errorcode
from read_data import attractions_data

### connecting to MySQL server
cnx = mysql.connector.connect(host="localhost", user="root", password="!QAZ-2wsx")
cursor = cnx.cursor()

### connecting to MySQL database
DB_name = "taipei_attractions"
try:
    cursor.execute("USE {};".format(DB_name))
    print("Successfully connects to MySQL DB: {}.".format(DB_name))
except mysql.connector.Error as err: 
    if err.errno == 1049:
        cursor.execute("CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8';".format(DB_name))
        cnx.database = "taipei_attractions"
        print("A new MySQL DB '{}' is created and connected successfully.".format(DB_name))
    else:
        print(err)
        exit(1)

### use the tables
create_table = textwrap.dedent("""\
    CREATE TABLE attractions(
        attrac_id      BIGINT UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT,
        name           VARCHAR(100) NOT NULL UNIQUE,
        category       VARCHAR(100) NOT NULL,
        description    VARCHAR(5000) NOT NULL,
        address        VARCHAR(100) NOT NULL,
        transport      VARCHAR(1000) NOT NULL          COMMENT 'direction',
        mrt            VARCHAR(100),
        lat            FLOAT NOT NULL CHECK (lat>0)    COMMENT 'latitude',
        lng            FLOAT NOT NULL CHECK (lng>0)    COMMENT 'longitude',
        images         JSON,
        INDEX indexes(name, category, mrt)
    ) ENGINE=InnoDB;""")
try:
    cursor.execute(create_table)
    print("Table 'attractions' is created and ready for use.")
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
        print("Table 'attractions' is ready for use.")
    else:
        print(err.msg)

### insert data
insert_data = textwrap.dedent("""\
    INSERT INTO attractions
    (attrac_id, name, category, description, address, transport, mrt, lat, lng, images)
    VALUES (%(attrac_id)s, %(name)s, %(category)s, %(description)s, %(address)s, 
    %(transport)s, %(mrt)s, %(lat)s, %(lng)s, %(images)s);
    """)
try:
    for i in attractions_data():
        cursor.execute(insert_data, i)
        cnx.commit()
    print("Inserting attractions data is completed.")
except mysql.connector.Error as err:
    if err.errno == 1062:
        print("Data 'attractions' is ready for use.")
    else:
        print(err.msg)