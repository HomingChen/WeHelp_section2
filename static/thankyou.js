const thankyouView = {
  adjustTimeText(){
    let time = (document.querySelector("#tourTime").value==="morning") ? "早上9點至中午12點" : "下午1點至下午4點";
    document.querySelector("#tourTime").innerText = time;
    },
};
// thankyouModel = {
    // async getPaymentData(){
    //     let data = await fetch().then();
    // },
// };
// thankyouControl = {
    // async initialThankyouPage(orderData){
    //     let data = await bookingModel.getOrderData();
    //     if(data["message"]==="未登入系統，拒絕存取"){
    //         window.location.replace("/");
    //         return "未登入系統，拒絕存取"
    //     }else if(data["data"]==null){
    //         let memberData = await memberModel.checkMemberStatus();
    //         bookingView.noOrderInfo(memberData=memberData["data"]);
    //     }else if(data["data"]!=null){
    //         let memberData = await memberModel.checkMemberStatus();
    //         bookingView.initialValidOrderInfo(memberData["data"], data["data"]);
    //         bookingModel.stroeOrderData(orderData, data["data"]);
    //     }else{
    //         return "內部伺服器錯誤"
    //     };
    // },
// };
thankyouView.adjustTimeText();