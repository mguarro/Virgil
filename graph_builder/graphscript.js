var temp = $.getJSON("graph.json", function(json) {
    makeGraph(json); // this will show the info it in firebug console
});

function go123(callback){
  var temp = $.getJSON("")
}


function makeGraph(graphJSON){
console.log(graphJSON)

//probably not the best way of scaling, but it's better than nothing
var i
var maxX = 0
var maxY = 0 
for(i=0; i<graphJSON.length;i++){
  var cx = graphJSON[i].x_axis;
  var cy = graphJSON[i].y_axis;
  if(Math.abs(cx)>maxX){
    maxX = cx
  }
  if(Math.abs(cy)>maxY){
    maxY = cy
  }
}

var cSize = 800; //container size

var maxT  = maxX;
if(maxY>maxT){
  maxT = maxY;
}

var circleSize = 10; //radius of dots

var sf = (cSize-2*circleSize)/(2*maxT); // scaling factor

var shift = cSize/2; //



transformString = "".concat("translate(",shift.toString(),",",shift.toString(),") scale(",sf.toString(),")");



var svgContainer = d3.select("body").append("svg")
                                     .attr("width", cSize)
                                    .attr("height", cSize);

var circleGroup = svgContainer.append("g")
.attr("transform",transformString);


var circles = circleGroup.selectAll("circle")
.data(graphJSON)
.enter()
.append("svg:a")
.attr("xlink:href",function(d){return d.doi;})
.append("circle");


                          

var circleAttributes = circles
                          .attr("cx", function (d) { return d.x_axis; })
                          .attr("cy", function (d) { return d.y_axis; })
                          .attr("r", circleSize/sf )
                          .style("fill", "red")
                          .append("svg:title")
                          .text(function(d){return d.doi;});
                          
                        }
                        




// console.log("hello")

// var spaceCircles = [30,70,110];

// var jsonCircles = [
  // {
   // "x_axis": 30,
   // "y_axis": 30,
   // "radius": 20,
   // "color" : "green"
  // }, {
   // "x_axis": 70,
   // "y_axis": 70,
   // "radius": 20,
   // "color" : "purple"
  // }, {
   // "x_axis": 110,
   // "y_axis": 100,
   // "radius": 20,
   // "color" : "red"
// }];

// function colorCircles(d){
	// if (d === 30){
		// return "green"
	// }
	// if (d === 70){
		// return "purple"
	// }
	// if (d === 110){
		// return "red"
	// }
// }

// var svgContainer = d3.select("body").append("svg")
// .attr("width",200)
// .attr("height",200)
// .style("border","1px solid black");

// var circles = svgContainer.selectAll("circle")
// .data(jsonCircles)
// .enter()
// .append("circle")

// var circleAttributes = circles
// .attr("cx",function(d) {return d.x_axis;})
// .attr("cy",function(d) {return d.y_axis;})
// .attr("r",function(d) {return d.radius;})
// .style("fill",function(d) {return d.color;});

// var circleAttributes = circles.attr("cx",function(d) {return d;})
// .attr("cy",function(d) {return d;})
// .attr("r",20)
// .style("fill",function (d){return colorCircles(d)});