const navMemberTab = document.getElementById("navMember");
export const memberView = {
    initalMemberPortal(){
        let memberPortalTab = document.createElement("div");
        memberPortalTab.setAttribute("id", "memberPortal");
        document.body.appendChild(memberPortalTab);
        this.loginMemberPortal();
    },
    loginMemberPortal(){
        // 建立
        let memberPortalTab = document.getElementById("memberPortal");
        let loginWindowTab = document.createElement("form");
        loginWindowTab.setAttribute("id", "loginWindow");
        let divTab = document.createElement("div");
        let memberPortalTitleTab = document.createElement("span");
        memberPortalTitleTab.innerText = "登入會員帳號";
        let closeMemberPortalTab = document.createElement("button");
        closeMemberPortalTab.setAttribute("id", "closeMemberPortal");
        closeMemberPortalTab.setAttribute("type", "button");
        let emailTab = document.createElement("input");
        emailTab.setAttribute("id", "email");
        emailTab.setAttribute("type", "email");
        emailTab.setAttribute("placeholder", "輸入電子信箱");
        emailTab.setAttribute("autocomplete", "email");
        emailTab.setAttribute("pattern", "[^@]+@[^@]+");
        let passwordTab = document.createElement("input");
        passwordTab.setAttribute("id", "password");
        passwordTab.setAttribute("type", "password");
        passwordTab.setAttribute("placeholder", "輸入密碼");
        passwordTab.setAttribute("autocomplete", "current-password");
        let loginBtnTab = document.createElement("button");
        loginBtnTab.setAttribute("id", "loginBtn");
        loginBtnTab.setAttribute("type", "button");
        loginBtnTab.innerText = "登入帳戶";
        let toRegisterTab = document.createElement("span");
        toRegisterTab.setAttribute("id","toRegister");
        toRegisterTab.innerText = "還沒有註冊帳戶？點此註冊";
        // 組合
        memberPortalTab.appendChild(loginWindowTab);
        loginWindowTab.append(memberPortalTitleTab, closeMemberPortalTab, divTab);
        divTab.append(emailTab, passwordTab, loginBtnTab, toRegisterTab);
    },
    signUpMemberPortal(){
        // 建立
        let memberPortalTab = document.getElementById("memberPortal");
        let signUpWindowTab = document.createElement("form");
        signUpWindowTab.setAttribute("id", "signUpWindow");
        let divTab = document.createElement("div");
        let memberPortalTitleTab = document.createElement("span");
        memberPortalTitleTab.innerText = "註冊會員帳號";
        let closeMemberPortalTab = document.createElement("button");
        closeMemberPortalTab.setAttribute("id", "closeMemberPortal");
        closeMemberPortalTab.setAttribute("type", "button");
        let nameTab = document.createElement("input");
        nameTab.setAttribute("id", "name");
        nameTab.setAttribute("type", "text");
        nameTab.setAttribute("placeholder", "輸入姓名");
        nameTab.setAttribute("autocomplete", "name");
        nameTab.setAttribute("minlength", 1);
        let emailTab = document.createElement("input");
        emailTab.setAttribute("id", "email");
        emailTab.setAttribute("type", "email");
        emailTab.setAttribute("placeholder", "輸入電子信箱");
        emailTab.setAttribute("autocomplete", "email");
        emailTab.setAttribute("pattern", "[^@]+@[^@]+");
        let passwordTab = document.createElement("input");
        passwordTab.setAttribute("id", "password");
        passwordTab.setAttribute("type", "password");
        passwordTab.setAttribute("placeholder", "輸入密碼");
        passwordTab.setAttribute("autocomplete", "off");
        passwordTab.setAttribute("minlength", 8);
        passwordTab.setAttribute("maxlength", 32);
        let signUpBtnTab = document.createElement("button");
        signUpBtnTab.setAttribute("id", "signUpBtn");
        signUpBtnTab.setAttribute("type", "button");
        signUpBtnTab.innerText = "註冊新帳戶";
        let toLoginTab = document.createElement("span");
        toLoginTab.setAttribute("id","toLogin");
        toLoginTab.innerText = "已經有帳戶了？點此登入";
        // 組合
        memberPortalTab.appendChild(signUpWindowTab);
        signUpWindowTab.append(memberPortalTitleTab, closeMemberPortalTab, divTab);
        divTab.append(nameTab, emailTab, passwordTab, signUpBtnTab, toLoginTab);
    },
    closeMemberPortal(){
        let memberPortalTab = document.getElementById("memberPortal");
        memberPortalTab.remove();
    },
    toSignUp(){
        let loginWindowTab = document.getElementById("loginWindow");
        loginWindowTab.remove();
        this.signUpMemberPortal();
    },
    toLogin(){
        let signUpWindowTab = document.getElementById("signUpWindow");
        signUpWindowTab.remove();
        this.loginMemberPortal();
    },
    clearMemberPortalMessage(){
        let messageTab = document.querySelectorAll(".memberPortalMessage");
        if(messageTab.length>0){
            messageTab.forEach((element)=>{
                element.remove();
                // console.log("message is cleared");
            });
        }else{
            // console.log("there is no message");
        };
    },
    showMemberPortalMessage(message){
        this.clearMemberPortalMessage();
        let theLastElement = document.querySelector("div#memberPortal>form>div");
        let messageTab = document.createElement("span");
        messageTab.setAttribute("class", "memberPortalMessage");
        messageTab.innerText = message;
        theLastElement.appendChild(messageTab);
    },
    memberLogedIn(){
        navMemberTab.innerText = "登出系統";
    },
    memberLogedOut(){
        navMemberTab.innerText = "登入/註冊";
    },
    memberAlert(message){
        alert(message);
        // let alertTab = document.createElement("div");
        // alertTab.setAttribute("class", "alert");
        // alertTab.innerText = message;
        // document.body.appendChild(alertTab);
    },
    cleanInputValue(inputTabID){
        let inputTab = document.getElementById(inputTabID);
        inputTab.innerText = null;
    },
};
export const memberModel = {
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
    isPasswordValid(){
        let password = document.getElementById("password").value;
        if(password.length>=8 && password.length<=32){
            // console.log("password is valid");
            return true;
        }else{
            // console.log("password is NOT valid");
            return false;
        };
    },
    collectingLoginData(){
        if([this.isEmailValid(), this.isPasswordValid()].includes(false)){
            // console.log({"data": null});
            return {"data": null};
        }else{
            let email = document.getElementById("email").value;
            let password = document.getElementById("password").value;
            // console.log({"data": {"email": email, "password": password}});
            return {"data": {"email": email, "password": password}};
        };
    },
    collectingSignUpData(){
        if([this.isNameValid(), this.isEmailValid(), this.isPasswordValid()].includes(false)){
            // console.log("sign up data are:", {"data": null});
            return {"data": null};
        }else{
            let name = document.getElementById("name").value;
            let email = document.getElementById("email").value;
            let password = document.getElementById("password").value;
            // console.log("sign up data are:", {"data": {"name":name, "email": email, "password": password}});
            return {"data": {"name":name, "email": email, "password": password}};
        };
    },
    async checkMemberStatus(){
        let result = await fetch("/api/user/auth", {
            method: "GET",
            headers: {"Cookie": document.cookie}
        }).then((response)=>{
            return response.json();
        }).then((data)=>{
            if(data["data"]!=null){
                return {"result": true, "data": data["data"]};
            }else{
                return {"result": false, "data": null};
            };
        }).catch((error)=>{
            console.log("function 'checkMemberStatus' error:", error);
        });
        return result;
    },
    async requestLogIn(data){
        let result = await fetch("/api/user/auth", {
            method: "PUT",
            headers: {"Content-Type": "application/json", "Cookie": document.cookie},
            body: JSON.stringify(data)
        }).then((response)=>{
            return response.json();
        }).then((data)=>{
            if("ok" in data){
                return {"result": true, "message": "登入成功"};
            }else{
                return {"result": false, "message": data["message"]}
            }
        }).catch((error)=>{
            console.log("function 'requestLogIn' error:", error);
        });
        return result;
    },
    async requestSignUp(data){
        let result = await fetch("/api/user", {
            method: "POST",
            headers: {"Content-Type": "application/json", "Cookie": document.cookie},
            body: JSON.stringify(data)
        }).then((response)=>{
            return response.json();
        }).then((data)=>{
            if("ok" in data){
                return {"result": true, "message": "註冊成功"};
            }else{
                return {"result": false, "message": data["message"]};
            }
        }).catch((error)=>{
            console.log("function 'requestSignUp' error:", error);
        });
        return result;
    },
    async requestLogOut(){
        let result = await fetch("/api/user/auth", {method: "DELETE"}).then((response)=>{
            return response.json();
        }).then((data)=>{
            if("ok" in data){
                return {"result": true, "message": "登出成功"};
            };
        });
        return result;
    },
    // checkCookie(){
    //     let cookie = document.cookie;
    //     console.log("cookie", cookie);
    // },
    // decodeCookie(){
    //     let cookie = document.cookie;
    //     let base64Url = cookie.split('.')[1];
    //     let base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    //     let jsonPayload = decodeURIComponent(window.atob(base64).split('').map(function(c) {
    //         return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
    //     }).join(''));
    //     let data = JSON.parse(jsonPayload);
    //     console.log(data["status"]);
    //     return JSON.parse(jsonPayload);
    // }
};
export const memberControl = {
    async initialMemberStatus(){
        let memberStatus = await memberModel.checkMemberStatus();
        if(memberStatus["result"]===true){
            memberView.memberLogedIn();
            return "logedIn";
        }else{
            memberView.memberLogedOut();
            return "logedOut";
        };
    },
    async login(){
        let data = memberModel.collectingLoginData()["data"];
        if(data===null){
            let message = "請輸入會員資料";
            memberView.showMemberPortalMessage(message);
        }else if(data!=null){
            if([memberModel.isEmailValid(), memberModel.isPasswordValid()].includes(false)){
                return false;
            }else if(memberModel.isEmailValid()===true && memberModel.isPasswordValid()===true){
                let response = await memberModel.requestLogIn(data);
                if(response["result"]===true){
                    memberView.closeMemberPortal();
                    memberView.memberAlert("登入成功")
                    memberView.memberLogedIn();
                }else{
                    memberView.showMemberPortalMessage(response["message"]);
                };
            };
        };
    },
    async signUp(){
        let data = memberModel.collectingSignUpData()["data"];
        if(data===null){
            let message = "請確認註冊資料是否完整填寫";
            memberView.showMemberPortalMessage(message);
        }else{
            let result = await memberModel.requestSignUp(data);
            // console.log("the result of sign up is:", result);
            if(result["result"]===true){
                memberView.toLogin();
                let message = "註冊成功，請立即登入"
                memberView.showMemberPortalMessage(message);
            }else{
                let message = result["message"];
                // console.log("message:", message);
                memberView.showMemberPortalMessage(message);
            };
        };
    },
    async logout(){
        let result = await memberModel.requestLogOut();
        if(result["result"]===true){
            memberView.memberLogedOut();
            memberView.memberAlert(result["message"]);
            window.location.replace("/");
        };
    },
    async toBooking(){
        let memberStatus = await memberModel.checkMemberStatus();
        if(memberStatus["result"]===false){
            memberView.initalMemberPortal();
            memberView.showMemberPortalMessage("請先登入/註冊會員");
            return "請先登入/註冊會員";
        }else if(memberStatus["data"]!=null){
            window.location.replace("/booking");
            return "成功轉跳";
        };
    },
};

memberControl.initialMemberStatus();
window.addEventListener("click", (event)=>{
    // console.log(event.target.id);
    if(event.target.innerText==="登入/註冊"){
        event.preventDefault();
        event.stopPropagation();
        memberView.initalMemberPortal();
    }else if(event.target.innerText==="登出系統"){
        memberControl.logout();
    }else if(event.target.id==="closeMemberPortal"){
        memberView.closeMemberPortal();
    }else if(event.target.id==="toRegister"){
        memberView.toSignUp();
    }else if(event.target.id==="toLogin"){
        memberView.toLogin();
    }else if(event.target.id==="loginBtn"){
        memberModel.isEmailValid();
        memberModel.isPasswordValid();
        memberControl.login();
    }else if(event.target.id==="signUpBtn"){
        memberControl.signUp();
    }else if(event.target.innerText==="預定行程"){
        memberControl.toBooking();
    };
});