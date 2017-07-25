 // create an array with nodes
// create an array with nodes
  // create an array with nodes
  var nodes = new vis.DataSet([
    {id: 1, label: 'node\none', shape: 'box', color:'#97C2FC'},
    {id: 2, label: 'node\ntwo', shape: 'circle', color:'#FFFF00'},
    {id: 3, label: 'node\nthree', shape: 'diamond', color:'#FB7E81'},
    {id: 4, label: 'node\nfour', shape: 'dot', size: 10, color:'#7BE141'},
    {id: 5, label: 'node\nfive', shape: 'ellipse', color:'#6E6EFD'},
    {id: 6, label: 'node\nsix', shape: 'star', color:'#C2FABC'},
    {id: 7, label: 'node\nseven', shape: 'triangle', color:'#FFA807'},
    {id: 8, label: 'node\neight', shape: 'triangleDown', color:'#6E6EFD'}
  ]);

  // create an array with edges
  var edges = new vis.DataSet([
    {from: 1, to: 8, color:{color:'red'}}//,
    // {from: 1, to: 3, color:'rgb(20,24,200)'},
    // {from: 1, to: 2, color:{color:'rgba(30,30,30,0.8)', highlight:'blue'}},
    // {from: 2, to: 4, color:{inherit:'to'}},
    // {from: 2, to: 5, color:{inherit:'from'}},
    // {from: 5, to: 6, color:{inherit:'both'}},
    // {from: 6, to: 7, color:{color:'#ff0000', opacity:0.3}},
    // {from: 6, to: 8, color:{opacity:0.3}},
  ]);


    // create a network
    var container = document.getElementById('mynetwork');
    var data = {
        nodes: nodes,
        edges: edges
    };
    var options = {interaction:{hover:true}};
    var network = new vis.Network(container, data, options);

    // network.on("click", function (params) {
    //     params.event = "[original event]";
    //     document.getElementById('eventSpan').innerHTML = '<h2>Click event: </h2>' + JSON.stringify(params, null, 4);
    //     console.log('click event, getNodeAt returns: ' + this.getNodeAt(params.pointer.DOM));
    // });
    // network.on("doubleClick", function (params) {
    //     params.event = "[original event]";
    //     document.getElementById('eventSpan').innerHTML = '<h2>doubleClick event:</h2>' + JSON.stringify(params, null, 4);
    // });
    // network.on("oncontext", function (params) {
    //     params.event = "[original event]";    var nodes = new vis.DataSet([
    //     {id: 1, label: 'Node 1', title: 'I have a fucking popup'},
    //     {id: 2, label: 'Node 2', title: 'I have a popup!'},
    //     {id: 3, label: 'Node 3', title: 'I have a popup!'},
    //     {id: 4, label: 'Node 4', title: 'I have a popup!'},
    //     {id: 5, label: 'Node 5', title: 'I have a popup!'}
    // ]);

    // create an array with edges
    // var edges = new vis.DataSet([
    //     {from: 1, to: 3},
    //     {from: 1, to: 2},
    //     {from: 2, to: 4},
    //     {from: 2, to: 5}
    // ]);
    //     document.getElementById('eventSpan').innerHTML = '<h2>oncontext (right click) event:</h2>' + JSON.stringify(params, null, 4);
    // });
    // network.on("dragStart", function (params) {
    //     params.event = "[original event]";
    //     document.getElementById('eventSpan').innerHTML = '<h2>dragStart event:</h2>' + JSON.stringify(params, null, 4);
    // });
    // network.on("dragging", function (params) {
    //     params.event = "[original event]";
    //     document.getElementById('eventSpan').innerHTML = '<h2>dragging event:</h2>' + JSON.stringify(params, null, 4);
    // });
    // network.on("dragEnd", function (params) {
    //     params.event = "[original event]";
    //     document.getElementById('eventSpan').innerHTML = '<h2>dragEnd event:</h2>' + JSON.stringify(params, null, 4);
    // });
    // network.on("zoom", function (params) {
    //     document.getElementById('eventSpan').innerHTML = '<h2>zoom event:</h2>' + JSON.stringify(params, null, 4);
    // });
    // network.on("showPopup", function (params) {
    //     document.getElementById('eventSpan').innerHTML = '<h2>showPopup event: </h2>' + JSON.stringify(params, null, 4);
    // });
    // network.on("hidePopup", function () {
    //     console.log('hidePopup Event');
    // });
    // network.on("select", function (params) {
    //     console.log('select Event:', params);
    // });
    network.on("selectNode", function (params) {

        var edgeId = params.edges[0];

        var connectedEdge = edges.get(edgeId);

        // connectedEdge.color = {'opacity' : .2};
        // connectedEdge.color = "#000000";
        // connectedEdge.color = {opacity: 0.1};
        // connectedEdge.color = {'color': '#FF0000', 'opacity' : 0.5};

        connectedEdge.color = {'color' : 'rgba(255, 0, 0, 0.5)'};

        console.log(connectedEdge.color);
        // connectedEdge.opacity = 1;
        edges.update(connectedEdge);
        console.log(connectedEdge);
    });
    // network.on("selectEdge", function (params) {
    //     console.log('selectEdge Event:', params);
    // });
    // network.on("deselectNode", function (params) {
    //     console.log('deselectNode Event:', params);
    // });
    // network.on("deselectEdge", function (params) {
    //     console.log('deselectEdge Event:', params);
    // });
    // network.on("hoverNode", function (params) {
    //     console.log('hoverNode Event:', params);
    // });
    // network.on("hoverEdge", function (params) {
    //     console.log('hoverEdge Event:', params);
    // });
    // network.on("blurNode", function (params) {
    //     console.log('blurNode Event:', params);
    // });
    // network.on("blurEdge", function (params) {
    //     console.log('blurEdge Event:', params);
    // });
