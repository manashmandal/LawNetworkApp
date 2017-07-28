
var connected_edges;
var all_edges;
var all_edge_ids = [];

//TODO: Optimize
function drawNetwork (data, stopLoading){

    let nodes = [];
    let edges = [];

    for (var i = 0; i < data.laws.length; i++){
        nodes.push({id : data.laws[i], label: "" + data.laws[i], title: data.id_title_map[data.laws[i]]});
    }

    for (var i = 0; i < data.network.length; i++){
        edges.push({from : data.network[i].from, to : data.network[i].to });
    }

    // Create data


    let _nodes = new vis.DataSet(nodes);
    let _edges = new vis.DataSet(edges);

    all_edges = _edges;

    // Getting all data
    for (key in all_edges._data){
        all_edge_ids.push(key);
    }

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

    // var options = {
    //     nodes: {
    //         shape: 'dot',
    //         size: 15
    //     }
    // };

    var network = new vis.Network(container, _data, options);

    // Loading done
    // stopLoading();

    network.on('stabilized', function(){
        stopLoading();
    });

     // Add less opacity
        for (var i = 0; i < all_edge_ids.length; i++){
            let connected_edge = _edges.get(all_edge_ids[i]);
            try {
                connected_edge.color = {color : 'rgba(255, 0, 0, 0.1)'};
                _edges.update(connected_edge);
            } catch(error){
                console.log(error);
            }
        }

    console.log("ALL EDGE ID");
    console.log(all_edge_ids);

    // On Double click reset it 
    network.on('selectNode', function(params){

        // let remaining_ids = _.difference(
        //     all_edge_ids, params.edges
        // )

        // console.log("REMAINING EDGES");
        // console.log(remaining_ids);        
        
        // // Add less opacity
        // for (var i = 0; i < remaining_ids.length; i++){
        //     let connected_edge = _edges.get(remaining_ids[i]);
        //     try {
        //         connected_edge.color = {color : 'rgba(255, 0, 0, 0.1)'};
        //         _edges.update(connected_edge);
        //     } catch(error){
        //         console.log(error);
        //     }
        // }
    });
}