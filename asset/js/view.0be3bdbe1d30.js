var allow_close = true;

// pdf open and close

function close_pdf_edit(){
    var x = document.querySelectorAll("#open-pdfedit-form")
    for(i=0;i<x.length;i++){
        if(x[i].style.display=="flex"){
            x[i].style.display='none';
        }
    }
}

function open_pdf_edit(e){
    body_click('open_pdf_edit');
    var a= e.parentNode.parentNode.parentNode.querySelector("#open-pdfedit-form");
    var open=true;
    if(a.style.display=='flex'){
        a.style.display = 'none';
    }else{
        close_pdf_edit();
        a.style.display='flex';
    }
    
}
// --------------------------------

// new feature
function close_notes(){
    console.log("close_notes");
    var a = document.querySelector(".notes-section");
    a.style.display='none';
}

function open_notes(){
    body_click('open_notes');
    var a = document.querySelector(".notes-section");
    if(a.style.display=='none'){
        a.style.display='flex';
    } 
    else{
        a.style.display = 'none';
    } 
}

// -------------------------

function body_click(except = null){
    if(except != 'open_pdf_edit')
    close_pdf_edit();
    if(except != 'open_notes')
    close_notes();
}