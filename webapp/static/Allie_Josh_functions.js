getData= {};
getDetail = {};
function onChangeYear() {
    var yearEntered = getEnteredYear();
    var url = 'http://thacker.mathcs.carleton.edu:5147/politicalconflicts/twoletter/'+ yearEntered;
    xmlHttpRequest = new XMLHttpRequest();
    xmlHttpRequest.open('get', url);

    xmlHttpRequest.onreadystatechange = function() {
            if (xmlHttpRequest.readyState == 4 && xmlHttpRequest.status == 200) {
                changeYearCallback(xmlHttpRequest.responseText);
            }
        };

    xmlHttpRequest.send(null);
}
function onKeyPress(keyEvent){
    if (keyEvent.keyCode == 13){
        onChangeYear();
    }}


function changeYearCallback(responseText) { 
    getData = JSON.parse(responseText);
    document.getElementById('world-map-gdp').innerHTML = "";
    getDetailForRollover();
    makeMap();
}

function getEnteredYear() {
    var yearElement = document.getElementById('year_entered');
   yearElement.innerHTML = 'You entered "' + yearElement.value + '"';
    return yearElement.value;
}


function getDetailForRollover() {
    var yearEntered = getEnteredYear();
    var url = 'http://thacker.mathcs.carleton.edu:5147/politicalconflicts/'+ yearEntered;
    xmlHttpRequest = new XMLHttpRequest();
    xmlHttpRequest.open('get', url);

    xmlHttpRequest.onreadystatechange = function() {
            if (xmlHttpRequest.readyState == 4 && xmlHttpRequest.status == 200) {
                getDetailCallback(xmlHttpRequest.responseText);
            }
        };

    xmlHttpRequest.send(null);
}


function getDetailCallback(responseText) {  
    getDetail = JSON.parse(responseText);
    var detailHTMLTest = document.getElementById('details');
    detailHTMLTest.innerHTML = getDetail;
}



