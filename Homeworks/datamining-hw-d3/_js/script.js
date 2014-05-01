/* 
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */


$(document).on("ready", function() {
    init();
});
var filename = "_data/train_purchase.csv";
var entries, chart,
        inputs = {'shopping_pt': 'int', 'record_type': 'int', 'day': 'int', 'time': 'string', 'state': 'string',
            'location': 'string', 'group_size': 'int', 'homeowner': 'bool', 'car_age': 'int', 'car_value': 'string',
            'risk_factor': 'string', 'age_oldest': 'int', 'age_youngest': 'int', 'married_couple': 'bool', 'C_previous': 'string',
            'duration_previous': 'float', 'cost': 'float'},
outputs = {'A': 'string', 'B': 'string', 'C': 'string', 'D': 'string', 'E': 'string', 'F': 'string', 'G': 'string'};
defaults = {key: "married_couple", output: "A"}
function init()
{
    entries = cleanData(readCSV(filename));
    initMenus();
    chart = areaChart();
    refresh();
//    var key1 = "state", key2 = "A";

//    var dataset = prepareDatasets(entries, key1, key2);
//    console.log(dataset);

//    chart.update(dataset, key1, key2);
}
function initMenus() {
    for (var header in inputs)
    {
        var html = "<option value='" + header + "' "
                + ((header === defaults.key) ? "selected" : "") + ">"
                + header + "</option>";
        $("#key1-selector").append(html);
    }
    for (var header in outputs)
    {
        var html = "<option value='" + header + "' "
                + ((header === defaults.output) ? "selected" : "") + ">"
                + header + "</option>";
        $("#output-selector").append(html);
    }

    $("select").on("change", function()
    {
        refresh();
    });
}
function refresh() {
    var key = $("#key1-selector").val(), output = $("#output-selector").val();
    console.log(key + " " + output);
    var dataset = prepareDatasets(entries, key, output);
    chart.update(dataset, key, output);
}
function cleanData(d) {
    for (var i = 0, j = d.length; i < j; i++)
    {
        for (var head in inputs)
        {
            switch (inputs[head])
            {
                case "int":
                    d[i][head] = parseInt(d[i][head]);
                    break;
                case "float":
                    d[i][head] = parseFloat(d[i][head]);
                    break;
                case "bool":
                    d[i][head] = (d[i][head] === "1") ? "Yes" : "No";
                    break;
            }
        }
    }
    return d;
}

function prepareDatasets(data, key, key2)
{
    var nested = d3.nest()
            .key(function(d) {
                return d[key];
            }).sortKeys(d3.ascending)
            .key(function(d) {
                return d[key2];
            }).sortKeys(d3.ascending)
            .rollup(function(leaves) {
                var list = [];
                for (var i = 0, j = leaves.length; i < j; i++)
                {
                    var leaf = leaves[i];
                    list.push(leaf);
                }
                return {'list': list, count: leaves.length};
            })
            .entries(data);
    for (var i = 0, j = nested.length; i < j; i++)
    {
        nested[i]["total"] = d3.sum(nested[i].values, function(d) {
            return d.values.count;
        });
    }
    return nested;
}


areaChart = function() {
    self = {};
    var margin = {top: 20, right: 100, bottom: 30, left: 40},
    width = 960 - margin.left - margin.right,
            height = 500 - margin.top - margin.bottom;
    var x = d3.scale.ordinal()
            .rangeRoundBands([0, width], .1);
    var y = d3.scale.linear()
            .rangeRound([height, 0]);
    var color = d3.scale.ordinal()
            .range(["#98abc5", "#8a89a6", "#7b6888", "#6b486b", "#a05d56", "#d0743c", "#ff8c00"]);
    var xAxis = d3.svg.axis()
            .scale(x)
            .orient("bottom");
    var yAxis = d3.svg.axis()
            .scale(y)
            .orient("left")
            .tickFormat(d3.format(".0%"));
    var svg = d3.select("body").append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
            .append("g")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
    svg.append("g")
            .attr("class", "x axis")
            .attr("transform", "translate(0," + height + ")")
            .call(xAxis);
    svg.append("g")
            .attr("class", "y axis")
            .call(yAxis);
//    svg.append("g").attr("class", "columns")
//d3.csv("data.csv", function(error, data) {
//  color.domain(d3.keys(data[0]).filter(function(key) { return key !== "State"; }));



    self.update = function(data, key1, key2) {

        data.forEach(function(d)
        {
//            console.log(d);
            var y0 = 0;
            var total = d.total;
            d.values.forEach(function(d1) {
//                console.log(d1);
                d1.y0 = y0;
                d1.y1 = y0 += +d1.values.count;
                d1.y0 /= total;
                d1.y1 /= total;
            });
        });
//        data.sort(function(a, b) {
//            return b.ages[0].y1 - a.ages[0].y1;
//        });
        console.log(data);
        x.domain(data.map(function(d) {
            return d.key;
        }));
       
       svg.selectAll(".col-group").remove();
        var vis1 = svg.selectAll(".col-group")
                .data(data)
                .enter().append("g")
                .classed("col-group", true)
//                .classed(key1,true)
                .classed("active-group", function(d,i){
                    console.log(i);
            return true;
        })
                .attr("transform", function(d) {
                    return "translate(" + x(d.key) + ",0)";
                });
//        $(".active-columns").show();

        vis1.selectAll(".column")
                .attr("opacity", 0)
                .data(function(d) {
                    return d.values;
                })
                .enter().append("rect")
                .attr("class", "column")
                .attr("width", x.rangeBand())
                .attr("y", function(d) {
                    return y(d.y1);
                })
                .attr("height", function(d) {
                    return y(d.y0) - y(d.y1);
                })
                .style("fill", function(d) {
                    return color(d.key);
                })
                .attr("opacity", 1)
                .on("mouseover", function(d, i) {
                    d3.select(this).style("opacity", .1);
                })
                .on("mouseout", function(d, i) {
                    d3.select(this).style("opacity", 1);
                });
//        vis1.selectAll(".column").transition().duration(1500)
//                .attr("width", x.rangeBand())
//                .attr("y", function(d) {
//                    return y(d.y1);
//                })
//                .attr("height", function(d) {
//                    return y(d.y0) - y(d.y1);
//                })
        self.updateAxis()
        self.drawLegend(data, key1, key2);
    };
    self.updateAxis = function() {
        svg.select(".x.axis")
                .transition().duration(1000)
                .call(xAxis);
        svg.select(".y.axis")
                .transition().duration(1000)
                .call(yAxis);
    }
    self.drawLegend = function(data, key1, key2)
    {
        svg.selectAll(".legend").remove();
        var legend = svg.selectAll(".legend")
                .data(color.domain().slice().reverse())
                .enter().append("g")
                .attr("class", "legend")
                .attr("transform", function(d, i) {
                    return "translate(0," + i * 20 + ")";
                });
        legend.append("rect")
                .attr("x", width )
                .attr("width", 18)
                .attr("height", 18)
                .style("fill", color);
        legend.append("text")
                .attr("x", width - 6)
                .attr("y", 9)
                .attr("dy", ".35em")
                .style("text-anchor", "end")
                .text(function(d) {
                    console.log(d);
                    return d;
                });
    }
    return self;
}