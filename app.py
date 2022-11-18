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
def getAttractions():
	page = int(request.args.get("page"))
	keyword = str(request.args.get("keyword"))
	result = sql.getAttractions(page=page, keyword=keyword)
	return jsonify(result)

@app.route("/api/attraction/<attractionID>")
def getAttractionWithID(attractionID):
	result = sql.getAttractionWithID(attractionID)
	return jsonify(result)
	# return jsonify({"error": True, "message": attractionID})

@app.route("/api/categories")
def getCategories():
	try: 
		categories = ["string"]
		return jsonify({"data:": categories})
	except:
		message = "請按照情境提供對應的錯誤訊息"
		return jsonify({"error": True, "message": message})

app.run(port=3000)