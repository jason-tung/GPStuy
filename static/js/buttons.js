var s1 = document.getElementById("s1");
var s2 = document.getElementById("s2");

var row = [];
for (var i = 0; i < 10; i ++){
  row.push({});
  try {
    // row[i].room = document.getElementById(i).innerHTML;
    row[i].start = document.getElementById("s_" + i);
    row[i].start.room = document.getElementById(i).innerHTML;
    row[i].end = document.getElementById("e_" + i);
    row[i].end.room = document.getElementById(i).innerHTML;
  }
  catch {
    row[i] = null;
  }
}

for (var i = 0; i < row.length; i ++){
  if (!row[i]){
    row.splice(i, 1);
    i --;
  }
}
//
for (var i = 0; i < row.length; i ++){

  row[i].start.addEventListener('click', function(){
    console.log(this);
    for (var j = 0; j < row.length; j ++)
      row[j].start.setAttribute("class", "btn btn-secondary");
    s1.setAttribute("value", this.room);
    this.setAttribute("class", "btn btn-primary");
  });

  row[i].end.addEventListener('click', function(){
    for (var j = 0; j < row.length; j ++)
      row[j].end.setAttribute("class", "btn btn-secondary");
    s2.setAttribute("value", this.room);
    this.setAttribute("class", "btn btn-primary");
  });
}
