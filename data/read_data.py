import json
import re

def attractions_data(data_path="taipei-attractions.json"):
    with open(data_path, encoding="utf-8") as data_file:
        data = json.load(data_file)
    attractions = data["result"]["results"]
    attractions_data = []
    for i in range(0, len(attractions)):
        attractions_data.append({
            "attrac_id":    attractions[i]["_id"],
            "name":         attractions[i]["name"],
            "category":     attractions[i]["CAT"],
            "description":  attractions[i]["description"],
            "address":      attractions[i]["address"],
            "transport":    attractions[i]["direction"],
            "mrt":          attractions[i]["MRT"],
            "lat":          attractions[i]["latitude"],
            "lng":          attractions[i]["longitude"],
            "images":       re.match(r"https.+?\.(jpg|JPG|png|PNG)(?=(https|$))", attractions[i]["file"]).group(0)
        })
    # print(attractions_data)
    return attractions_data

def files_data(data_path="taipei-attractions.json"):
    with open(data_path, encoding="utf-8") as data_file:
        data = json.load(data_file)
    attractions = data["result"]["results"]
    attractions_files_data = []
    for i in range(0, len(attractions)):
        file_rawString = attractions[i]["file"]
        file_path = re.findall(r"(https.+?)(?=https|$)", file_rawString)
        file_extention = re.findall(r"\.([A-Za-z0-9]+?)(?=https|$)", file_rawString)
        for path, ext in zip(file_path, file_extention):
            if str(ext).lower()=="jpg":
                file_type = "image"
            elif str(ext).lower()=="mp3":
                file_type = "audio"
            elif str(ext).lower()=="flv":
                file_type = "video"
            else:
                file_type = "undefined"
            attractions_files_data.append({
                "attrac_id": attractions[i]["_id"],
                "link_path": path,
                "extention": ext,
                "type": file_type
            })
    # print(attractions_files_data)
    return attractions_files_data

data = attractions_data()
print(data[2]["lat"])

# """
# i,  [json_dic_name],[note],                                     [DB_column_name]
# 1,  rate,           rating score from 1 to 5,                   x
# 2,  direction,      direction,                                  transport
# 3,  name,           name,                                       name
# 4,  date,           not defined date,                           x
# 5,  longitude,      longitude,                                  lng
# 6,  REF_WP,         not defined yet,                            x
# 7,  avBegin,        not defined date,                           x
# 8,  langinfo,       not defined number (10),                    x
# 9,  MRT,            MRT station nearby,                         mrt
# 10, SERIAL_NO,      serial number with 16 digit unique number,  x
# 11, RowNumber,      the same as id (strating from 1 to 58),     id
# 12, CAT,            category,                                   category
# 13, MEMO_TIME,      opening time,                               x
# 14, POI,            point of interesting (Y),                   x
# 15, file,           related image or files,                     images
# 16, idpt,           not defined string (臺北旅遊網),             x
# 17, latitude,       latitude,                                   lat
# 18, description,    description,                                description
# 19, _id,            the same as id (strating from 1 to 58),     id
# 20, avEnd,          not defined date,                           x
# 21, address,        address,                                    address
# """