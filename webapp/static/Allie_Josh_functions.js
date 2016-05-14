getData= {};
getDetail = {};
currentYear = 0;
var baseUrl =  'http://thacker.mathcs.carleton.edu:5147/politicalconflicts/'
function onChangeYear() {
 /*This is used when the user clicks the change year button.
  * It makes an api request of the country data
  * then calls changeYearCallback, updating the global getData variable*/
     var yearEntered = getEnteredYear();
    var url = baseUrl +'twoletter/'+ yearEntered;
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
   /*This allows the user to hit enter to update the year*/
    if (keyEvent.keyCode == 13){
        onChangeYear();
    }}


function changeYearCallback(responseText) { 
    /*This converts the string into a JSON object to get the
     * dictionary data, then uses that data to make the map*/
    getData = JSON.parse(responseText);
    document.getElementById('world-map-gdp').innerHTML = "";
    makeMap();
}

function getEnteredYear() {
    /*This returns the year that is entered by the user*/
    var yearElement = document.getElementById('year_entered');
    currentYear = yearElement.value;
    return yearElement.value;
}

function onChangeCountry() {
    /*This is used when the user clicks the search country button.
     * It makes an api request of the country data
     * then calls changeCountryCallback, updating the global getData variable*/
    var countryEntered = getEnteredCountry();
    var url = baseUrl+'detail/'+countryEntered;
    xmlHttpRequest = new XMLHttpRequest();
    xmlHttpRequest.open('get', url);

    xmlHttpRequest.onreadystatechange = function() {
            if (xmlHttpRequest.readyState == 4 && xmlHttpRequest.status == 200) {
                changeCountryCallback(xmlHttpRequest.responseText);
            }
        };

    xmlHttpRequest.send(null);
}

function changeCountryCallback(responseText) { 
    /*This converts the string into a JSON obkect to get the 
     * dictionary data, then uses the data to make the map.
     * It also calls onChangeHighestYear to update the current year*/ 
    getData = JSON.parse(responseText);
    onChangeHighestYear();
    document.getElementById('world-map-gdp').innerHTML = "";
    makeMap();
}

function onChangeHighestYear() {
   /*This makes an api request to get the year being used to create the current map
    * (by finding the highest severity year for the selected country).
    * And then calls changeHighestYearCallback*/
    var countryEntered = getEnteredCountry();
    var url = baseUrl+'highestYear/'+countryEntered;
    xmlHttpRequest = new XMLHttpRequest();
    xmlHttpRequest.open('get', url);

    xmlHttpRequest.onreadystatechange = function() {
            if (xmlHttpRequest.readyState == 4 && xmlHttpRequest.status == 200) {
                changeHighestYearCallback(xmlHttpRequest.responseText);
            }
        };

    xmlHttpRequest.send(null);
}

function changeHighestYearCallback(responseText) { 
    /*This updates the currentYear global variable to the new year*/
    currentYear = JSON.parse(responseText);
}



function getEnteredCountry() {
    /*This returns the text from the search country box*/
    var countryElement = document.getElementById('country_entered');
    return countryElement.value;
}


function getDetailForRollover(code) {
    /*This is used when a user clicks on a country in the map.
     * It makes an api request to get details about that country.
     * It calls getDetailCallback*/
    var yearEntered = currentYear;
    var url = baseUrl+ yearEntered + '/' + code;
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
    /*It sets the global variable getDetail to the data from the most
     * recently clicked country.
     * It uses this data to update the inner HTML of various elements to display
     * this data on the website*/
    getDetail =JSON.parse(responseText);
    getDetail = getDetail[0];
    console.log(getDetail);
    var description = getDetail['description'];
    var sum = getDetail['sum'];
    var country = getDetail['country'];
    var year = getDetail['year'];
    
    var detailHTMLTest = document.getElementById('details');
    var countryNameHTML = document.getElementById('cntry');
    countryNameHTML.innerHTML = "Country";
    detailHTMLTest.innerHTML = description;
    var countryHTMLTest = document.getElementById('country');
    countryHTMLTest.innerHTML = country;
    var sumHTMLTest = document.getElementById('sum');
    sumHTMLTest.innerHTML = sum;
    var yearHTMLTest = document.getElementById('year');
    yearHTMLTest.innerHTML = year;
    var countryNameHTML = document.getElementById('Yr');
    countryNameHTML.innerHTML = "Year";
    var countryNameHTML = document.getElementById('Severity');
    countryNameHTML.innerHTML = "Political Violence Severity";
    var countryNameHTML = document.getElementById('dts');
    countryNameHTML.innerHTML = "Description";
}


