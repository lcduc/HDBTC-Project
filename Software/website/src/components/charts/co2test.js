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

        // Define the line generator function for historical data
        const lineHistorical = d3.line()
            .x(d => x(d.date))
            .y(d => y(d.avg))
            .defined(d => d.avg !== undefined && !isNaN(d.avg));

        // Define the line generator function for predicted data (assuming same structure)
        const linePredicted = d3.line()
            .x(d => x(d.date))
            .y(d => y(d.avg))
            .defined(d => d.avg !== undefined && !isNaN(d.avg));

        // Load both CSV files using Promise.all
        Promise.all([
            d3.csv("/historical_data.csv"),
            d3.csv("/predicted_data.csv")
        ]).then(([historicalData, predictedData]) => {
            // Function to parse data (for both datasets)
            function parseData(data) {
                return data.map(d => {
                    const parsedDate = d3.timeParse("%Y-%m-%d")(d.date);
                    const parsedTime = d3.timeParse("%H:%M")(d.time);
                    if (!parsedDate || !parsedTime) {
                        console.log("Invalid date or time:", d.date, d.time);
                        return null;
                    }
                    // Combine date and time
                    d.timestamp = new Date(
                        parsedDate.getTime() +
                        parsedTime.getTime() -
                        parsedTime.setHours(0, 0, 0, 0)
                    );
                    d.CO2air = +d.CO2air; // Convert CO2air to number
                    if (isNaN(d.CO2air)) {
                        console.log("Invalid CO2air value:", d.CO2air);
                        return null;
                    }
                    return d;
                })
                    .filter(d => d !== null);
            }

            historicalData = parseData(historicalData);
            predictedData = parseData(predictedData);

            // Process historical data: Group by day and calculate daily average and error.
            const dailyAverageHistorical = d3.rollup(historicalData,
                v => {
                    const avg = d3.mean(v, d => d.CO2air);
                    const error = d3.deviation(v, d => d.CO2air); // Calculate standard deviation (error)
                    return { avg, error }; // Return both average and error
                },
                d => d3.timeDay(d.timestamp)
            ); // Group by day, using the timestamp
            const dailyHistorical = Array.from(dailyAverageHistorical, ([date, { avg, error }]) => ({ date, avg, error }));

            // Process predicted data similarly, but here we assume no error bars.
            const dailyAveragePredicted = d3.rollup(predictedData,
                v => {
                    const avg = d3.mean(v, d => d.CO2air);
                    return { avg };
                },
                d => d3.timeDay(d.timestamp)
            );
            const dailyPredicted = Array.from(dailyAveragePredicted, ([date, { avg }]) => ({ date, avg }));

            // Merge or update the filter if you need to filter both datasets by time.
            // For simplicity, we'll assume that the filter applies to both datasets.
            // (You can adjust this logic as needed.)
            function applyFilter(filterOption) {
                let filteredHistorical, filteredPredicted;
                if (filterOption === "monthly-co2") {
                    const latestHistorical = d3.max(dailyHistorical, d => d.date);
                    const twelveMonthsAgo = d3.timeMonth.offset(latestHistorical, -12);
                    filteredHistorical = dailyHistorical.filter(d => d.date >= twelveMonthsAgo && d.date <= latestHistorical);
                    filteredPredicted = dailyPredicted.filter(d => d.date >= twelveMonthsAgo && d.date <= latestHistorical);
                } else if (filterOption === "weekly-co2") {
                    const latestHistorical = d3.max(dailyHistorical, d => d.date);
                    const sevenDaysAgo = d3.timeDay.offset(latestHistorical, -7);

                    // Filter data for the last 7 days
                    filteredHistorical = dailyHistorical.filter(d => d.date >= sevenDaysAgo && d.date <= latestHistorical);
                    filteredPredicted = dailyPredicted.filter(d => d.date >= sevenDaysAgo && d.date <= latestHistorical);
                }

                // Ensure filtered data has at least one data point

                if (filteredHistorical.length > 0) {
                    updateChart(filteredHistorical, filteredPredicted);
                } else {
                    console.log("No data available for the selected filter option.");
                }
            }

            d3.select("#filter-option-co2").on("change", () => {
                const filterOption = d3.select("#filter-option-co2").property("value");
                applyFilter(filterOption);
            });
            // Initial chart rendering with default filter
            applyFilter("monthly-co2");

            function updateChart(historical, predicted) {
                // Remove old elements
                svg.selectAll(".dot-co2").remove();
                svg.selectAll(".dot-predicted").remove();
                svg.selectAll(".error-bar-co2").remove();
                svg.selectAll(".hover-area-co2").remove();
                svg.selectAll(".hover-area-predicted").remove();
                svg.selectAll("defs").remove();
                svg.selectAll("path").remove();

                // Combine both datasets for the scales (if they share the same x and y)
                const combinedDates = historical.map(d => d.date).concat(predicted.map(d => d.date));
                const xExtent = d3.extent(combinedDates);
                x.domain(xExtent);

                // For y scale, consider historical (with error) and predicted (avg only)
                const yMaxHist = d3.max(historical, d => d.avg + (d.error || 0));
                const yMinHist = d3.min(historical, d => d.avg - (d.error || 0));
                const yMaxPred = d3.max(predicted, d => d.avg);
                const yMinPred = d3.min(predicted, d => d.avg);
                const yMax = Math.max(yMaxHist || 0, yMaxPred || 0);
                const yMin = Math.min(yMinHist || 0, yMinPred || 0);
                y.domain([yMin - 1.5, yMax + 1.5]);

                // Determine tick format based on time range
                const timeRange = xExtent[1] - xExtent[0];
                let xTicks, xTickFormat;
                if (timeRange > 8 * 24 * 60 * 60 * 1000) {
                    xTicks = d3.timeMonth.every(1);
                    xTickFormat = d3.timeFormat("%b"); // Format: Jan, Feb, Mar, ...
                } else { // Less than 7 days
                    xTicks = d3.timeDay.every(1);
                    xTickFormat = d3.timeFormat("%d"); // Format: dd
                }

                // Update axes
                xAxis.transition().duration(500)
                    .call(d3.axisBottom(x).ticks(xTicks).tickFormat(xTickFormat));
                yAxis.transition().duration(500)
                    .call(d3.axisLeft(y))
                    .attr("transform", "translate(-10,0)");

                // Draw historical area and line (with error bars)
                // Gradient for historical area

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
                    .attr("offset", "4%")
                    .attr("stop-color", "#ffffff")
                    .attr("stop-opacity", 0);

                // Define the area generator for historical data (the area under the line chart)
                const area = d3.area()
                    .x(d => x(d.date))
                    .y0(y(0))  // y-axis baseline (0 is the bottom of the chart)
                    .y1(d => y(d.avg))  // Average temperature
                    .defined(d => d.avg !== undefined && !isNaN(d.avg));  // Only include defined values

                // Append historical area with the gradient fill
                svg.append("path")
                    .datum(historical)
                    .attr("class", "area-co2")
                    .attr("d", area)
                    .style("fill", "url(#line-gradient-co2)");  // Apply the gradient to the area

                // Append historical line with the gradient fill
                svg.append("path")
                    .datum(historical)
                    .attr("class", "area-co2")
                    .attr("d", area)
                    .style("fill", "url(#line-gradient-co2)");  // Apply the gradient

                // Check if all data for the line is valid before appending path-co2
                if (historical.every(d => !isNaN(d.avg))) {
                    // Add the updated path-co2 (with line connecting points)
                    svg.append("path")
                        .datum(historical)
                        .attr("fill", "none")
                        .attr("stroke", "#808080")
                        .attr("stroke-width", 1.5)
                        .attr("d", lineHistorical);
                } else {
                    console.log("Invalid data for historical line.");
                }

                // Append historical data points (dots)
                svg.selectAll(".dot-co2")
                    .data(historical)
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
                            .html(`Date: ${d3.timeFormat("%Y-%m-%d")(d.date)}<br>CO₂: ${d.avg.toFixed(2)}<br>Error: ±${d.error ? d.error.toFixed(2) : 0}`);
                    })
                    .on("mouseout", () => {
                        // Hide tooltip
                        tooltip.style("display", "none");
                    });

                // Append error bars for historical data (standard deviation)
                svg.selectAll(".error-bar-co2")
                    .data(historical)
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

                // Increase hover area for historical dots (if desired)
                svg.selectAll(".hover-area-co2")
                    .data(historical)
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
                            .html(`Date: ${d3.timeFormat("%Y-%m-%d")(d.date)}<br>CO₂: ${d.avg.toFixed(2)}<br>Error: ±${d.error ? d.error.toFixed(2) : 0}`);
                    })
                    .on("mouseout", () => {
                        tooltip.style("display", "none");
                    });

                // ------------------------------
                // Now add the predicted data line (without error bars)
                // Append predicted line
                if (predicted.every(d => !isNaN(d.avg))) {
                    svg.append("path")
                        .datum(predicted)
                        .attr("fill", "none")
                        .attr("stroke", "#FF5733")  // Different color for predicted data
                        .attr("stroke-width", 1.5)
                        .attr("stroke-dasharray", "5,5")  // Dashed line style to differentiate
                        .attr("d", linePredicted);
                } else {
                    console.log("Invalid data for predicted line.");
                }

                // Append predicted data points (dots)
                svg.selectAll(".dot-predicted")
                    .data(predicted)
                    .enter()
                    .append("circle")
                    .attr("class", "dot-predicted")
                    .attr("cx", d => x(d.date))
                    .attr("cy", d => y(d.avg))
                    .attr("r", 4)
                    .style("fill", "#FF5733")
                    .attr("opacity", d => isNaN(d.avg) ? 0 : 1)
                    .style("cursor", "pointer")
                    .on("mouseover", (event, d) => {
                        tooltip.style("display", "block")
                            .style("left", (event.pageX + 10) + "px")
                            .style("top", (event.pageY - 20) + "px")
                            .html(`Date: ${d3.timeFormat("%Y-%m-%d")(d.date)}<br>Predicted CO₂: ${d.avg.toFixed(2)}`);
                    })
                    .on("mouseout", () => {
                        tooltip.style("display", "none");
                    });

                // Increase hover area for predicted dots (if desired)
                svg.selectAll(".hover-area-predicted")
                    .data(predicted)
                    .enter()
                    .append("circle")
                    .attr("class", "hover-area-predicted")
                    .attr("cx", d => x(d.date))
                    .attr("cy", d => y(d.avg))
                    .attr("r", 10)
                    .style("fill", "transparent")
                    .style("cursor", "pointer")
                    .on("mouseover", (event, d) => {
                        tooltip.style("display", "block")
                            .style("left", (event.pageX + 10) + "px")
                            .style("top", (event.pageY - 20) + "px")
                            .html(`Date: ${d3.timeFormat("%Y-%m-%d")(d.date)}<br>Predicted CO₂: ${d.avg.toFixed(2)}`);
                    })
                    .on("mouseout", () => {
                        tooltip.style("display", "none");
                    });
            }
        });
    }
}
