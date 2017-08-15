// </Manash>


// Loads Ttile and Draws The Network

var loadingDone = function(){
    $("#loadingIcon").removeClass("loading");
}

var startLoading = function(){
    $("#loadingIcon").addClass("loading");
}


// 
var loadLawTitlesAndDrawNetwork = function(data){

    // Emptying the panel body
    $("#searchResultPanelBody").empty();

    // Adding unordered list
    $("#searchResultPanelBody").append("<ul id='resultList'></ul>");

    // Add the count
    $("#searchResultPanelTitle").empty();
    $("#searchResultPanelTitle").append("Total Law Found <b><i>" + data.laws.length + "</b></i>");
    // For debugging purpose
    loaded_data = data;

    for (var i = 0; i < data.laws.length; i++){
        $("#resultList").append("<li id=" + data.laws[i] + " class='lawResult'>" +  "<b>" + data.laws[i] + "</b> - <i>" + data.id_title_map[data.laws[i]] + "</i>");
    }


    let net = drawNetwork(data, loadingDone);

    // Bind network and search result prop
    $(".lawResult").click(function(params){
        console.log(this.id);
        console.log(net);
    });

    // loadingDone();
}

$(document).ready(function(){
    // drawNetwork();

    // Clears input text
    $("#clearButton").click(function(event){
        event.preventDefault();
        // Empty keyword search bar
        $("#keywordSearchInput").val("");
        // Empty Search result panel body
        $("#searchResultPanelBody").empty();
        // Empty Visualization 
        $("#mynetwork").empty();

        $("#searchResultPanelBody").empty();
        $("#amendmentPanelBody").empty();
        $("#edgeDetailPanelBody").empty();

        $("#searchResultPanelTitle").empty().append("Search Result");
        $("#searchResultPanelBody").append("<h3>Search Result Will Be Shown Here </br> <b>Enter Keywords in the Search Area to Begin</b></h3>");
        $("#amendmentPanelBody").append("<h3>Amendment Visualization Plot <b>Click On A Node to View</b>");
        $("#amendmentPanelTitle").empty().append("Amendments");
        $("#edgeDetailPanelBody").append("<h3>The section that connects two laws will be shown here</h3>");
    });


    $("#searchButton").click(function(event){
    
        event.preventDefault();
        // console.log("Default action prevented");
        

        // Send Jquery request for searching
        let search_keywords = $("#keywordSearchInput").val();


        // Save the keyword
        $.getJSON('/api/userstat/law_search_term', {term: search_keywords}).done(function(res){
            console.log("SAVED DATA");
        });

        // Additional parameters
        let _ngram = $("#excludeSingleKeywordCheckBox").prop('checked') ? 1 : 0;
        let _exclude_unigram = $("#phraseOnlyCheckBox").prop('checked') ? 1 : 0;
        
        // Set loading 
        startLoading()

        $.getJSON($SCRIPT_ROOT + "/api/search_law", {
            q: search_keywords,
            ngram: _ngram,
            exclude_unigram: _exclude_unigram
        }).done(function(response){
            $("#mynetwork").empty();
            loadLawTitlesAndDrawNetwork(response);
        }).fail(function(){
            loadingDone();
            $("#mynetwork").empty();
            $("#mynetwork").append("<div class='alert alert-warning'><h3 class='text-center'>Nothing Found!</h3></div>");
        });

    });

    // TODO: Handle resizing to fit the viz browser window
    $(window).resize(function(){

    });
});
  