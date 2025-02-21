export function renderCo2Chart() {
    if (document.getElementById("co2-chart") && document.getElementById("tooltip-co2")) {
        // Define the dimensions and margins of the chart
        const margin = { top: 20, right: 30, bottom: 40, left: 40 };
        const width = 500 - margin.left - margin.right;
        const height = 200 - margin.top - margin.bottom;

        // Select the tooltip div
        const tooltip = d3.select("#tooltip-co2");

        // Select the SVG container and set up the chart dimensions
        const svg = d3.select("#co2-chart")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
            .append("g")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

        // Set up the scales for x and y axes
        const x = d3.scaleTime().range([0, width]);
        const y = d3.scaleLinear().range([height, 0]);

        // Set up the axes groups
        const xAxis = svg.append("g")
            .attr("transform", "translate(0," + height + ")");
        const yAxis = svg.append("g");

        // Define the line generator function
        const line = d3.line()
            .x(d => x(d.date))
            .y(d => y(d.avg))
            .defined(d => d.avg !== undefined && !isNaN(d.avg)); // Only include defined values

        // Use API instead of CSV
        d3.json("http://14.225.205.88:8000/calculate_monthly_averages/1").then(apiResponse => {
            // Use the historical_data (you can also use predicted_data if needed)
            const monthlyData = apiResponse.historical_data;

            // Transform each record into an object with a Date object and the average CO2 value.
            // Assuming the date is the first day of the month.
            const processedData = monthlyData.map(d => ({
                date: new Date(d.year, d.month - 1, 1),  // month is 0-indexed in JS Date
                avg: d.avg_co2,
                // If error data is not provided, we set it to 0 (or calculate if available)
                error: 0
            }));

            // Sort the data by date
            processedData.sort((a, b) => a.date - b.date);

            // Add event listener for the filter option (if applicable)
            d3.select("#filter-option-co2").on("change", () => {
                const filterOption = d3.select("#filter-option-co2").property("value");
                applyFilter(filterOption, processedData);
            });

            // Initial chart rendering with default filter ("monthly-co2")
            applyFilter("monthly-co2", processedData);
        });

        function applyFilter(filterOption, data) {
            let filteredData;
            if (filterOption === "monthly-co2") {
                // For monthly data, we use all data
                filteredData = data;
            } else if (filterOption === "weekly-co2") {
                // If you want to simulate weekly, you might aggregate differently.
                // For now, we'll log and use all data.
                console.log("Weekly filter not supported with monthly aggregated data. Showing monthly data.");
                filteredData = data;
            }

            if (filteredData.length > 0) {
                updateChart(filteredData);
            } else {
                console.log("No data available for the selected filter option.");
            }
        }

        function updateChart(data) {
            // Remove old elements (path, dots, error bars, etc.)
            svg.selectAll(".dot-co2").remove();
            svg.selectAll(".error-bar-co2").remove();
            svg.selectAll(".hover-area-co2").remove();
            svg.selectAll("defs").remove();
            svg.selectAll("path").remove();

            // Update the scales
            x.domain(d3.extent(data, d => d.date));
            const yMax = d3.max(data, d => d.avg + (d.error || 0)) || 0;
            const yMin = d3.min(data, d => d.avg - (d.error || 0)) || 0;
            y.domain([yMin - 1.5, yMax + 1.5]);

            // Determine the tick format based on the time range (using the extent of our data)
            const timeRange = x.domain()[1] - x.domain()[0];
            let xTicks, xTickFormat;
            if (timeRange > 8 * 24 * 60 * 60 * 1000) {
                xTicks = d3.timeMonth.every(1);
                xTickFormat = d3.timeFormat("%b"); // Format: Jan, Feb, etc.
            } else {
                xTicks = d3.timeDay.every(1);
                xTickFormat = d3.timeFormat("%d"); // Format: day of month
            }

            // Update the x-axis
            xAxis.transition().duration(500)
                .call(d3.axisBottom(x).ticks(xTicks).tickFormat(xTickFormat));

            // Update the y-axis
            yAxis.transition().duration(500)
                .call(d3.axisLeft(y))
                .attr("transform", "translate(-10,0)");

            // Append a gradient for the area fill
            const gradient = svg.append("defs")
                .append("linearGradient")
                .attr("id", "line-gradient-co2")
                .attr("x1", "0%")
                .attr("y1", "0%")
                .attr("x2", "0%")
                .attr("y2", "100%");

            gradient.append("stop")
                .attr("offset", "0%")
                .attr("stop-color", "#808080")
                .attr("stop-opacity", 0.4);

            gradient.append("stop")
                .attr("offset", "50%")
                .attr("stop-color", "#ffffff")
                .attr("stop-opacity", 0);

            // Define the area generator for the area under the line
            const area = d3.area()
                .x(d => x(d.date))
                .y0(y(0))  // Baseline at y(0)
                .y1(d => y(d.avg))
                .defined(d => d.avg !== undefined && !isNaN(d.avg));

            // Append the area with the gradient fill
            svg.append("path")
                .datum(data)
                .attr("class", "area-co2")
                .attr("d", area)
                .style("fill", "url(#line-gradient-co2)");

            // Check if data is valid for the line
            if (data.every(d => !isNaN(d.avg))) {
                svg.append("path")
                    .datum(data)
                    .attr("fill", "none")
                    .attr("stroke", "#808080")
                    .attr("stroke-width", 1.5)
                    .attr("d", line);
            } else {
                console.log("Invalid data for line path-co2");
            }

            // Add data points (dots)
            svg.selectAll(".dot")
                .data(data)
                .enter()
                .append("circle")
                .attr("class", "dot-co2")
                .attr("cx", d => x(d.date))
                .attr("cy", d => y(d.avg))
                .attr("r", 4)
                .style("fill", "#808080")
                .attr("opacity", d => isNaN(d.avg) ? 0 : 1)
                .style("cursor", "pointer")
                .on("mouseover", (event, d) => {
                    tooltip.style("display", "block")
                        .style("left", (event.pageX + 10) + "px")
                        .style("top", (event.pageY - 20) + "px")
                        .html(`Date: ${d3.timeFormat("%Y-%m-%d")(d.date)}<br>CO2: ${d.avg.toFixed(2)}<br>Error: ±${d.error ? d.error.toFixed(2) : 0}`);
                })
                .on("mouseout", () => {
                    tooltip.style("display", "none");
                });

            // Increase the hoverable area
            svg.selectAll(".hover-area")
                .data(data)
                .enter()
                .append("circle")
                .attr("class", "hover-area-co2")
                .attr("cx", d => x(d.date))
                .attr("cy", d => y(d.avg))
                .attr("r", 10)
                .style("fill", "transparent")
                .style("cursor", "pointer")
                .on("mouseover", (event, d) => {
                    tooltip.style("display", "block")
                        .style("left", (event.pageX + 10) + "px")
                        .style("top", (event.pageY - 20) + "px")
                        .html(`Date: ${d3.timeFormat("%Y-%m-%d")(d.date)}<br>CO2: ${d.avg.toFixed(2)}<br>Error: ±${d.error ? d.error.toFixed(2) : 0}`);
                })
                .on("mouseout", () => {
                    tooltip.style("display", "none");
                });

            // Add error bars if needed (currently error is set to 0)
            svg.selectAll(".error-bar")
                .data(data)
                .enter()
                .append("line")
                .attr("class", "error-bar-co2")
                .attr("x1", d => x(d.date))
                .attr("x2", d => x(d.date))
                .attr("y1", d => y(d.avg + d.error))
                .attr("y2", d => y(d.avg - d.error))
                .attr("stroke", "#808080")
                .attr("stroke-width", 1)
                .attr("opacity", d => isNaN(d.avg) ? 0 : 1);
        }
    }
}
