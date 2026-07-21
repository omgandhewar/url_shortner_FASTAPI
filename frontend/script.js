function login(successcallback){

    let email=document.querySelector("#email").value;
    let password=document.querySelector("#password").value;

    fetch("http://127.0.0.1:8000/login",{
        method:"POST",
        credentials:"include",
        headers:{
            "Content-Type":"application/json"
        },
        body:JSON.stringify({
            email:email,
            password:password
        })

    })
    .then(function(response){
        if(!response.ok){
            throw new Error("invalid credential");
        }
        return response.json()
    })
    .then(function(data){
        console.log(data);
        successcallback();
    })
    .catch(function(error){
        console.log(error);
    })
    
}

let loginform=document.querySelector("#loginform");
console.log(loginform);
if(loginform){
    loginform.addEventListener("submit",function(event){

        event.preventDefault();

        login(function(){
            window.location.href="dashboard.html";
        });
    });
}

function signup(signupcallback){

    let name=document.querySelector("#username").value;
    let email=document.querySelector("#email").value;
    let password=document.querySelector("#password").value;

    fetch("http://127.0.0.1:8000/signup",{
        method:"POST",
        headers:{
            "Content-Type":"application/json"
        },
        body:JSON.stringify({
            name:name,
            email:email,
            password:password
        })
    })
    .then(function(response){
        return response.json();
    })
    .then(function(data){
        console.log(data);
        signupcallback();
    })
    .catch(function(error){
        console.log(error);
    })
}

let signupform=document.querySelector("#signupform");
if(signupform){
    signupform.addEventListener("submit",function(event){

        event.preventDefault();

        signup(function(){
            window.location.href="login.html";
        })
    })
}


function dashboard(){

    fetch("http://127.0.0.1:8000/dashboard",{
        method:"GET",
        credentials:"include",
    })
    .then(function(response){

   if (response.status === 401) {
    alert("Session expired. Please login again.");
    window.location.replace("login.html");
    return Promise.reject(new Error("Unauthorized"));
}
 
        if(!response.ok){
            throw new Error("Not Authenticated");
        }

        return response.json();
    })
    .then(function(data){

        console.log(data);
        document.getElementById("total_url").innerText=data.total_url;
        document.getElementById("total_count").innerText=data.total_count;

        let div=document.querySelector("#url_list");

        data.url.forEach(function(url1){

        button=document.createElement("button");

        button.innerText = "Analytics";

        button.onclick = function () {
        window.location.href = `analytics.html?id=${url1.id}`;
    }
        div.appendChild(button);
    });

    })
    .catch(function(error){
        console.log(error);
    })
}

if (window.location.pathname.endsWith("dashboard.html")) {
    dashboard();
}

function url_shortner(urlcallback){

    let url=document.querySelector("#short_url").value;
    
   fetch("http://127.0.0.1:8000/urlshortner", {
    method: "POST",
    credentials: "include",
    headers: {
        "Content-Type": "application/json"
    },
    body: JSON.stringify({
        Original_url: url
    })
})
.then(function(response){

    console.log("Status:", response.status);

    if (!response.ok) {
        
        return response.json().then(function(data){

            throw new Error(data.detail);

        });

    }

    return response.json();

})
.then(function(data){

    console.log(data);

})
.catch(function(error){

    alert(error.message);

})
}

let url_shortner1=document.querySelector("#url_shortner");
if(url_shortner1){
    url_shortner1.addEventListener("submit",function(event){

        event.preventDefault();

        url_shortner(function(){
            console.log("short url");
        })
    })
}


let logoutBtn = document.querySelector("#logout");

if (logoutBtn) {

    logoutBtn.addEventListener("click", function () {

        fetch("http://127.0.0.1:8000/logout", {
            method: "POST",
            credentials: "include"
        })
        .then(function(response) {
            return response.json();
        })
        .then(function(data) {
            console.log(data);
            window.location.href = "login.html";
        });

    });

}


function Analytics(url_id){

     console.log("Analytics function called");
    console.log("URL ID:", url_id);

    fetch(`http://127.0.0.1:8000/Analytics/${url_id}`,{
        method:"GET",
        credentials:"include"
    })
    .then(function(response){
        return response.json()
    })
    .then(function(data){
        console.log(data);


        document.getElementById("total_clicked").innerText = data.total_clicked;
        document.getElementById("Last_clicked").innerText = data.Last_clicked;
    })
}

if (window.location.pathname.endsWith("analytics.html")) {

    const params = new URLSearchParams(window.location.search);

    const url_id = params.get("id");

    console.log(url_id);

    Analytics(url_id);

}

