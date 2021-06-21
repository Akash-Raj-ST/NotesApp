function open_code_form(){

    var a = document.getElementById('right-form');
    var b = document.querySelector(".code");
    var c = document.querySelector("#code_warning");

    a.style.display="block";
    b.style.display = "none";
    
    if(c){
        c.style.display='none';
    }
    
}

