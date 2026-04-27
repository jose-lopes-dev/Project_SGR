<script setup>
definePageMeta({
  middleware: ["auth", "admin"],
  layout: "admin"
})

import DashboardCard from '~/components/DashboardCard.vue'
import BarChart from '~/components/BarChart.vue'

const { getDashboardKpis, getReceitaUltimos3Meses } = useApi()

const resumo = ref({})
const chartData = ref({
  labels: [],       // ⬅ inicializa vazio
  datasets: []      // ⬅ inicializa vazio
})

const mesesPt = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]
const formatMes = (ym) => {
  const [y, m] = (ym || "").split("-").map(Number)
  if (!y || !m) return ym
  return `${mesesPt[m - 1]} ${y}`
}

onMounted(async () => {
  // KPIs filtrados para março/2026
  resumo.value = await getDashboardKpis({
    data_inicio: "2026-03-01",
    data_fim: "2026-03-31"
  })

  const dados = await getReceitaUltimos3Meses(2026, 3)

  // ⬅ só atualiza quando dados existirem
  if (dados && dados.length) {
    chartData.value = {
      labels: dados.map(d => formatMes(d.mes)),
      datasets: [
        {
          label: "Receita (€)",
          data: dados.map(d => d.receita)
        }
      ]
    }
  }
})
</script>

<template>
<div class="space-y-6">
  <h1 class="text-2xl font-bold">Dashboard</h1>

  <div class="grid grid-cols-4 gap-4">
    <DashboardCard title="Total Resíduos (Mar/2026)" :value="resumo.total_residuos"/>
    <DashboardCard title="Receita (Mar/2026)" :value="resumo.receita_total" format="currency"/>
    <DashboardCard title="Reutilizado (Mar/2026)" :value="resumo.total_reutilizado"/>
    <DashboardCard title="Aterro (Mar/2026)" :value="resumo.total_aterro"/>
  </div>

  <!-- ⬅ renderiza BarChart apenas se chartData tiver labels -->
  <BarChart v-if="chartData.labels.length" :chartData="chartData"/>
</div>
</template>