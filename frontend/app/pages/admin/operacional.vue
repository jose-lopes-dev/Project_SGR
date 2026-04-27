<script setup>
definePageMeta({
  middleware: ["auth", "admin"],
  layout: "admin"
})

import BarChart from '~/components/BarChart.vue'
import DataTable from '~/components/DataTable.vue'

const { getOperacionalUltimos3Meses } = useApi()

const chartData = ref({ labels: [], datasets: [] })
const registos = ref([])

const mesesPt = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]
const formatMes = (ym) => {
  const [y, m] = (ym || "").split("-").map(Number)
  if (!y || !m) return ym
  return `${mesesPt[m - 1]} ${y}`
}

const headers = ["ID", "Tipo Resíduo", "Local", "Matéria Prima", "Quantidade", "Data", "Utilizador"]
const fields = ["id", "tipo_nome", "local_nome", "materia_nome", "quantidade", "data", "utilizador_nome"]

onMounted(async () => {
  const res = await getOperacionalUltimos3Meses(2026, 3)

  const series = res?.series || []
  if (series.length) {
    chartData.value = {
      labels: series.map(d => formatMes(d.mes)),
      datasets: [{
        label: "Quantidade de resíduos registados",
        data: series.map(d => d.quantidade)
      }]
    }
  }

  const lista = res?.registos || []
  registos.value = lista.map(r => ({
    ...r,
    tipo_nome: r.tipo_residuo?.nome || "N/A",
    local_nome: r.local?.tipo_local || "N/A",
    materia_nome: r.materia_prima?.nome || "N/A",
    utilizador_nome: r.utilizador?.nome || "N/A",
  }))
})
</script>

<template>
<div>
  <h1 class="text-2xl font-bold mb-6">Operacional</h1>
  <BarChart v-if="chartData.labels.length" :chartData="chartData"/>

  <div class="mt-8">
    <h2 class="text-lg font-semibold mb-3">Registos (últimos 3 meses até Mar/2026)</h2>
    <DataTable :headers="headers" :fields="fields" :rows="registos" />
  </div>
</div>
</template>