//TODO: Optimize
// check if same node was clicked twice

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

    // On Double click initiate a modal to show the law text and inner graph 
    network.on('doubleClick', function(params){
        console.log(params);
        // If clicked on a law or not
        if (params.nodes.length > 0){
            $("#lawModalTitle").text(data.id_title_map[params.nodes[0]]);
            


            // Get law text
            $.getJSON($SCRIPT_ROOT + '/api/law_detail/all', {id: params.nodes[0]}).done(function(response){
                $("#volume").append('<span class="label label-default" style="margin-right: 10px;">Volume</span>' + response.detail.volume);

                $("#lawModal").modal('toggle');
            });
            

        }
    });

    $("#lawModal").on('hide.bs.modal', function(){
        
        // Empty texts
        $("#volume").empty();
    });
    

    // On Double click reset it 
    network.on('selectNode', function(params){


        // Remove previous highlight
        $("#resultList>li").removeClass('highlight');
        
        
        // Send request to get connected nodes
        $.getJSON($SCRIPT_ROOT + '/api/connected_laws', {
            id: params.nodes[0]
        }).done(function(json){
            // Now highlight the search results from the connected law ids

            _.each(json.connections, function(connected_node_id){
                $("#" + connected_node_id).addClass("highlight");
            });

            // console.log(json.connections);
        });

    });
}