export function renderTempChart() {
    // Check if the chart and tooltip elements exist on the page
    if (document.getElementById("temperature-chart") && document.getElementById("tooltip-temp")) {
        // Set the margins and dimensions of the chart
        const margin = { top: 20, right: 30, bottom: 40, left: 40 };
        const width = 500 - margin.left - margin.right;
        const height = 200 - margin.top - margin.bottom;

        // Select tooltip and create SVG for the chart
        const tooltip = d3.select("#tooltip-temp");
        const svg = d3.select("#temperature-chart")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
            .append("g")
            .attr("transform", `translate(${margin.left},${margin.top})`);

        // Create scales for the x and y axes
        const x = d3.scaleTime().range([0, width]);
        const y = d3.scaleLinear().range([height, 0]);

        // Create the axes groups
        const xAxis = svg.append("g").attr("transform", `translate(0,${height})`);
        const yAxis = svg.append("g");

        // Define the line generator function for the line chart
        const line = d3.line().x(d => x(d.date)).y(d => y(d.avg));

        // Define the area generator function for the area chart
        const area = d3.area()
            .x(d => x(d.date))
            .y0(height)
            .y1(d => y(d.avg));

        // Attach a listener to the filter option select element
        d3.select("#filter-option-temp").on("change", function () {
            loadData(this.value);  // Reload data based on the selected filter
        });

        // Parse the date from the format 'dd/mm'
        function parseDate(d) {
            const parts = d.split("/");  // Split the date string by '/'
            const currentYear = new Date().getFullYear();  // Use the current year
            return new Date(currentYear, parseInt(parts[1]) - 1, parseInt(parts[0]));  // Return a new Date object
        }

        // Load the data from the API based on the selected filter option
        function loadData(filterOption) {
            // Define the API URL based on the filter option
            const apiUrl = filterOption === "monthly-temp"
                ? "http://sol1.swin.edu.vn:8016/calculate_monthly_averages/1"
                : "http://sol1.swin.edu.vn:8016/calculate_weekly_averages/1";

            // Fetch data from the API
            fetch(apiUrl)
                .then(response => response.json())
                .then(jsonData => {
                    if (!jsonData || !jsonData.historical_data || !jsonData.predicted_data) {
                        console.error("Invalid API response:", jsonData);
                        return;
                    }

                    // Filter out zero values for avg_temperature and format the data
                    const historicalData = jsonData.historical_data.filter(d => d.avg_temperature > 0).map(d => ({
                        date: filterOption === "monthly-temp"
                            ? new Date(d.year, d.month - 1)  // Use the year and month for monthly data
                            : parseDate(d.date),  // Use parsed date for weekly data
                        avg: d.avg_temperature
                    }));

                    const predictedData = jsonData.predicted_data.filter(d => d.avg_temperature > 0).map(d => ({
                        date: filterOption === "monthly-temp"
                            ? new Date(d.year, d.month - 1)
                            : parseDate(d.date),
                        avg: d.avg_temperature
                    }));

                    updateChart(historicalData, predictedData, filterOption);  // Update the chart with the new data
                })
                .catch(error => console.error("Error fetching API:", error));  // Handle errors
        }

        // Update the chart with new data
        function updateChart(historicalData, predictedData, filterOption) {
            // Remove previous chart elements
            svg.selectAll(".line-temp, .dot-temp, .area-temp").remove();

            // Update the domains of the axes based on the data
            x.domain(d3.extent([...historicalData, ...predictedData], d => d.date));
            y.domain([0, d3.max([...historicalData, ...predictedData], d => d.avg)]);

            // Format ticks based on the filter option
            const tickFormat = filterOption === "monthly-temp" ? d3.timeFormat("%b") : d3.timeFormat("%d/%m");
            const tickValues = filterOption === "weekly-temp" ? historicalData.map(d => d.date) : null;

            // Update the x and y axes
            xAxis.transition().duration(800).call(d3.axisBottom(x).tickFormat(tickFormat).tickValues(tickValues));
            yAxis.transition().duration(800).call(d3.axisLeft(y));

            // Append the area chart for historical data
            svg.append("path")
                .datum(historicalData)
                .attr("class", "area-temp")
                .attr("fill", "rgba(126, 0, 172, 0.3)")
                .attr("d", area);

            // Append the historical data line chart with animation
            const historicalLine = svg.append("path")
                .datum(historicalData)
                .attr("class", "line-temp")
                .attr("fill", "none")
                .attr("stroke", "#7E00AC")
                .attr("stroke-width", 1.5)
                .attr("d", line);

            // Append the predicted data line chart with animation
            const predictedLine = svg.append("path")
                .datum(predictedData)
                .attr("class", "line-temp")
                .attr("fill", "none")
                .attr("stroke", "#88C47A")
                .attr("stroke-width", 1.5)
                .attr("d", line);

            // Animation for the line to appear progressively (right to left)
            const totalLengthHistorical = historicalLine.node().getTotalLength();
            historicalLine
                .attr("stroke-dasharray", totalLengthHistorical)
                .attr("stroke-dashoffset", totalLengthHistorical)
                .transition()
                .duration(800)
                .ease(d3.easeLinear)
                .attr("stroke-dashoffset", 0);

            const totalLengthPredicted = predictedLine.node().getTotalLength();
            predictedLine
                .attr("stroke-dasharray", totalLengthPredicted)
                .attr("stroke-dashoffset", totalLengthPredicted)
                .transition()
                .duration(800)
                .ease(d3.easeLinear)
                .attr("stroke-dashoffset", 0);

            // Create dots for each data point
            const dots = svg.selectAll(".dot-temp")
                .data([...historicalData, ...predictedData])
                .enter().append("circle")
                .attr("class", "dot-temp")
                .attr("cx", d => x(d.date))
                .attr("cy", d => y(d.avg))
                .attr("r", 3)
                .style("fill", d => historicalData.includes(d) ? "#7E00AC" : "#88C47A")
                .style("opacity", 0)  // Start with opacity 0 (invisible)
                .on("mouseover", (event, d) => {
                    // Show tooltip on mouseover
                    const label = historicalData.includes(d) ? "Historical CO₂" : "Predicted CO₂";
                    tooltip.style("display", "block")
                        .style("left", (event.pageX + 10) + "px")
                        .style("top", (event.pageY - 20) + "px")
                        .html(`<strong>${label}</strong><br>${d.avg.toFixed(2)} ppm`);
                })
                .on("mouseout", () => tooltip.style("display", "none"));  // Hide tooltip on mouseout

            // Animate the appearance of dots (sequentially)
            dots.transition()
                .duration(800)
                .delay((d, i) => i * 100)  // Delay each dot's appearance
                .style("opacity", 1);  // Fade in the dots
        }

        // Initial data load (monthly temp data)
        loadData("monthly-temp");
    }
}
