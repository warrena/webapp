getData= { "US": 14624.18};
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

function changeYearCallback(responseText) { 
    getData = JSON.parse(responseText);
    console.log(getData);
}

function getEnteredYear() {
    var yearElement = document.getElementById('year_entered');
   yearElement.innerHTML = 'You entered "' + yearElement.value + '"';
    return yearElement.value;
}

