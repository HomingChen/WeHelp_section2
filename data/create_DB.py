import textwrap
import mysql.connector
from mysql.connector import errorcode
from read_data import attractions_data, files_data

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

### use attractions table
create_attractions_table = textwrap.dedent("""\
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
        INDEX indexes(name, category, mrt)
    ) ENGINE=InnoDB;""")
try:
    cursor.execute(create_attractions_table)
    print("Table 'attractions' is created and ready for use.")
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
        print("Table 'attractions' is ready for use.")
    else:
        print(err.msg)

### insert attractions data
insert_attractions_data = textwrap.dedent("""\
    INSERT INTO attractions
    (attrac_id, name, category, description, address, transport, mrt, lat, lng)
    VALUES (%(attrac_id)s, %(name)s, %(category)s, %(description)s, %(address)s, 
    %(transport)s, %(mrt)s, %(lat)s, %(lng)s);
    """)
try:
    for i in attractions_data():
        cursor.execute(insert_attractions_data, params=i)
        cnx.commit()
    print("Inserting attractions data is completed.")
except mysql.connector.Error as err:
    if err.errno == 1062:
        print("Data 'attractions' is ready for use.")
    else:
        print(err.msg)

### use files data
create_files_table = textwrap.dedent("""\
    CREATE TABLE files(
        file_id        BIGINT UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT,
        attrac_id      BIGINT UNSIGNED NOT NULL,
        type           ENUM('image', 'audio', 'video', 'undefined') NOT NULL,
        extention      VARCHAR(10) NOT NULL,
        path           VARCHAR(500) UNIQUE NOT NULL ,
        FOREIGN KEY(attrac_id) REFERENCES attractions(attrac_id), 
        INDEX indexes(attrac_id, type, extention)
    ) ENGINE=InnoDB;""")
try:
    cursor.execute(create_files_table)
    print("Table 'files' is created and ready for use.")
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
        print("Table 'files' is ready for use.")
    else:
        print(err.msg)

### insert files data
insert_files_data = textwrap.dedent("""
    INSERT INTO files (attrac_id, type, extention, path)
    VALUES (%(attrac_id)s, %(type)s, %(extention)s, %(path)s);
    """)
try:
    for i in files_data():
        cursor.execute(insert_files_data, params=i)
        cnx.commit()
        print("Inserting files data is completed.")
except mysql.connector.Error as err:
    if err.errno == 1062:
        print("Data 'files' is ready for use.")
    else:
        print(err.msg)

### use member data
create_members_table = textwrap.dedent("""
    CREATE TABLE members(
        member_id   BIGINT UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT,
        name        VARCHAR(100) NOT NULL,
        email       VARCHAR(100) UNIQUE NOT NULL,
        password    VARCHAR(32) NOT NULL,
        INDEX indexes(name, email)
    ) ENGINE=InnoDB;""")
try:
    cursor.execute(create_members_table)
    print("Table 'members' is created and ready for use.")
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
        print("Table 'members' is ready for use.")
    else:
        print(err.msg)

### use contact information data
create_contact_info_table = textwrap.dedent("""
    CREATE TABLE contact_info(
        contact_id      BIGINT UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT,
        member_id       BIGINT UNSIGNED NOT NULL,
        contact_name    VARCHAR(100) NOT NULL,
        contact_email   VARCHAR(100) NOT NULL,
        phone           VARCHAR(10) NOT NULL,
        FOREIGN KEY(member_id) REFERENCES members(member_id),
        INDEX indexes(member_id, contact_email, phone)
    ) ENGINE=InnoDB;""")
insert_contact_info_data = textwrap.dedent("""
    INSERT INTO contact_info (member_id, contact_name, contact_email, phone) 
        VALUES (%(member_id)s, %(contact_name)s, %(contact_email)s, %(phone)s);""")
try:
    cursor.execute(create_members_table)
    print("Table 'contact_info' is created and ready for use.")
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
        print("Table 'contact_info' is ready for use.")
    else:
        print(err.msg)

### use order data
create_orders_table = textwrap.dedent("""
    CREATE TABLE orders(
        order_id    BIGINT UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT,
        attrac_id   BIGINT UNSIGNED NOT NULL,
        tour_date   DATE NOT NULL,
        time_slot   ENUM('morning', 'afternoon') NOT NULL,
        expense     SMALLINT UNSIGNED NOT NULL,
        member_id   BIGINT UNSIGNED NOT NULL,
        order_date  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(attrac_id) REFERENCES attractions(attrac_id), 
        FOREIGN KEY(member_id) REFERENCES members(member_id),
        INDEX indexes(attrac_id, tour_date, time_slot, member_id)
    ) ENGINE=InnoDB;""")
try:
    cursor.execute(create_members_table)
    print("Table 'orders' is created and ready for use.")
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
        print("Table 'orders' is ready for use.")
    else:
        print(err.msg)

### use cancelled data
create_cancelled_orders_table = textwrap.dedent("""
    CREATE TABLE cancelled_orders(
        cancel_id       BIGINT UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT,
        order_id        BIGINT UNSIGNED NOT NULL,
        cancelled_date  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(order_id) REFERENCES orders(order_id),
        INDEX indexes(order_id)
    ) ENGINE=InnoDB;""")
try:
    cursor.execute(create_members_table)
    print("Table 'cancelled_orders' is created and ready for use.")
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
        print("Table 'cancelled_orders' is ready for use.")
    else:
        print(err.msg)

### use payment data
create_papment_table = textwrap.dedent("""
    CREATE TABLE payment(
        payment_id  BIGINT UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT,
        order_id    BIGINT UNSIGNED NOT NULL,
        contact_id  BIGINT UNSIGNED NOT NULL,
        card_id     VARCHAR(16) NOT NULL,
        pay_date    DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(order_id) REFERENCES orders(order_id),
        FOREIGN KEY(contact_id) REFERENCES contact_info(contact_id),
        INDEX indexes(order_id, contact_id, card_id)
    ) ENGINE=InnoDB;""")

