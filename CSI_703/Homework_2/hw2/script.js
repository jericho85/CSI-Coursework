// Global var for FIFA world cup data
var allWorldCupData;

/**
 * Render and update the bar chart based on the selection of the data type in the drop-down box
 *
 * @param selectedDimension a string specifying which dimension to render in the bar chart
 */
function updateBarChart(selectedDimension) {
    
    var svgBounds = d3.select("#barChart").node().getBoundingClientRect(),
        xAxisWidth = 100,
        yAxisHeight = 70;

    // ******* TODO: PART I *******

    // Create the x and y scales; make
    // sure to leave room for the axes
    var xScale = d3.scale.linear()
                            .domain([0,d3.max(selectedDimension, function(d) {return d[0];})])
                            .range([0,xAxisWidth]);
    var yScale = d3.scale.linear()
                            .domain([0,d3.max(selectedDimension, function(d) {return d[1];})])
                            .range([0,yAxisHeight]);

    // Create colorScale

    // Create the axes (hint: use #xAxis and #yAxis)
    d3.select("#xAxis").axis().scale(xScale).orient("bottomn");
    d3.select("#yAxis").axis().scale(yScale).orient("left");
    svg.append("g").call("#xAxis");
    svg.append("g").call("yAxis");

    // Create the bars (hint: use #bars)
    var svg = d3.select("#bars").append("svg").attr("width",yScale).attr("height",yAxisHeight);
    svg.selectAll("rect")
        .data(selectedDimension)
        .enter()
        .append("rect")
        .attr("x",1)
        .attr("y",1)
        .attr("width",10)
        .attr("height",100)

    // ******* TODO: PART II *******

    // Implement how the bars respond to click events
    // Color the selected bar to indicate is has been selected.
    // Make sure only the selected bar has this new color.

    // Output the selected bar to the console using console.log()

}

/**
 *  Check the drop-down box for the currently selected data type and update the bar chart accordingly.
 *
 *  There are 4 attributes that can be selected:
 *  goals, matches, attendance and teams.
 */
function chooseData() {

    // ******* TODO: PART I *******
    //Changed the selected data when a user selects a different
    // menu item from the drop down.

}

/* DATA LOADING */

// This is where execution begins; everything
// above this is just function definitions
// (nothing actually happens)

// Load CSV file
d3.csv("data/fifa-world-cup.csv", function (error, csv) {

    csv.forEach(function (d) {

        // Convert numeric values to 'numbers'
        d.year = +d.YEAR;
        d.teams = +d.TEAMS;
        d.matches = +d.MATCHES;
        d.goals = +d.GOALS;
        d.avg_goals = +d.AVERAGE_GOALS;
        d.attendance = +d.AVERAGE_ATTENDANCE;
        //Lat and Lons of gold and silver medals teams
        d.win_pos = [+d.WIN_LON, +d.WIN_LAT];
        d.ru_pos = [+d.RUP_LON, +d.RUP_LAT];

        //Break up lists into javascript arrays
        d.teams_iso = d3.csvParse(d.TEAM_LIST).columns;
        d.teams_names = d3.csvParse(d.TEAM_NAMES).columns;

    });

    // Store csv data in a global variable
    allWorldCupData = csv;
    // Draw the Bar chart for the first time
    updateBarChart('attendance');
});
