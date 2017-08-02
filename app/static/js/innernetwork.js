const ENTITY_TYPE = 1;
const SECTION_TYPE = 2;

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
          entity_phrase_edges.push({from: e.from, to : e.to, length: 150, color: {color: 'rgba(0, 220, 0, 0.3)'}});
        });


        _.each(_data.nodes, function(n){
          if (n.type === "entity"){
            entity_phrase_nodes.push({id: n.id, type: ENTITY_TYPE , shape: 'text', label: n.label, font: {strokeWidth: 5}});
          } else{
            entity_phrase_nodes.push({id: n.id, type: SECTION_TYPE ,label: "" + n.id, title: n.label})
          }
        });

        
        entity_phrase_edges = new vis.DataSet(entity_phrase_edges);
        entity_phrase_nodes = new vis.DataSet(entity_phrase_nodes);


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

        if (node.type === ENTITY_TYPE){
          $(".context").unmark().mark(node.label, {
            "accuracy" : {
              "value" : "exactly",
              "limiters" : [",", ".", ";"]
            },
            "separateWordSearch" : false,
          });
        } else {
          $(".context").unmark().mark(node.title, {
            "accuracy" : {
              "value" : "exactly",
              "limiters" : [",", ".", ";"]
            },
            "separateWordSearch" : false,
          });
        }

      });
}