// Global variables
var window_height;
var window_width; 

var footer_height;
var navbar_height;

var amendment_panel_height;

var search_result_panel_height;


function updateComponentMeasurements(){
    window_height = $(window).height();
    window_width = $(window).width();

    footer_height = $("#theFooter").height();
    navbar_height = $("#lawSearchNavBar").height();

    search_result_panel_height = $("#searchResultPanel").height() + $("#searchResultPanelBody").height();

    amendment_panel_height = $("#amendmentPanel").height();
}


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


  // Component Size Calculation
  function resizeComponents(){
        let wh = $(window).height();
        let ww = $(window).width();

        //Footer height 
        let fh = $("#theFooter").height();

        // Navbar height
        let nh = $("#lawSearchNavBar").height();

        // Amendment panel height
        let aph = $("#amendmentPanel").height();
        let cleareance = 50;

        let edge_panel_margin_top =  2 * cleareance - (wh - (nh + aph));


        $("#mynetwork").css('height',  wh - cleareance - fh - nh);
        $("#edgeDetailPanel").css('margin-top', "" + (edge_panel_margin_top) + 'px');
  }

//  resizeComponents();


var loadingDone = function(){
    $("#loadingIcon").removeClass("loading");
}

var startLoading = function(){
    $("#loadingIcon").addClass("loading");
}

var loadLawTitles = function(data){


    console.log("BEFORE HEIGHT: " + $("#searchResultPanel").height());

    // Emptying the panel body
    $("#searchResultPanelBody").empty();

    // Adding unordered list
    $("#searchResultPanelBody").append("<ul></ul>");

    for (var i = 0; i < data['laws'].length; i++){
        let law_id = data['laws'][i]
        $.getJSON($SCRIPT_ROOT + '/api/law_detail', {
            id: law_id,
            key: 'title'
        }, function(res){
            // Adding the details
            $("#searchResultPanelBody").append("<li id=" + res['law_id'] + ">" +  "<b>" + res['law_id'] + "</b> - <i>" + res['title'] + "</i>");
        });
    }

    console.log("LOOP ENDS");


    // console.log("AFTER HEIGHT: " + $("#searchResultPanel").height());
    console.log("HEIGHT:  " + search_result_panel_height);


    // Check height of the search panel body and take action according to the height 
}

$(document).ready(function(){
    drawNetwork();

    // Clears input text
    $("#clearButton").click(function(event){
        event.preventDefault();
        $("#keywordSearchInput").val("");
        $("#searchResultPanelBody").empty();
    });


    $("#searchButton").click(function(event){
        

        event.preventDefault();
        // console.log("Default action prevented");
        

        // Send Jquery request for searching
        let search_keywords = $("#keywordSearchInput").val();

        // Additional parameters
        let _ngram = $("#excludeSingleKeywordCheckBox").prop('checked') ? 1 : 0;
        let _exclude_unigram = $("#phraseOnlyCheckBox").prop('checked') ? 1 : 0;
        
        // Set loading 
        startLoading();
        // Requests for network data 
        $.getJSON($SCRIPT_ROOT + "/api/search_law", {
            q: search_keywords,
            ngram: _ngram,
            exclude_unigram: _exclude_unigram
        }, function(data){
            loadLawTitles(data);
        })
        .then(loadingDone)
        .then(updateComponentMeasurements);

        console.log(search_keywords);
    });

    $(window).resize(function(){
        // Redraws the network 
        setTimeout(drawNetwork(), 1000);
        // resizeComponents();
  });
});
  