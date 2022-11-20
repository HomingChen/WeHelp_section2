import textwrap
import ast
import mysql.connector
from collections import namedtuple

cnx = mysql.connector.connect(host="localhost", user="root", password="!QAZ-2wsx", database="taipei_attractions")
cursor = cnx.cursor()

def error_message(message="請按照情境提供對應的錯誤訊息"):
    return {"error":True, "message": message}

def get_attractions(page):
    try:
        query = "SELECT * FROM attractions"
        cursor.execute(query)
        data = []
        for i in cursor.fetchall():
            result = namedtuple("data", cursor.column_names)._make(i)._asdict()
            result["images"] = ast.literal_eval(result["images"])
            data.append(result)
        effective_pages = len(data)/12
        page = int(page)
        if page>effective_pages:
            return error_message("請縮小搜尋頁數。")
        else:
            next_page = page+1
            first_item = 12*page
            last_item = min(12*next_page, len(data))
            return {"nextPage": next_page, "data": data[first_item : last_item]}
    except:
        return error_message("請重新輸入頁數。")

def get_attractions_with_keyword(page, keyword):
    try:
        query = textwrap.dedent("""
            SELECT * FROM attractions 
                WHERE category=%(keyword)s OR description LIKE %(keyword_like)s
                ORDER BY 
                CASE 
                    WHEN category LIKE %(keyword_like)s THEN 0 
                    ELSE 1 
                END;""")
        cursor.execute(query, params={"keyword": keyword, "keyword_like": "%"+keyword+"%"})
        data = []
        for i in cursor.fetchall():
            result = namedtuple("data", cursor.column_names)._make(i)._asdict()
            result["images"] = ast.literal_eval(result["images"])
            data.append(result)
        effective_pages = len(data)/12
        page = int(page)
        if page>effective_pages:
            return error_message("請縮小搜尋頁數。")
        else:
            next_page = page+1
            first_item = 12*page
            last_item = min(12*next_page, len(data))
            return {"nextPage": next_page, "data": data[first_item : last_item]}
    except:
        return error_message("請重新輸入頁數。")

def get_attraction_with_ID(id):
    query = "SELECT * FROM attractions WHERE attrac_id=%(id)s"
    cursor.execute(query, params={"id": id})
    result = cursor.fetchone()
    data = namedtuple("data", cursor.column_names)._make(result)._asdict()
    data["images"] = ast.literal_eval(data["images"])
    return {"data": data}


def get_categories():
    try:
        query = "SELECT GROUP_CONCAT(DISTINCT category ORDER BY category DESC) FROM attractions;"
        cursor.execute(query)
        data = list(cursor.fetchone())
        return {"data": data}
    except:
        return error_message("請重新操作。")
