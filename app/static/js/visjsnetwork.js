//TODO: Optimize
// check if same node was clicked twice

var selected_law;

var _edges_;

var _net;

function drawNetwork (data, stopLoading){

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
    _edges_ = _edges;



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

    _net = network;

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
            

            selected_law = params.nodes[0];

            // Get law text
            $.getJSON($SCRIPT_ROOT + '/api/law_detail/all', {id: params.nodes[0]}).done(function(response){
                $("#volume").append('<span class="label label-success" style="margin-right: 10px;">Volume</span>' + response.detail.volume);
                $("#preamble").append('<span class="label label-primary" style="margin-right: 10px;">Preamble</span>' + response.detail.preamble);


                for (key in response.detail.section_details){
                    $("#sectionTableBody").prepend("<tr><td>" + key + "</td><td>" + response.detail.section_details[key].trim() +"</td></tr>")
                }

                $("#lawModal").modal('toggle');

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
        $.getJSON($SCRIPT_ROOT + '/api/law_inner_detail', {
            id: selected_law
        }).done(function(inner_response){
            drawInnerNetwork(inner_response);
            console.log("Drew inner law network");
        });
    });




    // Edge click show why it is connected 
    // Add the text to edgeDetailsPanelBody
    network.on('selectEdge', function(params){
        // console.log(params);
        console.log(params);

        let selected_edge = _edges.get(params.edges[0]);

        

        // console.log("Selected edge");
        // console.log(selected_edge);

        // Now requesting the details from database
        $.getJSON($SCRIPT_ROOT + '/api/edge_detail',
            {s : "" + selected_edge.from , d: "" + selected_edge.to}
        ).done(function(response){
            console.log(response);
            // Needs edit here
            // $("#edgeDetailPanelBody").append("<p>" + response.detail[0].section_title + "</p>");
            console.log(response.detail);
            response.detail.forEach(function(dat){
                $("#edgeDetailPanelBody").prepend("<p>" + dat.section_detail + "</p>");
                $("#edgeDetailPanelBody").prepend("<p><b>" + dat.section_title + "</b></p>");
            })
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

            // console.log(json.connections);
        });

        // Get amendment data
        $.getJSON("/api/amendments", {id: params.nodes[0]}).done(function(response){
            var amendment_data = [];

            
            
            for (key in response.amendments){
                amendment_data.push({'year' : +key, 'name' : response.title  ,'count' : response.amendments[key]});
            }

            console.log(amendment_data);



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