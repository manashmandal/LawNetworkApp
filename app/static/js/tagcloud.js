var DAT;


function draw(words_map){

    $("#tagcloud").empty();

    var fill = d3.scale.category20();
    // var words = ;

    d3.layout.cloud().size([300, 300])
                     .words(words_map.map(function(d){
                        return {text: d.word, size: d.freq};
                      }))
                     .padding(5)
                     .rotate(function() { return ~~(Math.random() * 2) * 90; })
                     .font("Impact")
                     .fontSize(function(d) { return d.size; })
                     .on('end', draw)
                     .start();

    function draw(words){
        d3.select('#tagcloud').append('svg')
                .attr('width', 300)
                .attr('height', 300)
            .append('g')
                .attr('transform', "translate(150, 150)")
            .selectAll('text')
                .data(words)
            .enter().append('text')
                .style('font-size', function(d) { return d.size + 'px'; })
                .style('font-family', "Impact")
                .style('fill', function(d, i) { return fill(i); })
                .attr('text-anchor', 'middle')
                .attr('transform', function(d){
                    return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
                })
                .text(function(d) { return d.text; });

    }
    
    
}


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

        
        // stopLoading();


        // Append the sections
        $("#sections").append("<ul>");
        for (let i = 0; i < _data['section_keys'].length; i++){
            // $("#sections").append("<span class='label label-default>'" + _data['section_keys'][i] + "</label>");
            // $("#sections").append(data['section_keys'][i]);

            let value = _data['section_keys'][i];
            if (value !== ""){
                $("#sections").append("<li class='section_keys' id='section_" + i + "'>" + value + "</li>");
            }
                // </br></br>
        }
        $("#sections").append("</ul>");

        $("#sections").css('max-height', $('.modal-body').height() + 'px');

        DAT = _data;
 

        // Add event listener to list items 
        $(".section_keys").on('click', function(){
            console.log(this.id);
            
            let section_key = $("#" + this.id).text();

            // Send get request for data
            $.getJSON("/api/wordcloud", {
                id: law_id,
                key: section_key
            }).done(function(response){
                draw(response.info.words);
                console.log(response);
            });

        });

        $("#lawModal").modal('toggle');
    // console.log(_data);
    // console.log("SELECTED LAW ID " + law_id);
    // stopLoading();
}