// Draws inner network

function drawInnerNetwork(){
    // create an array with nodes
  // var nodes = new vis.DataSet([
  //   {id: 1, label: 'Node 1'},
  //   {id: 2, label: 'Node 2'},
  //   {id: 3, label: 'Node 3'},
  //   {id: 4, label: 'Node 4'},
  //   {id: 5, label: 'Node 5'}
  // ]);

  // // create an array with edges
  // var edges = new vis.DataSet([
  //   {from: 1, to: 3},
  //   {from: 1, to: 2},
  //   {from: 2, to: 4},
  //   {from: 2, to: 5},
  //   {from: 3, to: 3}
  // ]);

  // // create a network
  // var container = document.getElementById('viz');
  // var data = {
  //   nodes: nodes,
  //   edges: edges
  // };
  // var options = {};
  // var network = new vis.Network(container, data, options);

  var sample_data = [
    {"name": "alpha", "size": 10},
    {"name": "beta", "size": 12},
    {"name": "gamma", "size": 30},
    {"name": "delta", "size": 26},
    {"name": "epsilon", "size": 12},
    {"name": "zeta", "size": 26},
    {"name": "theta", "size": 11},
    {"name": "eta", "size": 24}
  ];

  var connections = [
    {"source": "alpha", "target": "beta"},
    {"source": "alpha", "target": "gamma"},
    {"source": "beta", "target": "delta"},
    {"source": "beta", "target": "epsilon"},
    {"source": "zeta", "target": "gamma"},
    {"source": "theta", "target": "gamma"},
    {"source": "eta", "target": "gamma"}
  ];

  
  var visualization = d3plus.viz()
    .container("#viz")
    .type("network")
    .data(sample_data)
    .edges(connections)
    .size("size")
    .id("name")
    .mouse(true)
    .draw();

}