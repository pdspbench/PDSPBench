<template>
  <div>
    <!--<v-container>-->
    <!-- User Selection Card -->
    <v-card class="my-6 pa-0" color="white" elevation="24px">
      <v-card-title>
        <v-sheet color="primary" elevation="24"
          class="justify-center mt-n12 pl-16 pr-16 pt-6 pb-6 rounded  white--text ">
          <h3>Learned Cost Model</h3>
        </v-sheet>
      </v-card-title>
      <v-card-subtitle class="mt-2">
        Select parameters to infer the performance cost using learned cost Model
      </v-card-subtitle>
      <v-card-text>
        <v-row>
          <v-col cols="12" sm="3">
            <v-select :items="uniqueStrategies" label="Enumeration Strategy" v-model="selectedStrategy" return-object
              item-text="name" item-value="name"></v-select>
          </v-col>
          <v-col cols="12" sm="3">
            <v-select :items="uniqueCostModels" label="Learned Cost Models" v-model="selectedLearnedCostModels" return-object
              item-text="name" item-value="name"></v-select>
          </v-col>
          <v-col cols="12" sm="3">
            <v-select :items="uniqueMetrics" label="Metric" v-model="selectedMetric" return-object item-text="name"
              item-value="name"></v-select>
          </v-col>
          <v-col cols="12" sm="3">
            <v-select :items="testQueryTypes" label="Test Query Types" v-model="selectedTestQueryType"
              @change="onTestQueryTypeChange" item-text="name" item-value="value"></v-select>
          </v-col>
          <v-col cols="12" sm="3">
            <v-select :items="uniqueTemplates" label="Parallel Query Plans" v-model="selectedTemplate" return-object
              item-text="name" item-value="name"></v-select>
          </v-col>
        </v-row>
      </v-card-text>
      <v-card-actions>
        <v-btn color="primary" class="ma-4" elevation="3"
          @click="filterAndGeneratePlot"><v-icon>mdi-plus</v-icon>Inference Cost</v-btn>
        <v-btn color="primary" class="ma-4" elevation="3"
          @click="generateComparisonPlot"><v-icon>mdi-compare</v-icon>Compare Costs</v-btn>
      </v-card-actions>
    </v-card>

    <!-- Data Table -->
    <v-card class="my-12 pa-0" color="white" elevation="24px">

      <v-card-title>
        <v-sheet color="primary" elevation="24"
          class="justify-center mt-n12 pl-16 pr-16 pt-6 pb-6 rounded  white--text ">
          <h3>Data Summary</h3>
        </v-sheet>
        <v-spacer></v-spacer>
        <v-btn icon @click="clearTable">
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </v-card-title>

      <v-data-table v-model="selectedQueries" :headers="tableHeaders" :items="tableData" item-key="testTemplateName"
        show-select class="elevation-1" @selection-change="updateSelectedQueries">
      </v-data-table>
    </v-card>

    <!-- Plot Containers and Data Table -->
    <v-row>
      <v-col cols="12" md="12">
        <div ref="plotContainer" class="plot-container"></div>
      </v-col>
    </v-row>
    <!-- Comparison Plot Container -->
    <v-row>
      <v-col cols="12" md="12">
        <div ref="comparisonPlotContainer" class="comparison-plot-container"></div>
      </v-col>
    </v-row>
    <!--</v-container>-->
  </div>
</template>

<script>
import * as d3 from 'd3';

export default {
  name: 'MlDataVis',
  data() {
    return {
      selectedLearnedCostModels: null,
      selectedStrategy: null,
      selectedMetric: null,
      selectedTemplate: null,
      selectedTestQueryType: null,
      uniqueCostModels:[],
      uniqueStrategies: [],
      uniqueMetrics: [],
      uniqueTemplates: [],
      fullData: [],
      tableData: [],
      selectedQueries: [],
      testQueryTypes: [
        { name: "Parallel query plans Unseen", value: "parallelQueryPlansUnseen", file: "unseen_synthetic_query.csv" },
        { name: "Parallel query plans Seen", value: "parallelQueryPlansSeen", file: "seen_synthetic_query.csv" },
        //{ name: "Event rates", value: "eventRates", file: "unseen_event_rate.csv" },
        //{ name: "Tuple Width", value: "tupleWidth", file: "unseen_tuple_width.csv" },
        //{ name: "Window Durations", value: "windowDurations", file: "unseen_window_duration.csv" },
        //{ name: "Window Length", value: "windowLength", file: "unseen_window_length.csv" },
        //{ name: "Parallelism Categories", value: "parallelismCategories", file: "unseen_parallelism_category.csv" },
      ],
      tableHeaders: [
        { text: 'Enumeration Strategy', align: 'start', sortable: false, value: 'enumerationStrategy' },
        { text: 'Learned Cost Models', value: 'learnedCostModels' },
        { text: 'Metric', value: 'evaluationMetric' },
        { text: 'Test Template Name', value: 'testTemplateName' },
        { text: '50th Percentile', value: '50percentile' },
        { text: '95th Percentile', value: '95percentile' },
        { text: '99th Percentile', value: '99percentile' },
      ],
    };
  },
  async mounted() {
    await this.loadAndProcessData();
  },
  methods: {
    async loadAndProcessData(filename = 'unseen_synthetic_query.csv') {
      console.log(`Loading file: ${filename}`);
      try {
        const response = await d3.csv(process.env.BASE_URL + filename);
        console.log('Data loaded:', response);
        this.fullData = response;
        this.updateDropdowns(response);
      } catch (error) {
        console.error('Error loading or processing data:', error);
      }
    },
    updateDropdowns(data) {
      this.uniqueStrategies = [...new Set(data.map(item => item.enumerationStrategy))].map(name => ({ name }));
      this.uniqueCostModels = [...new Set(data.map(item => item.learnedCostModels))].map(name => ({ name }));
      this.uniqueMetrics = [...new Set(data.map(item => item.evaluationMetric))].map(name => ({ name }));
      this.uniqueTemplates = [...new Set(data.map(item => item.testTemplateName))].map(name => ({ name }));
    },
    filterAndGeneratePlot() {
      // Filter data based on the selections
      const filteredData = this.fullData.filter(d =>
        d.enumerationStrategy === this.selectedStrategy.name &&
        d.learnedCostModels === this.selectedLearnedCostModels.name &&
        d.evaluationMetric === this.selectedMetric.name &&
        d.testTemplateName === this.selectedTemplate.name
      );

      // Proceed to generate plot for the filtered data
      if (filteredData.length > 0) {
        this.generatePlots(filteredData);
      } else {
        alert("No data matching the selection.");
      }

    },
    clearPreviousPlots() {
      const container = this.$refs.plotContainer;
      while (container.firstChild) {
        container.removeChild(container.firstChild);
      }
    },

    clearPreviousComparisonPlots() {
      const container = this.$refs.comparisonPlotContainer;
      while (container.firstChild) {
        container.removeChild(container.firstChild);
      }
    },

    clearTable() {
      this.tableData = []; // Clears the table
      this.clearPreviousPlots();
      this.clearPreviousComparisonPlots();
    },

    updateSelectedQueries(selection) {
      this.selectedQueries = selection;
      this.generateComparisonPlot();
    },

    generateComparisonPlot() {
      const selectedData = this.selectedQueries; // Use selectedQueries instead of selectedItems

      if (!selectedData || selectedData.length === 0) {
        alert("Please select one or more items for comparison.");
        return;
      }

      // Assuming you have a dedicated SVG container for the comparison plot.
      // Ensure this container exists in your template.
      const comparisonContainer = this.$refs.comparisonPlotContainer;
      if (!comparisonContainer) {
        console.error("Comparison plot container not found.");
        return;
      }

      d3.select(comparisonContainer).selectAll("*").remove();

      // Setup for the comparison plot (margin, width, height, svg creation)
      const margin = { top: 50, right: 50, bottom: 100, left: 100 },
        width = 600 - margin.left - margin.right,
        height = 600 - margin.top - margin.bottom;

      const svg = d3.select(comparisonContainer).append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform",
          "translate(" + margin.left + "," + margin.top + ")");

      // Assuming data preparation for comparison plot
      const data = selectedData.map(d => ({
        name: d.testTemplateName,
        value: parseFloat(d['50percentile']) // Example: Comparing 50th percentile
      }));

      const x = d3.scaleBand()
        .range([0, width])
        .padding(0.1)
        .domain(data.map(d => d.name));
      const y = d3.scaleLinear()
        .range([height, 0])
        .domain([0, d3.max(data, d => d.value)]);

      //const colors = ['#69b3a2', '#ff8c00', '#6b486b']; // Define colors for the different percentiles
      // Assuming your data is structured for comparison
      // Dynamically generating a color scale
      //const color = d3.scaleSequential(d3.interpolateRainbow).domain([0, selectedData.length - 1]);
      const color = d3.scaleOrdinal(d3.schemeCategory10);

      // Append rectangles for the bar chart
      svg.selectAll(".bar")
        .data(data)
        .enter().append("rect")
        .attr("class", "bar")
        .attr("x", d => x(d.name))
        .attr("width", x.bandwidth())
        .attr("y", d => y(d.value))
        .attr("height", d => height - y(d.value))
        .attr("fill", (d, i) => color(i)); // Use index to assign color;

      // Append X axis
      svg.append("g")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(x))
        .selectAll("text")
        .style("text-anchor", "end")
        .attr("dx", "-.8em")
        .attr("dy", ".15em")
        .attr("transform", "rotate(-45)")
        .style("font-size", "14px");

      // Append Y axis
      svg.append("g")
        .call(d3.axisLeft(y))
        .selectAll("text")
        .style("font-size", "14px"); // Setting font size for y axis ticks;

      // Adding X axis label
      svg.append("text")
        .attr("text-anchor", "end")
        .attr("x", width / 2 + margin.left)
        .attr("y", height + margin.top + 40) // Move the X label down a bit
        .text("Parallel Query Plans")
        .attr("fill", "white")
        .style("font-size", "18px");

      // Adding Y axis label
      svg.append("text")
        .attr("text-anchor", "end")
        .attr("transform", "rotate(-90)")
        .attr("y", -margin.left + 20)
        .attr("x", -margin.top - height / 2 + 100)
        .text("Median Q-error")
        .attr("fill", "white")
        .style("font-size", "18px");
    },

    generatePlots(data) {
      //this.clearPreviousPlots();
      const margin = { top: 40, right: 30, bottom: 90, left: 90 },
        width = 600 - margin.left - margin.right,
        height = 600 - margin.top - margin.bottom;

      const tooltip = d3.select(this.$refs.plotContainer)
        .append("div")
        .style("opacity", 0)
        .attr("class", "tooltip")
        .style("background-color", "white")
        .style("border", "solid")
        .style("border-width", "2px")
        .style("border-radius", "5px")
        .style("padding", "5px")
        .style("position", "absolute")
        .style("z-index", "10")
        .style("visibility", "hidden");


      data.forEach((plotData) => {
        const plotDiv = d3.select(this.$refs.plotContainer)
          .append('div') // Add a div for each plot
          .attr('class', 'plot');

        this.tableData.push({
          enumerationStrategy: plotData.enumerationStrategy,
          learnedCostModels: plotData.learnedCostModels,
          evaluationMetric: plotData.evaluationMetric,
          testTemplateName: plotData.testTemplateName,
          '50percentile': plotData['50percentile'],
          '95percentile': plotData['95percentile'],
          '99percentile': plotData['99percentile'],
        });

        const svg = plotDiv.append("svg")
          .attr("width", '100%') // Make SVG width responsive
          .attr("viewBox", `0 0 ${width + margin.left + margin.right} ${height + margin.top + margin.bottom}`) // Use viewBox for responsiveness
          .append("g")
          .attr("transform", `translate(${margin.left},${margin.top})`);

        const x = d3.scaleBand()
          .range([0, width])
          .domain(["50percentile", "95percentile", "99percentile"])
          .padding(0.1);

        svg.append("g")
          .attr("transform", `translate(0,${height})`)
          .call(d3.axisBottom(x))
          .selectAll("text")
          .style("text-anchor", "middle")
          .attr("dx", "0.5em")
          .attr("dy", "1.25em")
          .attr("transform", "rotate(15))")
          .style("font-size", "14px");

        
        // Find the maximum value across all percentiles to set the y-axis dynamically
        const maxValue = d3.max(data, d => Math.max(d['50percentile'], d['95percentile'], d['99percentile']));


        const y = d3.scaleLinear()
          .domain([1, maxValue])
          .range([height, 0]);

        svg.append("g")
          .call(d3.axisLeft(y))
          .selectAll("text")
          .style("font-size", "14px");

        const percentiles = ["50percentile", "95percentile", "99percentile"];
        const colors = { "50percentile": "#48C9B0", "95percentile": "#AF7AC5", "99percentile": "#C0392B" };

        percentiles.forEach(percentile => {
          svg.append("rect")
            .attr("x", x(percentile))
            .attr("width", x.bandwidth())
            .attr("y", y(plotData[percentile]))
            .attr("height", height - y(plotData[percentile]))
            .attr("fill", colors[percentile])
            .on('mouseover', (event, d) => {
              tooltip.transition().duration(200).style('opacity', 0.9);
              tooltip.html(`${percentile}: ${d[percentile]}`)
                .style('left', (event.pageX) + 'px')
                .style('top', (event.pageY - 28) + 'px');
            })
            .on('mouseout', () => {
              tooltip.transition().duration(500).style('opacity', 0);
            });

          svg.selectAll("rect")
            .on("mouseover", function (event, d) {
              tooltip.style("visibility", "visible")
                .html("Value: " + d[percentile])
                .style("left", (event.pageX + 10) + "px")
                .style("top", (event.pageY + 10) + "px");
            })
            .on("mouseout", function () {
              tooltip.style("visibility", "hidden");
            });

          svg.append("text")
            .attr("x", x(percentile) + x.bandwidth() / 2)
            .attr("y", y(plotData[percentile]) - 5)
            .attr("text-anchor", "middle")
            .attr("fill", "white")
            .style("font-size", "14px")
            .text(plotData[percentile]);

          // Optionally, add x and y axis labels with increased font size
          //svg.append("text")
          //  .attr("text-anchor", "end")
          //  .attr("x", width / 2)
          //  .attr("y", height + margin.top + 25)
          //  .attr("fill", "white")
          //  .text("Percentiles")
          //  .style("font-size", "24px");

          svg.append("text")
            .attr("text-anchor", "end")
            .attr("transform", "rotate(-90)")
            .attr("y", -margin.left + 20)
            .attr("x", -margin.top - height / 2 + 10)
            .attr("fill", "white")
            .text("Q-error")
            .style("font-size", "18px");

          // Add plot title with the test template name
          svg.append("text")
            .attr("x", width / 2)
            .attr("y", -20) // Position above the plot
            .attr("text-anchor", "middle")
            .attr("fill", "white")
            .style("font-size", "18px")
            //.style("font-weight", "bold")
            .text(plotData.testTemplateName); // Use the test template name for the title
        });
      });
    },
    onTestQueryTypeChange() {
      // Assuming selectedTestQueryType is just the value
      console.log("Selected Test Query Type:", this.selectedTestQueryType);
      const selectedType = this.testQueryTypes.find(type => type.value === this.selectedTestQueryType);
      console.log("Selected Type File:", selectedType?.file);
      if (selectedType) {
        this.loadAndProcessData(selectedType.file);
      } else {
        console.error("Selected type or file not found");
      }
    },
  },
};
</script>

<style>
.plot-container {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  background-color: white;
  font-family: sans-serif;
}

.comparison-plot-container {
  flex-basis: calc(25% - 20px);
  /* Adjust based on desired plot size and gap */
  display: flex;
  justify-content: left;
  align-items: left;
  padding: 20px;
  /* This adds padding inside each plot container */
  box-sizing: border-box;
  /* Ensures the padding is included in the width calculation */
  background-color: #ffffff;
  /* Just an example to show the padding effect, can be removed */
  margin: 10px;
  /* Adds margin around each plot container */
  border: 1px solid #ffffff;
  /* Optional, just to show the boundary of the plot container */
}

.plot {
  flex-basis: calc(25% - 20px);
  /* Adjust based on desired plot size and gap */
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
  /* This adds padding inside each plot container */
  box-sizing: border-box;
  /* Ensures the padding is included in the width calculation */
  background-color: #ffffff;
  /* Just an example to show the padding effect, can be removed */
  margin: 10px;
  /* Adds margin around each plot container */
  border: 1px solid #ffffff;
  /* Optional, just to show the boundary of the plot container */
}

.axis-label {
  font-size: 24px !important;
}
</style>