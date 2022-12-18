import { memberView, memberModel, memberControl } from "/static/member.js";

const bookingView = {
    initialValidOrderInfo(memberData, orderData){
        document.getElementById("title").innerText = `您好，${[memberData["name"]]}，待訂的行程如下：`;
        document.getElementById("img").setAttribute("src", orderData["attraction"]["image"]);
        document.getElementById("tourPlace").innerText = `台北一日遊：${orderData["attraction"]["name"]}`;
        document.getElementById("tourDate").innerText = orderData["date"];
        let time = (orderData["time"]==="morning") ? "早上9點至中午12點" : "下午1點至下午4點";
        document.getElementById("tourTime").innerText = time;
        document.getElementById("tourPrice").innerText = `新台幣 ${orderData["price"]} 元`;
        document.getElementById("tourAddress").innerText = orderData["attraction"]["address"];
        document.getElementById("memberName").value = memberData["name"];
        document.getElementById("email").value = memberData["email"];
        document.getElementById("price").innerText = `總價：新台幣 ${orderData["price"]} 元`;
    },
    noOrderInfo(memberData){
        document.getElementById("order").remove();
        document.getElementById("title").innerText = `您好，${[memberData["name"]]}，待訂的行程如下：`;
        let noOrderTab = document.createElement("div");
        noOrderTab.setAttribute("id", "noOrder");
        noOrderTab.innerText = "目前沒有任何待預訂的行程"
        document.getElementById("mainContent").appendChild(noOrderTab);
    }
};
const bookingModel = {
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
};
const bookingControl = {
    async initialBookingPage(){
        let orderData = await bookingModel.getOrderData();
        if(orderData["message"]==="未登入系統，拒絕存取"){
            window.location.replace("/");
            return "未登入系統，拒絕存取"
        }else if(orderData["data"]==null){
            let memberData = await memberModel.checkMemberStatus();
            console.log(memberData);
            bookingView.noOrderInfo(memberData=memberData["data"]);
        }else if(orderData["data"]!=null){
            let memberData = await memberModel.checkMemberStatus();
            console.log(memberData["data"]);
            bookingView.initialValidOrderInfo(memberData=memberData["data"], orderData=orderData["data"]);
        }else{
            return "內部伺服器錯誤"
        };
    },
};

bookingControl.initialBookingPage();

window.addEventListener("click", (event)=>{
    if(event.target.id==="cancel"){
        bookingModel.cancelledAnOrder();
        bookingControl.initialBookingPage();
    };
});