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
        if(!response.ok){
            throw new Error("Not Authenticated");
        }

        return response.json();
    })
    .then(function(data){
        console.log(data);
        document.getElementById("total_url").innerText=data.total_url;
        document.getElementById("total_count").innerText=data.total_count;
    })
    .catch(function(error){
        console.log(error);
    })
}

dashboard()