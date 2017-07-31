

$(document).ready(function(){

    // Get current location
    var current_location = window.location.pathname.substring(1);

    var lists = $("#navbar>ul>li");



    for (var i = 0; i < lists.length; i++){
        var li_text = lists[i].innerText.toLowerCase().trim();

        console.log("LI TEXT: " + li_text);
        console.log("CURRENT LOC: " + current_location);

        if (li_text === current_location){
            console.log("FOUND MATCH");
            lists[i].className = "active";
        } else if (current_location != "" && li_text === "home") {
            lists[i].className = "";
        }
    }


    

});