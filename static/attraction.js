import { memberView, memberModel, memberControl } from "/static/member.js";

const imgList = [];
const attracView = {
    renderImgRadioInputs(i){
        let imgListRadioTab = document.createElement("input");
        imgListRadioTab.setAttribute("name", "imgList");
        imgListRadioTab.setAttribute("type", "radio");
        imgListRadioTab.setAttribute("id", i);
        imgListRadioTab.setAttribute("alt", i);
        document.getElementById("imgList").appendChild(imgListRadioTab);
    },
    renderMainContent(data){
        document.getElementById("attraction").textContent = data["data"]["name"];
        document.getElementById("categorynMRT").textContent = `${data["data"]["category"]} at ${data["data"]["mrt"]}`;
        document.getElementById("description").textContent = data["data"]["description"];
        document.getElementById("address").textContent = data["data"]["address"];
        document.getElementById("transport").textContent = data["data"]["transport"];
    },
    updateCurrentImg(i, imgList){
        let currentImgTab = document.getElementById("currentImg");
        // 把目前圖片更新為前一張圖片
        let lastImgTab = document.getElementById("lastImg");
        let lastImgID = currentImgTab.alt;
        lastImgTab.setAttribute("alt", lastImgID);
        lastImgTab.setAttribute("src", imgList[lastImgID].src);
        // 把下一張圖片更新為目前的圖片
        currentImgTab.replaceWith(imgList[i]);
        document.getElementById(i).checked = true;
    },
    renderAnimationForChangingImg(wayToChangingImg){
        document.getElementById("currentImg").className = wayToChangingImg;   // previousImg, nextImg, pickImg
    },
};
const attracModel = {
    getAttracID(){
        let attracID = document.URL.match(/[0-9]+?$/)[0];
        return attracID;
    },
    stackImgs(i, imgSrc, imgList){
        let img = new Image();
        img.id = "currentImg";
        img.src = imgSrc;
        img.alt = i;
        imgList.push(img);
        return imgList;
    },
    async getAttracData(){
        return await fetch("/api/attraction/"+attracModel.getAttracID(), {"method": "GET"}
            ).then((response)=>{
                return response.json();
            }).catch((error)=>{
                console.log("function 'getAttracData' error:", error);
            });
    },
    collectBookingInput(){
        let response = {
            "attractionID": attracModel.getAttracID(), 
            "date": document.getElementById("tourDate").value, 
            "time": document.querySelector("input[name='timeSlot']:checked").value, 
            "price": document.getElementById("charge").innerText.match(/[0-9]+/)[0]
        };
        return response;
    },
    async getOrderData(){
        let result = await fetch("/api/booking", {
            method: "GET",
            headers: {"Cookie": document.cookie}
        }).then((response)=>{
            return response.json();
        }).then((data)=>{
            return data;
        }).catch((error)=>{
            console.log("function 'getOrderData' error:", error)
        });
        return result;
    },
    async cancelledAnOrder(){
        let result = await fetch("/api/booking", {
            method: "DELETE",
            headers: {"Cookie": document.cookie}
        }).then((response)=>{
            return response.json();
        }).then((data)=>{
            if("ok" in data){
                console.log("cancelled");
            };
            return true;
        }).catch((error)=>{
            console.log("function 'cancelledAnOrder' error:", error)
        });
        return result;
    },
    async initialNewBooking(bookingData){
        console.log(bookingData);
        let result = await fetch("/api/booking", {
            method: "POST",
            headers: {"Content-Type": "application/json", "Cookie": document.cookie},
            body: JSON.stringify(bookingData)
        }).then((response)=>{
            return response.json();
        }).then((data)=>{
            console.log(data);
            if("ok" in data){
                return {"result": true, "message": "建立成功"};
            }else{
                return {"result": false, "message": data["message"]}
            };
        }).catch((error)=>{
            console.log("function 'initialNewBooking' error:", error);
        });
        return result;
    },
};
const attracControl = {
    initialAttracPage(imgList){
        attracModel.getAttracData().then((data)=>{
            attracView.renderMainContent(data);
            for(let i=0; i<data["data"]["images"].length; i++){
                attracView.renderImgRadioInputs(i);
                attracModel.stackImgs(i, data["data"]["images"][i], imgList);
            };
            attracView.updateCurrentImg(0, imgList);
        });
    },
    setBookingStartDate(){
        let currentDate = new Date().toJSON().slice(0, 10);     //取前十位數(YYYY-MM-DDTHH:MM:SS.SSSZ)
        document.getElementById("tourDate").min = currentDate;  // setAttribute("min", "currentDate")
    },
    isDateValid(){
        return (document.getElementById("tourDate").value.length>0) ? true : false;
    },
    isTimeSlotAndExpenseValid(){
        return (document.querySelector("input[name='timeSlot']:checked")!=null) ? true : false;
    },
    async submitBookingData(){
        console.log([this.isDateValid(), this.isTimeSlotAndExpenseValid()]);
        if([this.isDateValid(), this.isTimeSlotAndExpenseValid()].includes(false)){
            // console.log("資料未完整填寫");
        }else{
            // console.log("收集資料");
            let bookingData = attracModel.collectBookingInput();
            // console.log(bookingData);
            let orderData = await attracModel.getOrderData();
            if(orderData["data"]!=null){
                attracModel.cancelledAnOrder();
            };
            let result = await attracModel.initialNewBooking(bookingData);
            console.log(result);
            if(result["result"]===true){
                window.location.replace("/booking");
            }else if(result["message"]==="建立失敗，輸入不正確或其他原因"){
                return "建立失敗，輸入不正確或其他原因"
            }else if(result["message"]==="未登入系統，拒絕存取"){
                memberView.initalMemberPortal();
                memberView.showMemberPortalMessage("請先登入/註冊會員");
                return "未登入系統，拒絕存取"
            }else{
                return "內部伺服器錯誤"
            };
        };
    },
};
attracControl.initialAttracPage(imgList);
attracControl.setBookingStartDate();
window.addEventListener("click", (event)=>{
    if(event.target.id==="previousImg"){
        let currentImgID = parseInt(document.getElementById("currentImg").alt);
        (currentImgID-1>=0) ? attracView.updateCurrentImg(currentImgID-1, imgList) : attracView.updateCurrentImg(imgList.length-1, imgList);
        attracView.renderAnimationForChangingImg("previousImg");
    }else if(event.target.id==="nextImg"){
        let currentImgID = parseInt(document.getElementById("currentImg").alt);
        (currentImgID+1<imgList.length) ? attracView.updateCurrentImg(currentImgID+1, imgList) : attracView.updateCurrentImg(0, imgList);
        attracView.renderAnimationForChangingImg("nextImg");
    }else if(event.target.name==="imgList"){
        attracView.updateCurrentImg(event.target.id, imgList);
        attracView.renderAnimationForChangingImg("pickImg");
    }else if(event.target.name==="timeSlot"){
        let charge="";
        (event.target.id==="morning") ? charge=2000 : charge=2500;
        document.getElementById("charge").textContent = `新台幣${charge}元`;
    }else if(event.target.id==="stratBooking"){
        attracControl.submitBookingData();
    };
});
