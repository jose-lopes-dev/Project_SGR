<script setup>
import { Line } from "vue-chartjs"
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  LineElement,
  PointElement,
  CategoryScale,
  LinearScale,
} from "chart.js"

ChartJS.register(Title, Tooltip, Legend, LineElement, PointElement, CategoryScale, LinearScale)

defineProps({
  chartData: {
    type: Object,
    default: () => ({ labels: [], datasets: [] })
  }
})
</script>

<template>
  <div class="bg-white p-4 rounded shadow">
    <Line :data="chartData" />
  </div>
</template>
