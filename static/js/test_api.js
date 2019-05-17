// divvy = document.getElementById("test_div");
// fetch('/api_path/', {'loc1':131, 'loc2': 230})
//   .then(function(response) {
//       console.log("hello");
//       console.log();
//     divvy.innerHTML =  response.JSON;
//   });

var divvy = document.getElementById("test_div");
var divvy2 = document.getElementById("test_div2");

var promise = new Promise(function (resolve, reject) {
    $.get("/api_path/", {'loc1': 131, 'loc2': 230})
        .done(function (response) {
            resolve(response);
        })
        .fail(function () {
            reject();
        });
});

promise.then(function (result) {
        var maze = JSON.parse(result);
        var floor1 = maze['f1'];
        var floor2 = maze['f2'];
        console.log("DFSFDS");
        console.log(maze);
        console.log(floor1);
        console.log(floor2);
        for (var i = 0; i < floor1.length; i++) {
            for (var j = 0; j < floor1[0].length; j++) {
                divvy.innerHTML += floor1[i][j];
            }
            // console.log(divvy)
            // divvy.innerHTML+=floor1[i];
            divvy.innerHTML += "<br>";
        }
        for (var i = 0; i < floor2.length; i++) {
            for (var j = 0; j < floor2[0].length; j++) {
                divvy2.innerHTML += floor2[i][j];
            }
            // divvy.innerHTML+=floor2[i];
            divvy2.innerHTML += "<br>";
        }
        divvy.innerHTML.replace(" ", ".");
        divvy2.innerHTML.replace(" ", ".");

    },

    function (err) {
        console.log(err);
    }
);

