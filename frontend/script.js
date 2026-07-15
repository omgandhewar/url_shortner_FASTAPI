function login(successcallback){

    let email=document.querySelector("#email").value;
    let password=document.querySelector("#password").value;

    fetch("http://127.0.0.1:8000/login",{
        method:"POST",
        headers:{
            "Content-Type":"application/json"
        },
        body:JSON.stringify({
            email:email,
            password:password
        })

    })
    .then(function(response){
        return response.json()
    })
    .then(function(data){
        console.log(data);
        successcallback();
    })
    
}

let loginform=document.querySelector("#loginform");
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

    fetch("/http://127.0.0.1:8000/signup",{
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

        if(!response.ok){
            throw error("invalid credential");
        }
        return response.json();
    })
    .then(function(data){
        console.log(data);
        signupcallback();
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