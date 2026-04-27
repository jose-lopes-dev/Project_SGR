<script setup>
definePageMeta({
  middleware: ["auth", "admin"],
  layout: "admin"
})

import LineChart from "~/components/LineChart.vue"

const { getDashboardAmbiental, getAmbientalUltimos3Meses } = useApi()

// Inicializa dados como objeto vazio
const dados = ref({})
const chartData = ref({ labels: [], datasets: [] })

const mesesPt = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]
const formatMes = (ym) => {
  const [y, m] = (ym || "").split("-").map(Number)
  if (!y || !m) return ym
  return `${mesesPt[m - 1]} ${y}`
}

onMounted(async () => {
  const res = await getDashboardAmbiental()
  dados.value = res || {}  // evita undefined

  const ultimos = await getAmbientalUltimos3Meses(2026, 3)
  const series = ultimos?.series || []
  if (series.length) {
    chartData.value = {
      labels: series.map(s => formatMes(s.mes)),
      datasets: [
        {
          label: "CO₂ evitado (ton)",
          data: series.map(s => s.co2_evitar_estimado),
          borderColor: "#0ea5e9",
          backgroundColor: "rgba(14,165,233,0.15)",
          tension: 0.35,
        },
        {
          label: "Resíduos reutilizados (ton)",
          data: series.map(s => s.reutilizado),
          borderColor: "#22c55e",
          backgroundColor: "rgba(34,197,94,0.15)",
          tension: 0.35,
        }
      ]
    }
  }
})
</script>

<template>
<div class="space-y-6">
  <h1 class="text-2xl font-bold">Impacto Ambiental</h1>

  <div class="grid grid-cols-2 gap-6">
    <div class="bg-white p-6 rounded shadow">
      <h2 class="text-lg font-semibold">Resíduos Reutilizados</h2>
      <p class="text-3xl font-bold mt-4">
        {{ dados.quantidade_reutilizada ?? 0 }} ton
      </p>
    </div>

    <div class="bg-white p-6 rounded shadow">
      <h2 class="text-lg font-semibold">CO₂ Evitado</h2>
      <p class="text-3xl font-bold mt-4">
        {{ dados.co2_evitar_estimado ?? 0 }} ton
      </p>
    </div>
  </div>

  <div>
    <h2 class="text-lg font-semibold mb-3">Últimos 3 meses (até Mar/2026)</h2>
    <LineChart v-if="chartData.labels.length" :chartData="chartData" />
  </div>
</div>
</template>