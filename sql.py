import textwrap
import ast
import mysql.connector
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
query_dictionary["get_attraction_wit_id"] = textwrap.dedent("""
    SELECT attractions.*, JSON_ARRAYAGG(files.path) AS images 
    FROM attractions LEFT JOIN files ON attractions.attrac_id=files.attrac_id 
    WHERE attractions.attrac_id=%(id)s AND files.type='image'; 
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
        print("get_attractions_with_page")
        query = query_dictionary["get_attractions_with_page"]
        parameters = {"start_row": int(page)*12}
    else:
        print("get_attractions_with_page_n_keyword")
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
    query = query_dictionary["get_attraction_wit_id"]
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
    query = "INSERT INTO members (name, email, password) VALUES (%(name)s, %(email)s, %(password)s)"
    parameters = sign_up_data
    response = insert_data(query, parameters)
    if response["result"]==True:
        return {"result": True, "data": response["data"]}
    else:
        return {"result": False, "data": response["data"]}