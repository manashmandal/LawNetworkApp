
  function drawNetwork(){
    // create an array with nodes
    var nodes = new vis.DataSet([
        {id: 1, label: 'Node 1'},
        {id: 2, label: 'Node 2'},
        {id: 3, label: 'Node 3'},
        {id: 4, label: 'Node 4'},
        {id: 5, label: 'Node 5'}
    ]);

    // create an array with edges
    var edges = new vis.DataSet([
        {from: 1, to: 3},
        {from: 1, to: 2},
        {from: 2, to: 4},
        {from: 2, to: 5},
        {from: 3, to: 3}
    ]);

    // create a network
    var container = document.getElementById('mynetwork');
    var data = {
        nodes: nodes,
        edges: edges
    };
    var options = {};
    var network = new vis.Network(container, data, options);
  }

  function resizeComponents(){
        let window_height = $(window).height();
        let window_width = $(window).width();

        let footer_height = $("#theFooter").height();
        let navbar_height = $("#lawSearchNavBar").height();

        let amendment_panel_height = $("#amendmentPanel").height();
        let cleareance = 50;

        let edge_panel_margin_top =  2 * cleareance - (window_height - (navbar_height + amendment_panel_height));


        $("#mynetwork").css('height',  window_height - cleareance - footer_height - navbar_height);
        $("#edgeDetailPanel").css('margin-top', "" + (edge_panel_margin_top) + 'px');
  }

//  resizeComponents();



  // ------------- Component Size Calculations ------------------- //

$(document).ready(function(){
    resizeComponents();
    drawNetwork();


    $("#searchButton").click(function(event){
        event.preventDefault();
        // console.log("Default action prevented");
        $("#loadingIcon").addClass("loading");

        // Send Jquery request for searching
        let search_keywords = $("#keywordSearchInput").val();

        // Additional parameters
        let _ngram = $("#excludeSingleKeywordCheckBox").prop('checked') ? 1 : 0;
        let _exclude_unigram = $("#phraseOnlyCheckBox").prop('checked') ? 1 : 0;
        

        // Requests for network data 
        $.getJSON($SCRIPT_ROOT + "/api/search_law", {
            q: search_keywords,
            ngram: _ngram,
            exclude_unigram: _exclude_unigram
        }, function(data){
            console.log(data);
            $("#loadingIcon").removeClass("loading");
        });

        console.log(search_keywords);
    });

    $(window).resize(function(){
        
        // Redraws the network 
        setTimeout(drawNetwork(), 1000);
        resizeComponents();
  });
});
  