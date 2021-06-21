

// onclick handle of section

function hide_sect() {
  console.log("hide_sect");
  var sect_all = document.querySelectorAll(".sect-icons");
  for (i = 0; i < sect_all.length; i++) {
    sect_all[i].style.display = "none";
  }
}
function hide_sect_edit() {
  console.log("hide_sect_edit");
  // close edit input field
  var sect_edit = document.querySelectorAll("#open-section-edit");
  for (i = 0; i < sect_edit.length; i++) {
    if (sect_edit[i].style.display != "none") {
      sect_edit[i].style.display = "none";
    }
  }
}

function open_sect(e) {
  console.log("open_sect(e)");
  body_click("open_sect");
  var sect = e.parentNode.querySelector(".sect-icons");
  if (sect.style.display == "none") {
    hide_sect();
    sect.style.display = "flex";
  } else {
    sect.style.display = "none";
  }

  hide_sect_edit();
}

function open_section_edit(e) {
  console.log("open_section_edit(e)");
  var sect_edit =
    e.parentNode.parentNode.parentNode.querySelector("#open-section-edit");
  if (sect_edit.style.display == "none") {
    sect_edit.style.display = "flex";
  } else {
    sect_edit.style.display = "none";
  }
}

// -----------------------------------------

// onclick handle of add course
function hide_add_course() {
  console.log("hide_add_course");
  var course_all = document.querySelectorAll("#open-add-course");
  for (i = 0; i < course_all.length; i++) {
    course_all[i].style.display = "none";
  }
}

function open_add_course(e) {
  body_click("open_add_course");

  var course = e.parentNode.parentNode.querySelector("#open-add-course");
  if (course.style.display == "none") {
    hide_add_course();
    course.style.display = "flex";
  } else {
    course.style.display = "none";
  }
}

// ------------------------------------------

// onclick handle of add section
function close_form_sect() {
  console.log("close_form_sect");
  var add_section = document.querySelector("#open-form-sect");
  var button_section = document.querySelector(".add_sect");
  button_section.style.display = "block";
  add_section.style.display = "none";
}
function open_form_sect() {
  console.log("open_form_sect");

  body_click("open_form_sect");
  var add_section = document.querySelector("#open-form-sect");
  var button_section = document.querySelector(".add_sect");
  if (button_section.style.display == "block") {
    button_section.style.display = "none";
    add_section.style.display = "flex";
  }
}
// ---------------------------------------------------

// toggle name and code

function switch_name(name, code) {
  var text = document.querySelector(".name");
  var copy_icon = document.querySelector(".copy_icon");

  if (text.innerHTML == code) {
    text.innerHTML = name;
    // hide copy_icon while viewing name
    copy_icon.style.display = "none";
    // change margin style prop of name
    text.style.margin = "5px 20px";
  } else {
    text.innerHTML = code;
    // show copy_icon while viewing code
    copy_icon.style.display = "block";
    // change margin style prop of code
    text.style.margin = "5px 20px 5px 5px";
  }
}

// ---------------------------------------------------

// right click on edit or delete course

// hide menu
function hide_menu() {
  console.log("hide_menu");

  var menu_all = document.querySelectorAll("#contextMenu");

  for (i = 0; i < menu_all.length; i++) {
    if (menu_all[i].style.display == "block") {
      menu_all[i].style.display = "none";
      hide_course_edit(menu_all[i]);
    }
  }
}

// display menu
function right_click_course(e, event, holder) {
  body_click("right_click_course");
  if (holder == "True") {
    if (event.button == 2) {
      document.addEventListener("contextmenu", (event) =>
        event.preventDefault()
      );

      var menu = e.parentNode.parentNode.querySelector("#contextMenu");
      hide_menu();
      menu.style.display = "block";
      menu.style.left = event.pageX + "px";
      menu.style.top = event.pageY + "px";
      console.log("x: " + event.pageX + " y:" + event.pageY);
    }
  }
}

// fide course_edit field
function hide_course_edit(e) {
  console.log("hide_course_edit");

  var edit_field = e.parentNode.querySelector("#open-course-edit");
  edit_field.style.display = "none";
  var del = e.parentNode.querySelector(".del-popup");
  del.style.display = "block";
}

// open course edit
function open_course_edit(e) {
  console.log("open_course_edit");
  
  var edit_field = e.parentNode.querySelector("#open-course-edit");
  edit_field.style.display = "block";
  // var edit = e.parentNode.querySelector('.course_edit');
  // edit.style.display = 'none';
  var del = e.parentNode.querySelector(".del-popup");
  del.style.display = "none";
}

// -----------------------------------------------

// click on page
function body_click(except = null) {
  console.log("body click: " + except);
  if (except != "open_add_course") hide_add_course();
  if (except != "open_sect") hide_sect();
  if (except != "open_form_sect") close_form_sect();
  if (except != "right_click_course") hide_menu();
  // result of root click element
  hide_sect_edit();
}

// ----------------------------------------------------

// copy to clipboard
function copy_to_clip() {
  var text = document.querySelector(".name");
  var r = document.createRange();
  r.selectNode(text);
  window.getSelection().removeAllRanges();
  window.getSelection().addRange(r);
  document.execCommand("copy");
  window.getSelection().removeAllRanges();

  var alert = document.querySelector(".success_js");
  alert.querySelector(".text_msg").innerHTML = "Code copied";
  alert.style.display = "flex";
}
