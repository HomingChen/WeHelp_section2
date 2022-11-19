import json
from flask import *
import sql
app=Flask(__name__)
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

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
		if keyword == None or "":
			print("get_attractions")
			data = sql.get_attractions(page=page)
		else:
			print("get_attractions_with_keyword")
			data = sql.get_attractions_with_keyword(page=page, keyword=keyword)
		return jsonify(data)
	except:
		return jsonify({"error": True, "message": "請重新輸入。"})	

@app.route("/api/attraction/<attractionID>")
def get_attraction_with_ID(attractionID):
	try:
		data = sql.get_attraction_with_ID(attractionID)
		return jsonify(data)
	except:
		message = "請按照情境提供對應的錯誤訊息"
		return jsonify({"error": True, "message": message})

@app.route("/api/categories")
def get_categories():
	try: 
		data = sql.get_categories()
		return jsonify(data)
	except:
		message = "請按照情境提供對應的錯誤訊息"
		return jsonify({"error": True, "message": message})

app.run(port=3000)