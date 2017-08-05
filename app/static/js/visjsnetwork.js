//TODO: Optimize
// check if same node was clicked twice

var selected_law;


function drawNetwork (data, stopLoading){

    $("#edgeDetailPanelBody").empty();

    let nodes = [];
    let edges = [];

    for (var i = 0; i < data.laws.length; i++){
        nodes.push({id : data.laws[i], label: "" + data.laws[i], title: data.id_title_map[data.laws[i]]});
    }

    for (var i = 0; i < data.network.length; i++){
        edges.push({from : data.network[i].from, to : data.network[i].to, color: { color : 'rgba(255, 0, 0, 0.1)'} });
    }

    // Create data

    let _nodes = new vis.DataSet(nodes);
    let _edges = new vis.DataSet(edges);



    var container = document.getElementById("mynetwork");

    var _data = {
        nodes: _nodes,
        edges: _edges
    };


    var options = {
        "nodes": {
            "borderWidthSelected": 8
        },
        "edges": {
            "arrows": {
            "to": {
                "enabled": true,
                "scaleFactor" : 0.7
            },
            "from": {
                "enabled": true,
                "scaleFactor" : 0.7
            }
            },
            "scaling": {
            "min": 39,
            "max": 73
            },
            "smooth": {
            "forceDirection": "none"
            }
        },
        "interaction": {
            "hover": true
        },
        "physics": {
            "minVelocity": 0.75
        }
        };


    var network = new vis.Network(container, _data, options);


    network.on('stabilized', function(){
        stopLoading();
    });


    // Stabilize the network after two seconds
    setTimeout(function(){
        network.stopSimulation();
    }, 2000);

    // On Double click initiate a modal to show the law text and inner graph 
    network.on('doubleClick', function(params){
        console.log(params);
        

        // If clicked on a law or not
        if (params.nodes.length > 0){
            $("#lawModalTitle").text(data.id_title_map[params.nodes[0]]);
            
            //
            startLoading();
            

            selected_law = params.nodes[0];

            // Get law text
            $.getJSON($SCRIPT_ROOT + '/api/law_detail/all', {id: params.nodes[0]}).done(function(response){

                $("#volume").append('<span class="label label-success" style="margin-right: 10px;">Volume</span>' + response.detail.volume);
                $("#preamble").append('<span class="label label-primary" style="margin-right: 10px;">Preamble</span>' + response.detail.preamble);

            });


            $.getJSON($SCRIPT_ROOT + '/api/law_inner_detail/phrase_entity', {
                id: selected_law
        }).done(function(inner_response){
            drawInnerNetwork(inner_response, selected_law, stopLoading);
            console.log("Drew inner law network");
        });

        }
    });

    $("#lawModal").on('hide.bs.modal', function(){
        // Empty texts
        $("#volume").empty();
        $("#preamble").empty();
        $("#sectionTableBody").empty();
        $("#viz").empty();
        $("#amendmentPanelBody").empty();
        $("#edgeDetailPanelBody").empty();
    });


    $("#lawModal").on('show.bs.modal', function(){


        // Fix Size Here
        // $("#lawModalBody").css('height', '500px');


        // Why not phase entity route?
        // $.getJSON($SCRIPT_ROOT + '/api/law_inner_detail/phrase_entity', {
        //     id: selected_law
        // }).done(function(inner_response){
        //     drawInnerNetwork(inner_response, selected_law, stopLoading);
        //     console.log("Drew inner law network");
        //     loadingDone();
        // });
    });



    // Edge click show why it is connected 
    // Add the text to edgeDetailsPanelBody
    network.on('selectEdge', function(params){
        $("#edgeDetailPanelBody").empty();
        $("#edgeDetailPanel").removeClass('panel-warning').addClass('panel-success');
     

        let selected_edge = _edges.get(params.edges[0]);

        // Now requesting the details from database
        $.getJSON($SCRIPT_ROOT + '/api/edge_detail',
            {s : "" + selected_edge.from , d: "" + selected_edge.to}
        ).done(function(response){

            $("#connectionDetailsTitle").empty();
            $("#connectionDetailsTitle").append("Connection between : <b>" + selected_edge.from + "</b> and <b>" + selected_edge.to + "</b>");

            response.detail.forEach(function(dat){
                $("#edgeDetailPanelBody").prepend("<p>" + dat.section_detail + "</p>");
                $("#edgeDetailPanelBody").prepend("<p><b>" + dat.section_title + "</b></p>");
            });
            
        }).fail(function(){
            $("#edgeDetailPanelBody").empty();
            $("#connectionDetailsTitle").empty();
            $("#edgeDetailPanel").removeClass('panel-success').addClass('panel-warning');
            $("#edgeDetailPanelBody").append("<div class='alert alert-danger'>Connection Details Not Found!</div>");
            $("#connectionDetailsTitle").append("Connection between : <b>" + selected_edge.from + "</b> and <b>" + selected_edge.to + "</b> <i>NOT FOUND</i>");
        });

    });
    
    

    // On Double click reset it 
    network.on('selectNode', function(params){

        $("#amendmentPanelBody").empty();

        // Remove previous highlight
        $("#resultList>li").removeClass('highlight');
        
        
        // Send request to get connected nodes
        // Mainly used to highlight the search results
        $.getJSON($SCRIPT_ROOT + '/api/connected_laws', {
            id: params.nodes[0]
        }).done(function(json){
            // Now highlight the search results from the connected law ids
            _.each(json.connections, function(connected_node_id){
                $("#" + connected_node_id).addClass("highlight");
            });

        });

        // Get amendment data
        $.getJSON("/api/amendments", {id: params.nodes[0]}).done(function(response){
            var amendment_data = [];

            
            for (key in response.amendments){
                amendment_data.push({'year' : +key, 'name' : response.title  ,'count' : response.amendments[key]});
            }


            $("#amendmentPanelTitle").text("Showing Amendments of law : " + params.nodes[0]);

            var visualization = d3plus.viz()
            .container("#amendmentPanelBody")
            .data(amendment_data)
            .type("line")
            .id("name")
            .x("year")
            .height($("#amendmentPanelBody").height())
            .y("count")
            .draw();
        });
    });
}