const ENTITY_TYPE = 1;
const SECTION_TYPE = 2;

// Draws inner network
// Entity-Phrase network 
function drawInnerNetwork(_data, law_id, stopLoading){

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
        $("#lawModal").modal('toggle');
        stopLoading();
      }, 100);

      network.on('selectNode', function(params){
        $(".context").unmark();
        let node = entity_phrase_nodes.get(params.nodes[0]);

        console.log("NODE");
        console.log(node);

        $("#sectionTableBody").empty();
        var loadedData;

        $.getJSON('/api/law_detail',{id: "" + law_id, key: 'section_details'}).done(function(response){
            loadedData = response.section_details;

            if (node.type === ENTITY_TYPE){
              for (k in _data.map){
                if (_data.map[k].entity === node.label){
                  $("#sectionTableBody").prepend("<tr><td>" + _data.map[k].section_key + "</td><td>" + loadedData[_data.map[k].section_key].trim() +"</td></tr>");
                }
              }

              // Now Mark it
              $(".context").unmark().mark(node.label, {
                  "accuracy" : {
                    "value" : "exactly",
                    "limiters" : [",", ".", ";"]
                  },
                  "separateWordSearch" : false,
                });
            } else {
                $("#sectionTableBody").prepend("<tr><td>" + node.title + "</td><td>" + loadedData[node.title].trim() +"</td></tr>");

                // Now Mark it
                $(".context").unmark().mark(node.title, {
                    "accuracy" : {
                      "value" : "exactly",
                      "limiters" : [",", ".", ";"]
                    },
                    "separateWordSearch" : false,
                  });
            }
        });
  });
}