export function renderTempChart() {
    if (document.getElementById('temperature-chart') && document.getElementById('tooltip-temp')) {
        // Define the dimensions and margins of the chart
        const margin = { top: 20, right: 30, bottom: 40, left: 40 };
        const width = 500 - margin.left - margin.right;
        const height = 200 - margin.top - margin.bottom;

        // Select the tooltip div
        const tooltip = d3.select("#tooltip-temp");

        // Select the SVG container and set up the chart dimensions
        const svg = d3.select("#temperature-chart")
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

        // Load the data from CSV
        d3.csv("/historical_data.csv").then(data => {
            // Parse the data
            data.forEach(d => {
                const parsedDate = d3.timeParse("%Y-%m-%d")(d.date);
                const parsedTime = d3.timeParse("%H:%M")(d.time);
                if (!parsedDate || !parsedTime) {
                    console.log("Invalid date or time:", d.date, d.time);
                } else {
                    d.timestamp = new Date(parsedDate.getTime() + parsedTime.getTime() - parsedTime.setHours(0, 0, 0, 0)); // Combine date and time
                }
                d.Tair = +d.Tair; // Convert Tair to number
            });

            // Group data by date and calculate average Tair and standard deviation (error)
            const dailyAverage = d3.rollup(data,
                v => {
                    const avg = d3.mean(v, d => d.Tair);
                    const error = d3.deviation(v, d => d.Tair); // Calculate standard deviation (error)
                    return { avg, error }; // Return both average and error
                },
                d => d3.timeDay(d.timestamp)); // Group by day, using the timestamp

            const dailyData = Array.from(dailyAverage, ([date, { avg, error }]) => ({ date, avg, error }));

            // Add event listener for the filter option
            d3.select("#filter-option-temp").on("change", () => {
                const filterOption = d3.select("#filter-option-temp").property("value");
                applyFilter(filterOption);
            });

            // Initial chart rendering with default filter
            applyFilter("monthly-temp");

            function applyFilter(filterOption) {
                let filteredData;

                if (filterOption === "monthly-temp") {
                    const latestDate = d3.max(dailyData, d => d.date);
                    const twelveMonthsAgo = d3.timeMonth.offset(latestDate, -12);
                    filteredData = dailyData.filter(d => d.date >= twelveMonthsAgo && d.date <= latestDate);
                } else if (filterOption === "weekly-temp") {
                    const latestDate = d3.max(dailyData, d => d.date);
                    const sevenDaysAgo = d3.timeDay.offset(latestDate, -7);

                    // Filter data for the last 7 days
                    filteredData = dailyData.filter(d => d.date >= sevenDaysAgo && d.date <= latestDate);

                    // Ensure the filtered data is an array and log it for debugging
                    console.log("Filtered Data (Weekly-temp):", filteredData);
                }

                // Ensure filteredData has at least one data point
                if (filteredData.length > 0) {
                    updateChart(filteredData);
                } else {
                    console.log("No data available for the selected filter option.");
                }
            }


            function updateChart(data) {
                // Remove old elements (path, dots, error bars, etc.)
                svg.selectAll(".dot").remove();
                svg.selectAll(".error-bar").remove();
                svg.selectAll(".hover-area").remove();
                svg.selectAll("defs").remove();
                svg.selectAll("path").remove();

                // Determine the time range
                const minDate = d3.min(data, d => d.date);
                const maxDate = d3.max(data, d => d.date);
                const timeRange = maxDate - minDate;

                // Group data based on time range
                let groupedData;

                if (timeRange > 8 * 24 * 60 * 60 * 1000) {
                    // If the time range is large (over 8 days), group by month
                    groupedData = d3.rollup(data,
                        v => {
                            const avg = d3.mean(v, d => d.avg); // Use 'avg' from grouped data, not Tair
                            const error = v.length > 1 ? d3.deviation(v, d => d.error) : 0; // Deviation based on 'error' values
                            return { avg, error };
                        },
                        d => d3.timeMonth(d.date)); // Group by month
                } else {
                    // If the time range is small (e.g., less than 8 days), group by date and calculate avg and error
                    groupedData = d3.rollup(data,
                        v => {
                            const avg = d3.mean(v, d => d.avg); // Use 'avg' from grouped data
                            const error = v.length > 1 ? d3.deviation(v, d => d.error) : 0; // Deviation based on 'error' values
                            return { avg, error };
                        },
                        d => d3.timeDay(d.date)); // Group by day
                }


                // Convert grouped data into an array
                let groupedArray = Array.from(groupedData, ([date, { avg, error }]) => ({ date, avg, error }));

                // Sort the array by date to ensure correct path drawing
                groupedArray.sort((a, b) => a.date - b.date);

                // Update the scales
                x.domain(d3.extent(groupedArray, d => d.date));
                const yMax = d3.max(groupedArray, d => d.avg + (d.error || 0)) || 0; // Fallback to 0 if NaN
                const yMin = d3.min(groupedArray, d => d.avg - (d.error || 0)) || 0; // Fallback to 0 if NaN
                y.domain([yMin - 1.5, yMax + 1.5]);

                // Determine the tick format based on the time range
                let xTicks, xTickFormat;
                if (timeRange > 8 * 24 * 60 * 60 * 1000) {
                    xTicks = d3.timeMonth.every(1);
                    xTickFormat = d3.timeFormat("%b"); // Format: Jan, Feb, Mar, ...
                } else { // Less than 7 days
                    xTicks = d3.timeDay.every(1);
                    xTickFormat = d3.timeFormat("%d"); // Format: dd
                }

                console.log("y-axis data:", groupedArray.map(d => d.avg)); // Logs the average Tair values being passed to y

                // Update the x-axis
                xAxis.transition().duration(500)
                    .call(d3.axisBottom(x).ticks(xTicks).tickFormat(xTickFormat));

                // Update the y-axis
                yAxis.transition().duration(500).call(d3.axisLeft(y)).attr("transform", "translate(-10,0)");

                // Define a color gradient
                const gradient = svg.append("defs")
                    .append("linearGradient")
                    .attr("id", "line-gradient")
                    .attr("x1", "0%")
                    .attr("y1", "0%")
                    .attr("x2", "0%")
                    .attr("y2", "100%");

                gradient.append("stop")
                    .attr("offset", "0%")
                    .attr("stop-color", "#7E00AC") // Top color
                    .attr("stop-opacity", 0.4);

                gradient.append("stop")
                    .attr("offset", "25%")
                    .attr("stop-color", "#ffffff") // Bottom color (transparent)
                    .attr("stop-opacity", 0);

                // Define the area generator (the area under the line chart)
                const area = d3.area()
                    .x(d => x(d.date))
                    .y0(y(0))  // y-axis baseline (0 is the bottom of the chart)
                    .y1(d => y(d.avg))  // Average temperature
                    .defined(d => d.avg !== undefined && !isNaN(d.avg));  // Only include defined values

                // Append the area with the gradient fill
                svg.append("path")
                    .datum(groupedArray)
                    .attr("class", "area")
                    .attr("d", area)
                    .style("fill", "url(#line-gradient)");  // Apply the gradient to the area


                // Append the area path with the gradient fill
                svg.append("path")
                    .datum(groupedArray)
                    .attr("class", "area")
                    .attr("d", area)
                    .style("fill", "url(#line-gradient)");  // Apply the gradient

                // Check if all data for the line is valid before appending path
                if (groupedArray.every(d => !isNaN(d.avg))) {
                    // Add the updated path (with line connecting points)
                    svg.append("path")
                        .datum(groupedArray)
                        .attr("fill", "none")
                        .attr("stroke", "#7E00AC")
                        .attr("stroke-width", 1.5)
                        .attr("d", line);
                } else {
                    console.log("Invalid data for line path");
                }

                // Add data points (dots)
                svg.selectAll(".dot")
                    .data(groupedArray)
                    .enter()
                    .append("circle")
                    .attr("class", "dot")
                    .attr("cx", d => x(d.date))
                    .attr("cy", d => y(d.avg))
                    .attr("r", 4)
                    .style("fill", "#7E00AC")
                    .attr("opacity", d => isNaN(d.avg) ? 0 : 1) // Hide dots if avg is NaN4
                    .style("cursor", "pointer")
                    .on("mouseover", (event, d) => {
                        // Show and style tooltip on hover
                        tooltip.style("display", "block")
                            .style("left", (event.pageX + 10) + "px") // Position tooltip next to cursor
                            .style("top", (event.pageY - 20) + "px")
                            .html(`Date: ${d3.timeFormat("%Y-%m-%d")(d.date)}<br>Temp: ${d.avg.toFixed(2)}°C<br>Error: ±${d.error ? d.error.toFixed(2) : 0}`);
                    })
                    .on("mouseout", () => {
                        // Hide tooltip on mouseout
                        tooltip.style("display", "none");
                    });

                // Increase the hoverable area
                svg.selectAll(".hover-area")
                    .data(groupedArray)
                    .enter()
                    .append("circle")
                    .attr("class", "hover-area")
                    .attr("cx", d => x(d.date))
                    .attr("cy", d => y(d.avg))
                    .attr("r", 10) // Increase the radius for easier hovering
                    .style("fill", "transparent") // Make the circle invisible
                    .style("cursor", "pointer") // Change cursor to pointer
                    .on("mouseover", (event, d) => {
                        // Show tooltip
                        tooltip.style("display", "block")
                            .style("left", (event.pageX + 10) + "px")
                            .style("top", (event.pageY - 20) + "px")
                            .html(`Date: ${d3.timeFormat("%Y-%m-%d")(d.date)}<br>Temp: ${d.avg.toFixed(2)}°C<br>Error: ±${d.error ? d.error.toFixed(2) : 0}`);
                    })
                    .on("mouseout", () => {
                        // Hide tooltip
                        tooltip.style("display", "none");
                    });

                // Add error bars (standard deviation)
                svg.selectAll(".error-bar")
                    .data(groupedArray)
                    .enter()
                    .append("line")
                    .attr("class", "error-bar")
                    .attr("x1", d => x(d.date))
                    .attr("x2", d => x(d.date))
                    .attr("y1", d => y(d.avg + d.error))
                    .attr("y2", d => y(d.avg - d.error))
                    .attr("stroke", "#7E00AC")
                    .attr("stroke-width", 1)
                    .attr("opacity", d => isNaN(d.avg) ? 0 : 1); // Hide error bars if avg is NaN
            }

        });
    }
}