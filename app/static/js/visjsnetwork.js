function drawNetwork (data){

    let nodes = [];
    let edges = [];

    for (var i = 0; i < data.laws.length; i++){
        nodes.push({id : data.laws[i]});
    }

    for (var i = 0; i < data.network.length; i++){
        edges.push({from : data.network[i].from, to : data.network[i].to });
    }

    // Create data


    console.log(nodes);
    console.log(edges);

    var container = document.getElementById("mynetwork");

    var _data = {
        nodes: nodes,
        edges: edges
    };

    var options = {
        nodes: {
            shape: 'dot',
            size: 10
        }
    };

    var network = new vis.Network(container, _data, options);
}