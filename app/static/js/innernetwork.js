// Draws inner network
// Entity-Phrase network 
function drawInnerNetwork(_data){

  // console.log("Inner network viz");

  // console.log(_data);

  var entity_phrase_nodes = [];
  var entity_phrase_edges = [];
  
  // Inner network option
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


        _.each(_data.edges, function(e){
          entity_phrase_edges.push({from: e.from, to : e.to, length: 50, color: {color: 'rgba(0, 255, 0, 0.3)'}});
        });


        _.each(_data.nodes, function(n){
          entity_phrase_nodes.push({id: n.id, shape: 'text', label: n.label, font: {strokeWidth: 5}});
        });

        
        entity_phrase_edges = new vis.DataSet(entity_phrase_edges);
        entity_phrase_nodes = new vis.DataSet(entity_phrase_nodes);


  // // create some nodes
  //     var nodes = [
  //       {id: 1, label: 'Government', shape: 'text', font:{strokeWidth:4}},
  //       {id: 2, label: 'Receipt Custody', shape: 'text', font:{strokeWidth:4}},
  //       {id: 3, label: 'Prosecution of\nAccountants and\sureties', shape: 'text', font:{strokeWidth:4}},
  //       {id: 4, label: 'Public Accountant',shape: 'text', font:{strokeWidth:4}},
  //       {id: 5, label: 'Lands Belonging',shape: 'text', font:{strokeWidth:4}}
  //     ];

  //     // create some edges
  //     var edges = [
  //       {from: 1, to: 2, width: 3, length: 200}, // individual length definition is possible
  //       {from: 1, to: 3, width: 1, length: 200},
  //       {from: 1, to: 4, width: 1, length: 200, label:''},
  //       {from: 1, to: 5, arrows:'to', width: 3, length: 200, label:''}
  //     ];

  //     nodes = new vis.DataSet(nodes);
  //     edges = new vis.DataSet(edges);

      // create a network
      var container = document.getElementById('viz');

      var data = {
        nodes: entity_phrase_nodes,
        edges: entity_phrase_edges
      };
      // var options = {};
      var network = new vis.Network(container, data, options);

      setTimeout(function(){
        network.stopSimulation();
      }, 100);

      network.on('selectNode', function(params){
        $(".context").unmark();
        console.log("Clicked on a node");
        let node = entity_phrase_nodes.get(params.nodes[0]);
        console.log(node.label);


        $(".context").unmark().mark(node.label, {
          "accuracy" : {
            "value" : "exactly",
            "limiters" : [",", ".", ";"]
          },
          "separateWordSearch" : false,
        });

      });
}