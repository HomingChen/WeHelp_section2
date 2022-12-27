from flask import *
import ast
import jwt
import sql
import re
import requests
from datetime import datetime

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
	try:
		orderNumber = request.args.get("number")
		responseData = getPaymentResultByOrderID(orderNumber)[0]
		return render_template("thankyou.html", data=responseData)
	except:
		return render_template("index.html")

# APIs
@app.route("/api/attractions")
def get_attractions():
	try:
		page = request.args.get("page")
		keyword = request.args.get("keyword")
		# print(keyword)
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
			response_data = {
				"id": query_response["data"]["member_id"], 
				"name": query_response["data"]["name"], 
				"email": query_response["data"]["email"]}
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

@app.route("/api/booking", methods=["GET"])
def getOrderData():
	try:
		memberData = userStatusCheck()
		if memberData[0]["data"]==None:
			return {"error": True, "message": "未登入系統，拒絕存取"}, 403
		else:
			orderData = sql.get_last_unpaid_order_by_member_id(memberData[0]["data"]["id"])
			# if orderData["data"][0]["pay_status"]==0:
			# 	redirectUrl = "/thankyou?number=" + str(orderData["data"][0]["order_id"])
			# 	return redirect(url_for("thankyou", number=orderData["data"][0]["order_id"]))
			if orderData["result"]==True:
				data = {
					"attraction": {
						"id": orderData["data"][0]["attrac_id"],
						"name": orderData["data"][0]["name"],
						"address": orderData["data"][0]["address"],
						"image": ast.literal_eval(orderData["data"][0]["images"])[0]
					},
					"date": str(orderData["data"][0]["tour_date"]),
					"time": orderData["data"][0]["time_slot"],
					"price": orderData["data"][0]["expense"] 
				}
				return {"data": data}, 200
			else:
				return {"data": None}, 200
	except:
		return {"error": True, "message": "伺服器內部錯誤"}, 500

@app.route("/api/booking", methods=["POST"])
def insertANewOrder():
	try:
		memberData = userStatusCheck()
		if memberData[0]["data"]==None:
			return {"error": True, "message": "未登入系統，拒絕存取"}, 403
		else:
			newOrderData = request.get_json()
			newOrderData["member_id"] = memberData[0]["data"]["id"]
			checkNewOrderData = [
				isTourDateValid(newOrderData["date"]),
				isTimeSlotValid(newOrderData["time"]),
				isExpenseValid(newOrderData["price"])
				]
			if False in checkNewOrderData:
				return {"error": True, "message": "建立失敗，輸入不正確或其他原因"}, 400
			else:
				query_response = sql.insert_a_new_order(newOrderData)
				if query_response["result"]==True:
					return {"ok": True}, 200
				else:
					return {"error": True, "message": "伺服器內部錯誤"}, 500
	except:
		return {"error": True, "message": "伺服器內部錯誤"}, 500

def isTourDateValid(tourDate):
	if len(tourDate)>0:
		return True
	else:
		return False

def isTimeSlotValid(timeSlot):
	if timeSlot=="morning" or timeSlot=="afternoon":
		return True
	else:
		return False

def isExpenseValid(expense):
	if len(expense)>0:
		return True
	else:
		return False

@app.route("/api/booking", methods=["DELETE"])
def cancelledAnOrder():
	try:
		memberData = userStatusCheck()
		if memberData[0]["data"]==None:
			return {"error": True, "message": "未登入系統，拒絕存取"}, 403
		else:
			orderData = sql.get_valid_orders_by_member_id(memberData[0]["data"]["id"])
			if orderData["result"]==True:
				for i in orderData["data"]:
					if i["cancel_id"]==None:
						sql.cancelled_an_order(i["order_id"])
						# print("order_id:", i["order_id"], "is cancelled.")
			return {"ok": True}
	except:
		return {"error": True, "message": "伺服器內部錯誤"}, 500

@app.route("/api/order/<orderNumber>", methods=["GET"])
def getPaymentResultByOrderID(orderNumber):
	try:
		memberData = userStatusCheck()
		if memberData[0]["data"]==None:
			return {"error": True, "message": "未登入系統，拒絕存取"}, 403
		else:
			paymentResult = sql.get_payment_result_by_order_id(orderNumber)["data"][0]
			paymentResultData = {
				"number": paymentResult["order_id"],
				"price": paymentResult["expense"],
				"trip": {
					"attraction": {
						"id": paymentResult["attrac_id"],
						"name": paymentResult["name"],
						"address": paymentResult["address"],
						"image": paymentResult["image"]
					},
					"date": paymentResult["tour_date"],
					"time": paymentResult["time_slot"]
				},
				"contact": {
					"name": paymentResult["contact_name"],
					"email": paymentResult["contact_email"],
					"phone": paymentResult["phone"],
				},
				"status": paymentResult["pay_status"]
			}
			return {"data": paymentResultData}, 200
	except:
		return {"error": True, "message": "伺服器內部錯誤"}, 500

@app.route("/api/order", methods=["POST"])
def payOrder():
	try:
		memberData = userStatusCheck()
		if memberData[0]["data"]==None:
			return {"error": True, "message": "未登入系統，拒絕存取"}, 403
		else:
			orderData = request.get_json()
			contactData = {
				"member_id": memberData[0]["data"]["id"], 
				"name": orderData["contact"]["name"], 
				"email": orderData["contact"]["email"], 
				"phone": orderData["contact"]["phone"]
			}
			checkContact = [
				isNameValid(contactData["name"]),
				isEmailValid(contactData["email"]),
				isPhoneValid(contactData["phone"])
			]
			if False in checkContact:
				return {"error": True, "message": "訂單建立失敗，輸入不正確或其他原因"}, 400
			else:
				orderID = sql.get_valid_orders_by_member_id(memberData[0]["data"]["id"])["data"][0]["order_id"]
				paymentResult = isPaymentValid(orderData)
				if paymentResult["result"]==True:
					isContactDuplicated = sql.is_contact_info_duplicated(contactData)
					if isContactDuplicated["result"]==False:
						insertANewContactInfo = sql.insert_a_contact_info(contactData)
						contactID = insertANewContactInfo["data"][0]["contact_id"]
					else:
						contactID = isContactDuplicated["data"][0]["contact_id"]
					paymentRecord = {
						"order_id": orderID,
						"contact_id": contactID,
						"card_last_four": paymentResult["data"]["card_last_four"],
						"pay_status": paymentResult["data"]["status"],
						"pay_time": datetime.now()
					}
					sql.insert_a_payment_record(paymentRecord)
					paymentData = {
						"number": orderID,
						"payment": {
							"status": 0,
							"message": "付款成功"
						}
					}
					return {"data": paymentData}, 200
				else:
					return {"error": True, "message": "訂單建立失敗，輸入不正確或其他原因"}, 400
	except:
		return {"error": True, "message": "伺服器內部錯誤"}, 500

def isPhoneValid(phone):
	phone = phone.replace("-", "").replace(" ", "").replace("+886", "0")
	regex_check_result = re.match(r"[0-9]+", phone).group(0)
	if len(regex_check_result)==10:
		return True
	else:
		return False

def isPaymentValid(orderData):
	tapPayUrl = "https://sandbox.tappaysdk.com/tpc/payment/pay-by-prime"
	header = {
		"Content-Type": "application/json",
		"x-api-key": "partner_FFbAEZRzftTUwzITWVoUAaLaZyTy7hGZZKSIT7SIiHfQCQyLRMi84eQI"
	}
	body = {
		"prime": orderData["prime"],
		"partner_key": "partner_FFbAEZRzftTUwzITWVoUAaLaZyTy7hGZZKSIT7SIiHfQCQyLRMi84eQI",
		"merchant_id": "homing_TAISHIN",
		"amount": orderData["order"]["price"],
		"currency": "TWD",
		"details": "TapPay Test",
		"cardholder": {
			"phone_number": orderData["contact"]["phone"],
			"name": orderData["contact"]["name"],
			"email": orderData["contact"]["email"]
		},
		"remember": False,
		# "three_domain_secure": True,
		# "result_url": {
		# 	"frontend_redirect_url": "https://www.google.com/"
		# }
	}
	payment = requests.post(tapPayUrl, headers=header, data=json.dumps(body), timeout=30)
	paymentResult = json.loads(payment.text)
	if paymentResult["status"]==0:
		return {"result": True, "data": {"status": paymentResult["status"], "card_last_four":paymentResult["card_info"]["last_four"]}}
	else:
		return {"result": False, "data": None}

app.run(host="0.0.0.0", port=3000)