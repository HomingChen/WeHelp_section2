import textwrap
import mysql.connector
from read_data import attractions_data, files_data
# from collections import namedtuple

### connecting to MySQL server
cnx = mysql.connector.connect(host="localhost", user="root", password="7895123")
cursor = cnx.cursor()

### connecting to MySQL database
### If the DB didn't exist, a new DB will be created.
DB_name = "taipei_attractions"
try:
    cursor.execute("USE {};".format(DB_name))
    print("Successfully connects to MySQL DB: {}.".format(DB_name))
except mysql.connector.Error as err: 
    if err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
        cursor.execute("CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8';".format(DB_name))
        cnx.database = "taipei_attractions"
        print("A new MySQL DB '{}' is created and connected successfully.".format(DB_name))
    else:
        print(err)
        exit(1)

### use the tables
tables = {}
tables["attractions"] = textwrap.dedent("""\
    CREATE TABLE attractions(
        attrac_id      BIGINT UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT,
        name           VARCHAR(100) NOT NULL UNIQUE,
        category       VARCHAR(100) NOT NULL,
        description    VARCHAR(5000) NOT NULL,
        address        VARCHAR(100) NOT NULL,
        transport      VARCHAR(1000) NOT NULL             COMMENT 'direction',
        mrt            VARCHAR(100),
        lat            FLOAT NOT NULL CHECK (lat>0)    COMMENT 'latitude',
        lng            FLOAT NOT NULL CHECK (lng>0)    COMMENT 'longitude',
        images         VARCHAR(255) NOT NULL             COMMENT 'only takes the first img from the data, see table "files" for more info.',
        INDEX indexes(name, category, mrt)
    ) ENGINE=InnoDB;""")
tables["files"] = textwrap.dedent("""\
    CREATE TABLE files(
        file_id     BIGINT UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT,
        attrac_id   BIGINT UNSIGNED NOT NULL,
        link_path   VARCHAR(255) NOT NULL UNIQUE,
        extention   VARCHAR(10) NOT NULL,
        type        ENUM('image', 'audio', 'video', 'undefined') NOT NULL,
        FOREIGN KEY(attrac_id) REFERENCES attractions(attrac_id),
        INDEX indexes(attrac_id, extention, type)
    ) ENGINE=InnoDB;""")

for table_name in tables:
    table_frame = tables[table_name]
    try:
        cursor.execute(table_frame)
        print("Table '{}' is created and ready for use.".format(table_name))
    except mysql.connector.Error as err:
        if err.errno == mysql.connector.errorcode.ER_TABLE_EXISTS_ERROR:
            print("Table '{}' is ready for use.".format(table_name))
        else:
            print(err.msg)

insert_attractions_data = textwrap.dedent("""\
    INSERT INTO attractions
    (attrac_id, name, category, description, address, transport, mrt, lat, lng, images)
    VALUES (%(attrac_id)s, %(name)s, %(category)s, %(description)s, %(address)s, 
    %(transport)s, %(mrt)s, %(lat)s, %(lng)s, %(images)s);
    """)
insert_files_data = textwrap.dedent("""\
    INSERT INTO files
    (attrac_id, link_path, extention, type)
    VALUES (%(attrac_id)s, %(link_path)s, %(extention)s, %(type)s);
    """)

for i in attractions_data():
    # print(i)
    cursor.execute(insert_attractions_data, i)
    cnx.commit()
print("Inserting attractions data is completed.")

for i in files_data():
    cursor.execute(insert_files_data, i)
    cnx.commit()
print("Inserting files data is completed.")
