const title = document.getElementById('title');
const namefield = document.getElementById(namefield);
const signinbtn = document.getElementById(signinbtn);
const signupbtn = document.getElementById(signupbtn);

signupbtn.onclick = function(){
    title.innerHTML = "sign up";
    namefield.style.display = "block"; 
}
signinbtn.onclick = function(){
    title.innerHTML = "log in";
    namefield.style.display = "none"; 
}