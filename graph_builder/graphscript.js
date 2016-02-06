var temp = $.getJSON("graph.json", function(json) {
    makeGraph(json); // this will show the info it in firebug console
});

function go123(callback){
  var temp = $.getJSON("")
}

function makeGraph(graphJSON){
console.log(graphJSON)
// graphJSON = [{"y_axis": 0.12530908979457525, "x_axis": -0.25207039458369607, "doi": "http://dx.doi.org/10.1109/iv.2010.49"}, {"y_axis": 0.18238104596440313, "x_axis": 0.09602556220205033, "doi": "http://dx.doi.org/10.1109/tvcg.2009.165"}, {"y_axis": -0.33954536243945233, "x_axis": -0.40436306278880246, "doi": "http://dx.doi.org/10.1109/c5.2011.18"}, {"y_axis": 0.40454223674394102, "x_axis": -0.079032422820886433, "doi": "http://dx.doi.org/10.1109/wmute.2010.24"}, {"y_axis": 1.1250837303330676, "x_axis": 1.1517580517578063, "doi": "http://dx.doi.org/10.1109/icsc.2010.19"}, {"y_axis": -0.1476453569112543, "x_axis": 0.31598812237293789, "doi": "http://dx.doi.org/10.1109/ahs.2014.6880151"}, {"y_axis": -0.18869968686055205, "x_axis": -0.0029228676567548142, "doi": "http://dx.doi.org/10.1109/tvcg.2014.2388208"}, {"y_axis": -0.60993883379898284, "x_axis": -0.014102677752548502, "doi": "http://dx.doi.org/10.1109/jdt.2013.2292051"}, {"y_axis": -0.55148680609178824, "x_axis": -0.81128029721657979, "doi": "http://dx.doi.org/10.1109/wivec.2013.6698240"}]

// console.log(graphJSON)
// var graphJSON = require("./graph.json")

// var graphJSON = [
//    { "x_axis": 10, "y_axis": 10, "height": 20, "width":20, "color" : "green" },
//    { "x_axis": 160, "y_axis": 40, "height": 20, "width":20, "color" : "purple" },
//    { "x_axis": 70, "y_axis": 70, "height": 20, "width":20, "color" : "red" }];

var svgContainer = d3.select("body").append("svg")
                                     .attr("width", 1000)
                                    .attr("height", 1000);

var circleGroup = svgContainer.append("g")
.attr("transform","translate(300,300) scale(10,10)");

var circles = circleGroup.selectAll("circle")
.data(graphJSON)
.enter()
.append("circle")


var circleAttributes = circles
                          .attr("cx", function (d) { return d.x_axis*10; })
                          .attr("cy", function (d) { return d.y_axis*10; })
                          .attr("r", 1 )
                          .style("fill", "red");
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