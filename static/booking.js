import { memberView, memberModel, memberControl } from "/static/member.js";

const orderData = {};
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
        document.getElementById("name").value = memberData["name"];
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
    stroeOrderData(orderData, data){
        Object.assign(orderData, {
            "order": 
            {"price": data["price"], 
            "trip": data["attraction"], 
            "date": data["date"], 
            "time": data["time"]
            }
        });
        return orderData;
    },
    addContactInfoToOrderData(orderData){
        let contactInfo = {
            "name": document.querySelector("#name").value,
            "email": document.querySelector("#email").value,
            "phone": document.querySelector("#phone").value
        };
        Object.assign(orderData, {"contact": contactInfo});
        return orderData;
    },
    addPrimeToOrderData(orderData, prime){
        Object.assign(orderData, {"prime": prime});
        return orderData;
    }
};
const bookingControl = {
    isNameValid(){
        let name = document.getElementById("name").value;
        if(name.length>0 && name.length<=100){
            // console.log("name is valid");
            return true;
        }else{
            // console.log("name is NOT valid");
            return false;
        };
    },
    isEmailValid(){
        let email = document.getElementById("email").value;
        let regex_check_result = email.match(/[^@]+@[^@]+/g);
        if(regex_check_result===null){
            // console.log("email is NOT valid");
            return false;
        };
        if(regex_check_result[0].length===email.length && email.length<=100){
            // console.log("email is valid");
            return true;
        }else{
            // console.log("email is NOT valid");
            return false;
        };
    },
    isPhoneValid(){
        let phone = document.getElementById("phone").value.replace(
            "+886", "09").replace("-", "").replace(" ", "");
        let regex_check_result = phone.match(/[0-9]+/g);
        if(regex_check_result===null){
            // console.log("email is NOT valid");
            return false;
        };
        if(regex_check_result[0].length===10){
            // console.log("email is valid");
            return true;
        }else{
            // console.log("email is NOT valid");
            return false;
        };
    },
    checkPaymentStatus(){
        let cookie = document.cookie;
        console.log("cookie", cookie);
    },
    async initialBookingPage(orderData){
        let data = await bookingModel.getOrderData().then((response)=>{
            if(response.redirected==true){
                window.location.replace(response.url);
            }else{
                return response.json();
            };
        }).then((data)=>{
            return data;
        });
        if(data["message"]==="未登入系統，拒絕存取"){
            window.location.replace("/");
            return "未登入系統，拒絕存取"
        }else if(data["data"]==null){
            let memberData = await memberModel.checkMemberStatus();
            bookingView.noOrderInfo(memberData=memberData["data"]);
        }else if(data["data"]!=null){
            let memberData = await memberModel.checkMemberStatus();
            bookingView.initialValidOrderInfo(memberData["data"], data["data"]);
            bookingModel.stroeOrderData(orderData, data["data"]);
        }else{
            return "內部伺服器錯誤"
        };
    },
    async getPrimeByCard(){
        console.log("getPrimeByCard");
        let checkContactArray = [this.isNameValid(), this.isEmailValid(), this.isPhoneValid()];
        if (checkContactArray.includes(false)){
            alert("請確認各欄位是否填寫正確");
            return
        };
        // 取得 TapPay Fields 的 status
        const tappayStatus = TPDirect.card.getTappayFieldsStatus();
        // 確認是否可以 getPrime
        if (tappayStatus.canGetPrime === false) {
            alert("請確認各欄位是否填寫正確");
            return
        };
        // Get prime
        await TPDirect.card.getPrime((result) => {
            if (result.status !== 0) {
                // alert('get prime error ' + result.msg);
                return
            };
            bookingModel.addContactInfoToOrderData(orderData);
            bookingModel.addPrimeToOrderData(orderData, result.card.prime);
            console.log(orderData);
            console.log("getPrime Done");
            this.sendOrderPayment();
            return orderData;
        });
    },
    // async getPrimeByCCV(){
    //     console.log("getPrimeByCCV");
    //     const tappayStatus = TPDirect.ccv.onUpdate((update)=>{
    //         return update;
    //     });
    //     if(tappayStatus.canGetPrime === false){
    //         alert('can not get prime');
    //         return;
    //     };
    //     await TPDirect.ccv.getPrime().then((result)=>{
    //         if (result.status !== 0) {
    //             alert('get prime error ' + result.msg);
    //             return;
    //         };
    //         alert('get prime 成功，prime: ' + result.ccv_prime);
    //         // console.log("result", result);
    //         bookingModel.addContactInfoToOrderData(orderData);
    //         bookingModel.addPrimeToOrderData(orderData, result.ccv_prime);
    //         console.log(orderData);
    //         console.log("getPrime Done");
    //         this.sendOrderPayment();
    //         return orderData;
    //     });
    // },
    async sendOrderPayment(){
        console.log("start to send");
        await fetch("/api/order", {
            method: "POST",
            headers: {"Content-Type": "application/json", "Cookie": document.cookie},
            body: JSON.stringify(orderData)
        }).then((response)=>{
            console.log("getFeedBack");
            return response.json();
        }).then((data)=>{
            console.log(data);
            this.processPaymentResult(data);
        }).catch((error)=>{
            console.log("function 'sendOrderPayment' error:", error);
            alert("付款失敗，請確認帳戶資訊");
        });
    },
    processPaymentResult(data){      
        if(data["data"]["payment"]["status"]===0){
            let orderID = data["data"]["number"]
            window.location.replace("/thankyou?number="+orderID);
        }else{
            alert("付款失敗，請確認帳戶資訊");
        };
    }
};

bookingControl.initialBookingPage(orderData);

TPDirect.setupSDK(126876, 'app_5XuSpzvcH1eJB3ZCSU01Da9BBHXQccgnRIKsZicxMuFOh0KrfApMr41eWwZX', 'sandbox');
TPDirect.card.setup({
    // Display ccv field
    fields: {
        number: {
            // css selector
            element: '#card-number',
            placeholder: '**** **** **** ****'
        },
        expirationDate: {
            // DOM object
            element: document.getElementById('card-expiration-date'),
            placeholder: 'MM / YY'
        },
        ccv: {
            element: '#card-ccv',
            placeholder: 'ccv'
        }
    },
    styles: {
        // Style all elements
        'input': {
            'color': 'gray'
        },
        // Styling ccv field
        'input.ccv': {
            'font-size': '16px'
        },
        // Styling expiration-date field
        'input.expiration-date': {
            'font-size': '16px'
        },
        // Styling card-number field
        'input.card-number': {
            'font-size': '16px'
        },
        // style focus state
        ':focus': {
            'color': 'black',
            'border': '5px solid'
        },
        // style valid state
        '.valid': {
            'color': 'green'
        },
        // style invalid state
        '.invalid': {
            'color': 'red'
        }
    },
    // 此設定會顯示卡號輸入正確後，會顯示前六後四碼信用卡卡號
    isMaskCreditCardNumber: true,
    maskCreditCardNumberRange: {
        beginIndex: 6,
        endIndex: 11
    }
});

window.addEventListener("click", (event)=>{
    if(event.target.id==="cancel"){
        bookingModel.cancelledAnOrder();
        bookingControl.initialBookingPage();
    }else if(event.target.id==="submit"){
        event.preventDefault();
        let response = bookingControl.getPrimeByCard().then((data)=>{
            console.log("response", data);
        });
        console.log("responsed", response);
    };
});