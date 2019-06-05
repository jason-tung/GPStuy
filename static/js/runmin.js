// divvy = document.getElementById("test_div");
// fetch('/api_path/', {'loc1':131, 'loc2': 230})
//   .then(function(response) {
//       console.log("hello");
//       console.log();
//     divvy.innerHTML =  response.JSON;
//   });

var bodstr = `
    <svg id="vimage1" height="500" width="500" style="border: 1px solid;"></svg>
    <br>
    <br>
    <svg id="vimage2" height="500" width="500" style="border: 1px solid;"></svg>
`;

var first_time = true;

var same_floor = false;

var sbtn = document.getElementById("searchbtn");

var rdiv = document.getElementById("replace-here");

sbtn.addEventListener('click', function () {
    if (first_time) {
        rdiv.innerHTML = bodstr;

    }
    ;
    var s1 = document.getElementById("s1").value;

        console.log("s1: " + s1);
    var s2 = document.getElementById("s2").value;
    find(s1, s2);


});

function do_stuff(maze, pic) {
    var dim1 = [maze.length, maze[0].length];
    pic.setAttribute("height", dim1[0] * 10);
    pic.setAttribute("width", dim1[1] * 10);
    for (var i = 0; i < maze.length; i++) {
        for (var j = 0; j < maze[0].length; j++) {
            var c = document.createElementNS("http://www.w3.org/2000/svg", "rect");
            // console.log(c);
            c.setAttribute("height", 10);
            c.setAttribute("width", 10);
            c.setAttribute("x", 10 * j);
            c.setAttribute("y", 10 * i);
            c.setAttribute("stroke-opacity", "0");
            // console.log(maze[i][j]);
            // if (!maze[i][j]){
            //     console.log("FDSFDSF")
            // }
            switch (maze[i][j]) {
                case "@":
                    c.setAttribute("fill", "green");
                    break;
                case "#":
                    c.setAttribute("fill", "tan");
                    break;
                case " ":
                    c.setAttribute("fill", "white");
                    break;
                case ".":
                    c.setAttribute("fill", "white");
                    break;
                case "S":
                    c.setAttribute("fill", "blue");
                    break;
                case "E":
                    c.setAttribute("fill", "purple");
                    break;
                default:
                    c.setAttribute("fill", "red");
            }
            pic.appendChild(c)
        }
    }
    if (same_floor){
        var pic2 = document.getElementById("vimage2");
        pic2.remove();
    }
}

function find(a, b) {
    var pic1 = document.getElementById("vimage1");
    var pic2 = document.getElementById("vimage2");
    // var divvy = document.getElementById("test_div");
    // var divvy2 = document.getElementById("test_div2");
    var promise = new Promise(function (resolve, reject) {
        $.get("/api_path/", {'loc1': a, 'loc2': b})
            .done(function (response) {
                resolve(response);
            })
            .fail(function () {
                reject();
            });
    });

    promise.then(function (result) {
        var s1 = document.getElementById("s1").value;
        var s2 = document.getElementById("s2").value;
            if (result == '"poopy"'){
                pic1.remove();
                pic2.remove();
                console.log("fail!!!!!!!!!!!!!");
                rdiv.innerHTML = "<h1> Invalid Room Number(s)! </h1>";
                return;
            }
            console.log("DFSDKJFNDJKSNFKJDSJFKDSJKFDJSF");
            console.log(result);
            var maze = JSON.parse(result);
            var floor1 = maze['f1'];
            var floor2 = maze['f2'];
            console.log("DFSFDS");
            console.log(maze);
            console.log(floor1);
            console.log(floor2);
            function strip_letters(questionText) {
                return questionText.replace(/[A-Za-z]/g, '');
            }
            var t1 = strip_letters(s1);
            var t2 = strip_letters(s2);
            console.log("---+++++----");
            console.log(t1);
            console.log(t2);
            same_floor = t1.substring(0,t1.length-2) == t2.substring(0,t2.length-2);

            // for (var i = 0; i < floor1.length; i++) {
            //     for (var j = 0; j < floor1[0].length; j++) {
            //         divvy.innerHTML += floor1[i][j];
            //     }
            //     // console.log(divvy)
            //     // divvy.innerHTML+=floor1[i];
            //     divvy.innerHTML += "<br>";
            // }
            // for (var i = 0; i < floor2.length; i++) {
            //     for (var j = 0; j < floor2[0].length; j++) {
            //         divvy2.innerHTML += floor2[i][j];
            //     }
            //     // divvy.innerHTML+=floor2[i];
            //     divvy2.innerHTML += "<br>";
            // }
            // divvy.innerHTML.replace(" ", ".");
            // divvy2.innerHTML.replace(" ", ".");

            do_stuff(floor1, pic1);
            do_stuff(floor2, pic2);

        },

        function (err) {
            console.log(err);
        }
    );
};
