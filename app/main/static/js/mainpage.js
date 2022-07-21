function show() {
    document.getElementById("content").style.visibility = "visible";
    document.getElementById("m_info").style.visibility = "visible";
    document.body.style.overflow = "hidden";
}

function hide() {
    document.getElementById("content").style.visibility = "hidden";
    document.getElementById("m_info").style.visibility = "hidden";
    document.body.style.overflow = "";
}

function show_l() {
    document.getElementById("l_info").style.visibility = "visible";
    document.getElementById("l_info_cont").style.visibility = "visible";
    document.body.style.overflow = "hidden";
}

function hide_l() {
    document.getElementById("l_info").style.visibility = "hidden";
    document.getElementById("l_info_cont").style.visibility = "hidden";
    document.body.style.overflow = "";
}