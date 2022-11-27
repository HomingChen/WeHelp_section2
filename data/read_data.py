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
            "lng":          attractions[i]["longitude"]
        })
    return attractions_data

def files_data(data_path="taipei-attractions.json"):
    with open(data_path, encoding="utf-8") as data_file:
        data = json.load(data_file)
    attractions = data["result"]["results"]
    files_data = []
    for i in range(0, len(attractions)):
        each_file_rawString = attractions[i]["file"]
        each_file_path = re.findall(r"(https.+?)(?=https|$)", each_file_rawString)
        each_file_extention = re.findall(r"\.([A-Za-z0-9]+?)(?=https|$)", each_file_rawString)
        for path, ext in zip(each_file_path, each_file_extention):
            if str(ext).lower()=="jpg":
                each_file_type = "image"
            elif str(ext).lower()=="mp3":
                each_file_type = "audio"
            elif str(ext).lower()=="flv":
                each_file_type = "video"
            else:
                each_file_type = "undefined"
            files_data.append({
                "attrac_id": attractions[i]["_id"],
                "type": each_file_type,
                "extention": ext,
                "path": path
            })
    return files_data

def category_data(data_path="taipei-attractions.json"):
    with open(data_path, encoding="utf-8") as data_file:
        data = json.load(data_file)
    attractions = data["result"]["results"]
    category_list = []
    for i in range(0, len(attractions)):
        each_attraction_cat = attractions[i]["CAT"]
        category_list.append(each_attraction_cat)
    category_data = list(dict.fromkeys(category_list))
    return category_data



# """ columns infromation about taipei-attractions.json and mapping for MySQL DB column name
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

# """ data without data normalization as api offered
# def attractions_data(data_path="taipei-attractions.json"):
#     with open(data_path, encoding="utf-8") as data_file:
#         data = json.load(data_file)
#     attractions = data["result"]["results"]
#     attractions_data = []
#     for i in range(0, len(attractions)):
#         each_attraction_info = {
#             "attrac_id":    attractions[i]["_id"],
#             "name":         attractions[i]["name"],
#             "category":     attractions[i]["CAT"],
#             "description":  attractions[i]["description"],
#             "address":      attractions[i]["address"],
#             "transport":    attractions[i]["direction"],
#             "mrt":          attractions[i]["MRT"],
#             "lat":          attractions[i]["latitude"],
#             "lng":          attractions[i]["longitude"]
#         }
#         each_attraction_file = attractions[i]["file"]                                           # this section is the mainly different part:
#         each_attraction_images = re.findall(r".+?[JPG|jpg](?=https|$)", each_attraction_file)   # just take the extention is "jpg" or "JPG" path
#         each_attraction_info["images"] = json.dumps(each_attraction_images)                     # combine as a json array
#         attractions_data.append(each_attraction_info)                                           # append to the attraction so that each attraction will have a array of image from file
#     return attractions_data
# """