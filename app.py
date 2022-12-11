from flask import *
import jwt
import sql
import re

app=Flask(__name__)
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
key = "welovepongpong"

# Pages
@app.route("/")
def index():
	return render_template("index.html")
@app.route("/attraction/<id>")
def attraction(id):
	return render_template("attraction.html")
@app.route("/booking")
def booking():
	return render_template("booking.html")
@app.route("/thankyou")
def thankyou():
	return render_template("thankyou.html")

# APIs
@app.route("/api/attractions")
def get_attractions():
	try:
		page = request.args.get("page")
		keyword = request.args.get("keyword")
		print(keyword)
		data = sql.get_attractions(page=page, keyword=keyword)["data"]
		return jsonify(data), 200
	except:
		return jsonify({"error": True, "message": "內部伺服器錯誤"}), 500

@app.route("/api/attraction/<attractionID>")
def get_attraction_with_ID(attractionID):
	try:
		response = sql.get_attraction_with_ID(attractionID)
		if response["result"]==True:
			return jsonify(response["data"]), 200
		else:
			return jsonify({"error": True, "message": "景點編號不正確"}), 400
	except:
		return jsonify({"error": True, "message": "內部伺服器錯誤"}), 500

@app.route("/api/categories")
def get_categories():
	try:
		response = sql.get_categories()
		if response["result"]==True:
			return jsonify(response["data"]), 200
	except:
		return jsonify({"error": True, "message": "內部伺服器錯誤"}), 500

@app.route("/api/user", methods=["POST"])
def register():
	try:
		sign_up_data = request.get_json()
		if False in [isNameValid(sign_up_data["name"]), isEmailValid(sign_up_data["email"]), isPasswordValid(sign_up_data["password"])]:
			return {"error": True, "message": "註冊失敗，重複的 Email 或其他原因"}, 400
		else:
			result = sql.member_sign_up(sign_up_data)
			if result["result"] == True:
				return {"ok": True}, 200
			else:
				return {"error": True, "message": "註冊失敗，重複的 Email 或其他原因"}, 400
	except:
		return {"error": True, "message": "伺服器內部錯誤"}, 500

def isNameValid(name):
	if len(name)>0 & len(name)<=100:
		return True
	else:
		return False

def isEmailValid(email):
	regex_check_result = re.match(r"[^@]+@[^@]+", email).group(0)
	if len(regex_check_result)==len(email) & len(email)<=100:
		return True
	else:
		return False

def isPasswordValid(password):
	if len(password)>=8 & len(password)<=32:
		return True
	else:
		return False

@app.route("/api/user/auth", methods=["GET"])
def userStatusCheck():
	cookie = request.cookies.to_dict()
	try: 
		userStatus = jwt.decode(jwt=cookie["status"], key=key, algorithms="HS256")
		if userStatus["id"]==sql.get_member_data_by_email(userStatus["email"])["data"]["member_id"]:
			return {"data": userStatus}, 200
		else:
			return {"data": None}, 200
	except:
		return {"data": None}, 200

@app.route("/api/user/auth", methods=["PUT"])
def login():
	try:
		login_data = request.get_json()
		query_response = sql.get_member_data_by_email(login_data["email"])
		if query_response["result"]==False:
			return {"error": True, "message": "登入失敗，帳號或密碼錯誤或其他原因"}, 400
		elif query_response["data"]["password"]!=login_data["password"]:
			return {"error": True, "message": "登入失敗，帳號或密碼錯誤或其他原因"}, 400
		elif query_response["data"]["password"]==login_data["password"]:
			response_data = {"id": query_response["data"]["member_id"], 
				"name": query_response["data"]["name"], "email": query_response["data"]["email"]}
			response_cookie_encoded = jwt.encode(response_data, key, "HS256")					# 此處的key是指加密的key
			response = make_response({"ok": True})
			response.set_cookie(key="status", value=response_cookie_encoded, max_age=604800)	# 此處的key是指cookie的key
			return response, 200
	except:
		return {"error": True, "message": "伺服器內部錯誤"}, 500

@app.route("/api/user/auth", methods=["DELETE"])
def logout():
	response = make_response({"ok": True})
	response.set_cookie(key="status", value="", max_age=-1)
	return response, 200

app.run(host="0.0.0.0", port=3000)