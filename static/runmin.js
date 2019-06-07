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
                case "]":
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
            if (same_floor){
                var data = gendirections(floor1, false);
                createTable(data);
            }
            else{
                var data1 = gendirections(floor1,false,t2.substring(0,t2.length-2));
                var data2 = gendirections(floor2,true);
                createTable(data1.concat(data2));

            }

        },

        function (err) {
            console.log(err);
        }
    );
};

function gendirections(map,stairs1,floor) {
    var instruct;
    if (stairs1)
        instruct = ['Exit the stairs'];
    else 
        instruct = ['Exit the room'];
    console.log("hi")
    var curX;
    var curY; 
    var curDir;
    var steps =0; 

    for (var i = 0; i < map.length; i++)
    {
        for (var j = 0; j < map[0].length; j++)
        {
            if (map[i][j] == 'S')
            {
                curX = i;
                curY = j ;
            }
        }
    }
    console.log(curX,curY);

    var directions = [[0,1],[-1,0],[0,-1],[1,0]];
    for(var i = 0; i< 4; i++){
        var nextX = curX + directions[i][0]
        var nextY = curY + directions[i][1]
        console.log(nextX,nextY)
        if (map[nextX][nextY] == '@'){
            curDir = i;
            curX = nextX;
            curY = nextY;
            steps++;
        }
    }
    console.log(curDir);
    while(map[curX+directions[curDir][0]][curY+directions[curDir][1]] != 'E' ){
        while (map[curX+directions[curDir][0]][curY+directions[curDir][1]] == "@")
        {
            console.log('while loop started')
            // for(var i = 0; i <4;i++){
            console.log(map[curX+directions[curDir][0]][curY+directions[curDir][1]]);
            console.log(map[curX+directions[curDir][0]][curY+directions[curDir][1]] == "@");
            curX += directions[curDir][0];
            curY += directions[curDir][1];
            console.log(curX,curY);
            steps++; 
        } 

        console.log('hi')
        instruct.push("Move forward " +steps+ " ft.");
        console.log(instruct);
        console.log(steps);
        steps = 0;

        d = directions[(curDir+1)%4 ];
        if(map[curX+d[0]][curY+d[1]] == '@' || map[curX+d[0]][curY+d[1]] == 'E'){
            instruct.push('Turn Left')
            curDir++;
            curDir %= 4;
        }
        else{
            instruct.push('Turn Right')
            if (curDir == 0){
                curDir = 3;
            }
            else{
                curDir--;
            }
        }

        for(var i = 0; i< 4; i++){
            var nextX = curX + directions[i][0];
            var nextY = curY + directions[i][1];
            if (map[nextX][nextY] == 'E'){
                console.log('whats up');
                curDir = i;
            }
        }
    }
    if(floor){
        instruct.push('Take the stairs to Floor ' + floor);
    }
    else{
        instruct.push('You have arrived at your destination.');
        }

    console.log(instruct)
    return instruct;
};

function createTable(dt) {
    var table = document.createElement('table');
    var tableBody = document.createElement('tbody');
    var rhead = document.createElement('tr');
    var ind = document.createElement('th');
    ind.appendChild(document.createTextNode('Step #'));
    var dir = document.createElement('th');
    dir.appendChild(document.createTextNode('Direction'));
    rhead.appendChild(ind);
    rhead.appendChild(dir);
    tableBody.appendChild(rhead);

    for(var i = 0; i < dt.length; i++){
        var row = document.createElement('tr');
        var ind = document.createElement('td');
        ind.appendChild(document.createTextNode(i+1));
        row.appendChild(ind);
        var dir = document.createElement('td');
        dir.appendChild(document.createTextNode(dt[i]));
        row.appendChild(dir);
        tableBody.appendChild(row);

    }
    var box = document.getElementById('container');
    table.appendChild(tableBody);
    table.setAttribute("class", "table table-fixed");
    box.appendChild(table);
  } 
