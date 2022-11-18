import textwrap
import mysql.connector
from collections import namedtuple

cnx = mysql.connector.connect(host="localhost", user="root", password="7895123", database="taipei_attractions")
cursor = cnx.cursor()

def getAttractions(page=0, keyword=""):
    query = textwrap.dedent("""
        SELECT * FROM attractions 
            WHERE category=%(keyword)s OR description LIKE %(keyword_like)s
            ORDER BY 
                CASE 
                    WHEN category LIKE %(keyword_like)s THEN 0 
                    ELSE 1 
                END, attrac_id 
            LIMIT %(page)s,12;""")
    cursor.execute(query, params={"page": page, "keyword": keyword, "keyword_like": "%"+keyword+"%"})
    result = cursor.fetchall()
    data = []
    for i in result:
        attraction = namedtuple("getAttraction", cursor.column_names)._make(i)._asdict()
        data.append(attraction)
    # print(data)
    return {"nextPage": page+1, "data": data}
    # return data

def getAttractionWithID(id=0):
    print("received id={id} request.")
    query = "SELECT * FROM attractions WHERE attrac_id=%(id)s"
    cursor.execute(query, params={"id": id})
    print("excuting")
    result = cursor.fetchone()
    print(result)
    data = namedtuple("getAttractionWithID", cursor.column_names)._make(result)._asdict()
    print(data)
    return {"data": data}

# getAttractionWithID("1")
# getAttractions(page=0, keyword="藝文館所")