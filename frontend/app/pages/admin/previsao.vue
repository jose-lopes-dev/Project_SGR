<script setup>
definePageMeta({
  middleware: ["auth", "admin"],
  layout: "admin"
})

import LineChart from '~/components/LineChart.vue'

const { getPrevisaoReceita } = useApi()

const chartData = ref({ labels: [], datasets: [] })

const mesesPt = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]
const formatMes = (ym) => {
  const [y, m] = (ym || "").split("-").map(Number)
  if (!y || !m) return ym
  return `${mesesPt[m - 1]} ${y}`
}

onMounted(async () => {
  const dados = await getPrevisaoReceita()
  if (dados && (dados.historico || dados.previsao_proximos_meses)) {
    const histLabels = dados.meses_historico || []
    const prevLabels = dados.meses_previsao || []
    const labels = [...histLabels, ...prevLabels]

    const hist = dados.historico || []
    const prev = dados.previsao_proximos_meses || []

    chartData.value = {
      labels: labels.map(formatMes),
      datasets: [{
        label: "Histórico",
        data: [...hist, ...new Array(prev.length).fill(null)],
        borderColor: "#2563eb",
        backgroundColor: "rgba(37,99,235,0.10)",
        tension: 0.35,
      }, {
        label: "Previsão (regressão linear)",
        data: [...new Array(hist.length).fill(null), ...prev],
        borderColor: "#f97316",
        backgroundColor: "rgba(249,115,22,0.10)",
        borderDash: [6, 6],
        tension: 0.35,
      }]
    }
  }
})
</script>

<template>
<div class="space-y-6">
  <h1 class="text-2xl font-bold mb-6">Previsão Receita (IA)</h1>
  <LineChart v-if="chartData.labels.length" :chartData="chartData"/>
</div>
</template>