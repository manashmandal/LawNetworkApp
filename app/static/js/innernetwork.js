// Draws inner network
// Entity-Phrase network 
function drawInnerNetwork(_data){

  var entity_phrase_nodes = [];
  var entity_phrase_edges = [];
  




  // create some nodes
      var nodes = [
        {id: 1, label: 'Government', shape: 'text', font:{strokeWidth:4}},
        {id: 2, label: 'Receipt Custody', shape: 'text', font:{strokeWidth:4}},
        {id: 3, label: 'Prosecution of\nAccountants and\sureties', shape: 'text', font:{strokeWidth:4}},
        {id: 4, label: 'Public Accountant',shape: 'text', font:{strokeWidth:4}},
        {id: 5, label: 'Lands Belonging',shape: 'text', font:{strokeWidth:4}}
      ];

      // create some edges
      var edges = [
        {from: 1, to: 2, width: 3, length: 200}, // individual length definition is possible
        {from: 1, to: 3, width: 1, length: 200},
        {from: 1, to: 4, width: 1, length: 200, label:''},
        {from: 1, to: 5, arrows:'to', width: 3, length: 200, label:''}
      ];

      // create a network
      var container = document.getElementById('viz');
      var data = {
        nodes: nodes,
        edges: edges
      };
      var options = {};
      var network = new vis.Network(container, data, options);
}