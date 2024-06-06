<template>
  <div>
    <canvas ref="flowchartCanvas"></canvas>
  </div>
</template>

<script>
import { Chart } from 'chart.js/auto';



export default {
  name:'FlowChart',
  mounted() {
    this.renderFlowchart();
  },
  methods: {
    renderFlowchart() {
      const ctx = this.$refs.flowchartCanvas.getContext('2d');
      
      // Define the flowchart data
      const nodes = [
        { id: 'A', label: 'Step 1', x: 100, y: 100 },
        { id: 'B', label: 'Step 2', x: 300, y: 100 },
        { id: 'C', label: 'Step 3', x: 300, y: 300 },
        { id: 'D', label: 'Step 4', x: 100, y: 300 }
      ];
      
      const edges = [
        { from: 'A', to: 'B' },
        { from: 'B', to: 'C' },
        { from: 'C', to: 'D' }
      ];
      
      // Create an array of chart elements
      const chartElements = nodes.map(node => ({
        id: node.id,
        label: node.label,
        x: node.x,
        y: node.y,
        width: 80,
        height: 40
      }));
      
      // Create an array of chart connections
      const chartConnections = edges.map(edge => ({
        from: edge.from,
        to: edge.to
      }));
      
      // Create a new chart instance
      new Chart(ctx, {
        type: 'flowchart',
        data: {
          elements: {
            nodes: chartElements,
            connections: chartConnections
          }
        },
        options: {
          flowchart: {
            displayArrows: true
          },
          layout: {
            hierarchical: {
              enabled: true,
              direction: 'LR'
            }
          }
        }
      });
    }
  }
};
</script>
