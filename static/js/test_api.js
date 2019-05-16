divvy = document.getElementById("test_div");
fetch('./api_path', {loc1:131, loc2: 230})
  .then(function(response) {
    divvy.innerHTML =  response.JSON;
  });
