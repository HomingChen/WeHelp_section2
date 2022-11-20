import textwrap
import ast
import mysql.connector
from collections import namedtuple

cnx = mysql.connector.connect(host="localhost", user="root", password="!QAZ-2wsx", database="taipei_attractions")
cursor = cnx.cursor()

def get_attractions(page):
    strat_row = int(page)*12
    query = "SELECT * FROM attractions ORDER BY attrac_id LIMIT %(start_row)s,12;"
    cursor.execute(query, params={"start_row": strat_row})
    data = []
    for i in cursor.fetchall():
        result = namedtuple("data", cursor.column_names)._make(i)._asdict()
        result["images"] = ast.literal_eval(result["images"])
        data.append(result)
    next_page = None if len(data)<12 else int(page)+1
    return {"nextPage": next_page, "data": data}

def get_attractions_with_keyword(page, keyword):
    start_row = int(page)*12
    query = textwrap.dedent("""
        SELECT * FROM attractions 
            WHERE category=%(keyword)s OR description LIKE %(keyword_like)s
            ORDER BY 
            CASE 
                WHEN category LIKE %(keyword_like)s THEN 0 
                ELSE 1 
            END
            LIMIT %(start_row)s,12;""")
    cursor.execute(query, params={"keyword": keyword, "keyword_like": "%"+keyword+"%", "start_row": start_row})
    data = []
    for i in cursor.fetchall():
        result = namedtuple("data", cursor.column_names)._make(i)._asdict()
        result["images"] = ast.literal_eval(result["images"])
        data.append(result)
    next_page = None if len(data)<12 else int(page)+1
    return {"nextPage": next_page, "data": data}

def get_attraction_with_ID(id):
    query = "SELECT * FROM attractions WHERE attrac_id=%(id)s"
    cursor.execute(query, params={"id": id})
    result = cursor.fetchone()
    data = namedtuple("data", cursor.column_names)._make(result)._asdict()
    data["images"] = ast.literal_eval(data["images"])
    return {"data": data}

def get_categories():
    query = "SELECT DISTINCT category FROM attractions ORDER BY CASE WHEN category='其　　他' THEN 1 ELSE 0 END;"
    cursor.execute(query)
    result = cursor.fetchall()
    data = []
    [data.append(i[0]) for i in result]
    return {"data": data}