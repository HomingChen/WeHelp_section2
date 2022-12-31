import textwrap
import ast
import mysql.connector
import datetime
from collections import namedtuple

query_dictionary = {}
query_dictionary["get_attractions_with_page"] = textwrap.dedent("""
    SELECT filtered_attractions.*, filtered_files.images
    FROM 
        (SELECT * FROM attractions ORDER BY attrac_id LIMIT %(start_row)s, 13
        ) AS filtered_attractions 
    LEFT JOIN 
        (SELECT attrac_id, JSON_ARRAYAGG(path) AS images 
            FROM files WHERE type='image' 
            GROUP BY attrac_id
        ) AS filtered_files 
    ON filtered_files.attrac_id=filtered_attractions.attrac_id;
    """)
query_dictionary["get_attractions_with_page_n_keyword"] = textwrap.dedent("""
    SELECT filtered_attractions.*, filtered_files.images
        FROM 
            (SELECT * FROM attractions 
                WHERE category=%(keyword)s OR description LIKE %(keyword_like)s 
                ORDER BY 
                    CASE 
                        WHEN category LIKE %(keyword_like)s THEN 0
                        WHEN category='其　　他' THEN 2
                        ELSE 1
                    END
                LIMIT %(start_row)s, 13
            ) AS filtered_attractions 
        LEFT JOIN 
            (SELECT attrac_id, JSON_ARRAYAGG(path) AS images 
                FROM files WHERE type='image' 
                GROUP BY attrac_id
            ) AS filtered_files 
        ON filtered_files.attrac_id=filtered_attractions.attrac_id;
    """)
query_dictionary["get_attraction_with_id"] = textwrap.dedent("""
    SELECT attractions.*, JSON_ARRAYAGG(files.path) AS images 
    FROM attractions LEFT JOIN files ON attractions.attrac_id=files.attrac_id 
    WHERE attractions.attrac_id=%(id)s AND files.type='image'; 
    """)
query_dictionary["insert_a_new_order"] = textwrap.dedent("""
    INSERT INTO orders (attrac_id, tour_date, time_slot, expense, member_id) 
        VALUES (%(attractionID)s, %(date)s, %(time)s, %(price)s, %(member_id)s);
    """)
query_dictionary["get_valid_orders_by_member_id"] = textwrap.dedent("""
    SELECT orders.*, cancelled_orders.cancel_id, attractions.name, attractions.address, JSON_ARRAYAGG(files.path) AS images, payment.pay_status
        FROM orders 
            LEFT JOIN cancelled_orders ON orders.order_id = cancelled_orders.order_id 
            LEFT JOIN attractions ON orders.attrac_id = attractions.attrac_id
            LEFT JOIN files ON orders.attrac_id = files.attrac_id
            LEFT JOIN payment ON orders.order_id = payment.order_id
        WHERE orders.member_id = %(member_id)s AND cancelled_orders.cancel_id IS NULL AND files.type = 'image';
    """)
query_dictionary["get_last_unpaid_order_by_member_id"] = textwrap.dedent("""
    SELECT orders.*, cancelled_orders.cancel_id, attractions.name, attractions.address, JSON_ARRAYAGG(files.path) AS images, payment.pay_status
        FROM orders 
            LEFT JOIN cancelled_orders ON orders.order_id = cancelled_orders.order_id 
            LEFT JOIN attractions ON orders.attrac_id = attractions.attrac_id
            LEFT JOIN files ON orders.attrac_id = files.attrac_id
            LEFT JOIN payment ON orders.order_id = payment.order_id
        WHERE orders.member_id = %(member_id)s AND cancelled_orders.cancel_id IS NULL AND files.type = 'image' AND payment.pay_status IS NULL 
        ORDER BY order_id DESC LIMIT 1;
    """)
query_dictionary["insert_a_cancelled_order"] = "INSERT INTO cancelled_orders (order_id) VALUES (%(order_id)s);"
query_dictionary["get_contact_info_by_member_id_name_email_phone"] = textwrap.dedent("""
    SELECT * FROM contact_info 
        WHERE member_id=%(member_id)s AND contact_name=%(name)s AND contact_email=%(email)s AND phone=%(phone)s;
    """)
query_dictionary["insert_a_contact_info"] = textwrap.dedent("""
    INSERT INTO contact_info (member_id, contact_name, contact_email, phone) 
        VALUES (%(member_id)s, %(name)s, %(email)s, %(phone)s);
    """)
query_dictionary["insert_a_payment_record"] = textwrap.dedent("""
    INSERT INTO payment(order_id, contact_id, card_last_four, pay_status, pay_time) 
        VALUES (%(order_id)s, %(contact_id)s, %(card_last_four)s, %(pay_status)s, %(pay_time)s);
    """)
query_dictionary["get_payment_result_by_order_id"] = textwrap.dedent("""
    SELECT order_data.*, attraction_data.name, attraction_data.address, attraction_data.image
        FROM 
            (SELECT payment.*, contact_info.contact_name, contact_info.contact_email, contact_info.phone, 
                orders.attrac_id, orders.tour_date, orders.time_slot, orders.expense
            FROM payment
                LEFT JOIN contact_info ON payment.contact_id = contact_info.contact_id
                LEFT JOIN orders ON payment.order_id = orders.order_id
            WHERE orders.order_id = %(order_id)s
            ) AS order_data
        INNER JOIN 
            (SELECT orders.order_id, attractions.name, attractions.address, files.path AS image 
            FROM orders
                LEFT JOIN attractions ON orders.attrac_id = attractions.attrac_id
                LEFT JOIN files ON files.attrac_id = orders.attrac_id
            WHERE orders.order_id = %(order_id)s
            ORDER BY order_id LIMIT 1
            ) AS attraction_data
        ON order_data.order_id = attraction_data.order_id;
    """)

def query_data(query, parameters=None):
    try:
        cnx = mysql.connector.connect(host="localhost", user="root", password="!QAZ-2wsx", database="taipei_attractions")
        cursor = cnx.cursor()
        cursor.execute(operation=query, params=parameters)
        response = cursor.fetchall()
        if len(response)==0:
            cursor.close()
            cnx.close()
            return {"result": False, "data": None}
        elif len(response)==1 & all(i is None for i in response[0]):
            cursor.close()
            cnx.close()
            return {"result": False, "data": None}
        else:
            data = []
            for i in response:
                item = namedtuple("response", cursor.column_names)._make(i)._asdict()
                data.append(item)
            cursor.close()
            cnx.close()
            return {"result": True, "data": data}
    except mysql.connector.Error as err:
        return {"result": False, "data": err}

def insert_data(query, parameters):
    try:
        cnx = mysql.connector.connect(host="localhost", user="root", password="!QAZ-2wsx", database="taipei_attractions")
        cursor = cnx.cursor()
        cursor.execute(operation=query, params=parameters)
        cnx.commit()
        cursor.close()
        cnx.close()
        return {"result": True, "data": "successfully add an item: "+str(parameters)}
    except mysql.connector.Error as err:
        return {"result": False, "data": err}

def get_attractions(page, keyword=None):
    if keyword==None or len(keyword)==0:
        query = query_dictionary["get_attractions_with_page"]
        parameters = {"start_row": int(page)*12}
    else:
        query = query_dictionary["get_attractions_with_page_n_keyword"]
        parameters = {"keyword": keyword, "keyword_like": "%"+keyword+"%", "start_row": int(page)*12}
    response = query_data(query, parameters)
    data = []
    for i in response["data"]:
        sub_item = dict(i)
        sub_item["id"] = sub_item.pop("attrac_id")
        sub_item["images"] =  ast.literal_eval(sub_item["images"])
        data.append(sub_item)
    nextPage = None if len(data)<13 else int(page)+1
    return {"result": True, "data": {"nextPage": nextPage, "data": data[0:12]}}

def get_attraction_with_ID(id):
    query = query_dictionary["get_attraction_with_id"]
    parameters={"id": id}
    response = query_data(query, parameters)
    if response["result"]==False:
        return {"result": False, "data": "no matched data"}
    elif len(response["data"])>1:
        return {"result": False, "data": "there are more than one data with the same id"}
    elif len(response["data"])==1:
        data = dict(response["data"][0])
        data["id"] = data.pop("attrac_id")
        data["images"] = ast.literal_eval(data["images"])
        return {"result": True, "data": {"data": data}}

def get_categories():
    query = "SELECT DISTINCT category FROM attractions ORDER BY CASE WHEN category='其　　他' THEN 1 ELSE 0 END;"
    response = query_data(query)
    if response["result"]==True:
        data = []
        [data.append(i["category"]) for i in response["data"]]
        return {"result": True, "data": {"data": data}}
    else:
        return {"result": False, "data": response["data"]}

def get_member_data_by_email(email):
    query = "SELECT * FROM members WHERE email=%(email)s;"
    parameters = {"email": email}
    response = query_data(query, parameters)
    if response["result"]==False:
        return {"result": False, "data": "no matched data"} 
    elif len(response["data"])>1:
        return {"result": False, "data": "there are more than one data with the same email"}
    elif len(response["data"])==1:
        return {"result": True, "data": response["data"][0]}

def member_sign_up(sign_up_data):
    query = "INSERT INTO members (name, email, password) VALUES (%(name)s, %(email)s, %(password)s);"
    parameters = sign_up_data
    response = insert_data(query, parameters)
    if response["result"]==True:
        return {"result": True, "data": response["data"]}
    else:
        return {"result": False, "data": response["data"]}

def insert_a_new_order(new_order_data):
    query = query_dictionary["insert_a_new_order"]
    parameters = new_order_data
    response = insert_data(query, parameters)
    if response["result"]==True:
        return {"result": True, "data": {"ok": True}}
    else:
        return {"result": False, "data": response["data"]}

def get_valid_orders_by_member_id(member_id):
    query = query_dictionary["get_valid_orders_by_member_id"]
    parameters = {"member_id": member_id}
    response = query_data(query, parameters)
    if response["result"]==False:
        return {"result": False, "data": response["data"]}
    else:
        return {"result": True, "data": response["data"]}

def get_last_unpaid_order_by_member_id(member_id):
    query = query_dictionary["get_last_unpaid_order_by_member_id"]
    parameters = {"member_id": member_id}
    response = query_data(query, parameters)
    if response["result"]==False:
        return {"result": False, "data": response["data"]}
    else:
        return {"result": True, "data": response["data"]}

def cancelled_an_order(order_id):
    query = query_dictionary["insert_a_cancelled_order"]
    parameters = {"order_id": order_id}
    response = insert_data(query, parameters)
    if response["result"]==True:
        return {"result": True, "data": response["data"]}
    else:
        return {"result": False, "data": response["data"]}

def is_contact_info_duplicated(contactData):
    query = query_dictionary["get_contact_info_by_member_id_name_email_phone"]
    parameters = contactData
    response = query_data(query, parameters)
    if response["result"]==True:
        return {"result": True, "data": response["data"]}
    else:
        return {"result": False, "data": response["data"]}

def insert_a_contact_info(contactData):
    query = query_dictionary["insert_a_contact_info"]
    parameters = contactData
    response = insert_data(query, parameters)
    print(response)
    if response["result"]==True:
        print("true")
        data = is_contact_info_duplicated(contactData)["data"]
        return {"result": True, "data": data}
    else:
        print("false")
        return {"result": False, "data": response["data"]}

def insert_a_payment_record(paymentRecord):
    query = query_dictionary["insert_a_payment_record"]
    parameters = paymentRecord
    response = insert_data(query, parameters)
    if response["result"]==True:
        return {"result": True, "data": response["data"]}
    else:
        return {"result": False, "data": response["data"]}

def get_payment_result_by_order_id(order_id):
    query = query_dictionary["get_payment_result_by_order_id"]
    parameters = {"order_id": order_id}
    response = query_data(query, parameters)
    if response["result"]==True:
        return {"result": True, "data": response["data"]}
    else:
        return {"result": False, "data": response["data"]}