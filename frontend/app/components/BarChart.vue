<script setup>
import { Bar } from 'vue-chartjs'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale
} from 'chart.js'

ChartJS.register(
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale
)

// ⬅ garante valor padrão para evitar undefined
const props = defineProps({
  chartData: {
    type: Object,
    default: () => ({ labels: [], datasets: [] })
  }
})
</script>

<template>
<div class="bg-white p-4 rounded shadow">
  <Bar :data="chartData"/>
</div>
</template>