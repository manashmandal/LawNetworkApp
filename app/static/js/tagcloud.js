var DAT;


function drawTagCloud(_data, law_id, stopLoading){


        // Calculate available area
        let clearance = 50;

        // Resize viz
        $("#viz").css('height', $(window).height() - clearance + 'px');
        $("#viz").css('width', $(window).width() / 2.2 - clearance + 'px');
        
        // Resize modal
        $(".modal").css('min-height', $(window).height() + 'px');
        $(".modal").css('max-height', $(window).height()   + 'px');
        $(".modal-body").css('height', $(window).height() - clearance + 'px');
        $(".modal-body").css('max-height', $(window).height() - clearance  + 'px');

        $("#lawModal").modal('toggle');
        // stopLoading();


        // Append the sections
        $("#sections").append("<ul>")
        for (let i = 0; i < _data['section_keys'].length; i++){
            // $("#sections").append("<span class='label label-default>'" + _data['section_keys'][i] + "</label>");
            // $("#sections").append(data['section_keys'][i]);
            let value = _data['section_keys'][i];
            if (value !== "")
                $("#sections").append("<li class='section_keys'>" + value + "</li>");
            // </br></br>
        }
        $("#sections").append("</ul>");

        $("#sections").css('max-height', $('.modal-body').height() + 'px');

        DAT = _data;
 

        // Add event listener to list items 
        $(".section_keys").on('click', function(){
            console.log(this);
        });
    // console.log(_data);
    // console.log("SELECTED LAW ID " + law_id);
    // stopLoading();
}