// divvy = document.getElementById("test_div");
// fetch('/api_path/', {'loc1':131, 'loc2': 230})
//   .then(function(response) {
//       console.log("hello");
//       console.log();
//     divvy.innerHTML =  response.JSON;
//   });
var pic1 = document.getElementById("vimage1");
var pic2 = document.getElementById("vimage2");

var divvy = document.getElementById("test_div");
var divvy2 = document.getElementById("test_div2");

function do_stuff(maze,pic) {
    var dim1 = [maze.length, maze[0].length];
    pic.setAttribute("height", dim1[0] * 20);
    pic.setAttribute("width", dim1[1] * 20);
    for (var i = 0; i < maze.length; i++) {
        for (var j = 0; j < maze[0].length; j++) {
            var c = document.createElementNS("http://www.w3.org/2000/svg", "rect");
            // console.log(c);
            c.setAttribute("height", 20);
            c.setAttribute("width", 20);
            c.setAttribute("rx", 5);
            c.setAttribute("x", 20 * j);
            c.setAttribute("y", 20 * i);
            c.setAttribute("stroke", "black");
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
}


var promise = new Promise(function (resolve, reject) {
    $.get("/api_path/", {'loc1': 101, 'loc2': 202})
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
        // divvy.innerHTML.replace(" ", ".");
        // divvy2.innerHTML.replace(" ", ".");
        do_stuff(floor1,pic1);
        do_stuff(floor2,pic2);
        console.log('gen is being called now');
        instructions = gendirections(floor1,false);
        createTable(instructions);
        // gendirections(floor2);
    },

    function (err) {
        console.log(err);
    }
);

function gendirections(map,stairs) {
    var instruct;
    if (stairs)
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
        instruct.push("Move forward " +steps+ " steps");
        console.log(instruct);
        console.log(steps);
        steps = 0;
        
        if(directions[(curDir+1)%4 ] == '@'){
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
    }
    if(stairs){
        instruct.push('You have arrived at your destination.')
    }
    else{
        instruct.push('Take the stairs to the correct floor')
        }

    console.log(instruct)
    return instruct;
};

function createTable(dt) {
    var table = document.createElement('table');
    var tableBody = document.createElement('tbody');
    var head  = document.createElement('thead');
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
    
    table.appendChild(tableBody);
    table.setAttribute("class", "table");
    document.body.appendChild(table);
  }
  
