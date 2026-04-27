<script setup>
definePageMeta({
  middleware: ["auth", "funcionario"],
  layout: "funcionario"
})

import DashboardCard from '~/components/DashboardCard.vue'
import BarChart from '~/components/BarChart.vue'

const { getResiduos, getDestinos } = useApi()

const resumo = ref({
  total_residuos: 0,
  total_destinos: 0,
  total_reutilizado: 0,
  total_aterro: 0
})

const mesesPt = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]
const labelMes = (y, m) => `${mesesPt[m - 1]} ${y}`

const getYM = (isoDate) => {
  const d = new Date(isoDate)
  return { y: d.getFullYear(), m: d.getMonth() + 1 }
}

const chartData = ref({
  labels: [],
  datasets: []
})

onMounted(async () => {
  const residuos = await getResiduos()
  const destinos = await getDestinos()

  resumo.value.total_residuos = residuos.reduce((acc, r) => acc + Number(r.quantidade || 0), 0)
  resumo.value.total_destinos = destinos.reduce((acc, d) => acc + Number(d.quantidade || 0), 0)

  resumo.value.total_reutilizado = destinos
    .filter(d => (d.destino || "").toLowerCase() !== "aterro")
    .reduce((acc, d) => acc + Number(d.quantidade || 0), 0)

  resumo.value.total_aterro = destinos
    .filter(d => (d.destino || "").toLowerCase() === "aterro")
    .reduce((acc, d) => acc + Number(d.quantidade || 0), 0)

  // Últimos 3 meses fixos até Mar/2026: Jan, Fev, Mar 2026
  const meses = [
    { y: 2026, m: 1 },
    { y: 2026, m: 2 },
    { y: 2026, m: 3 },
  ]

  const porMes = new Map(meses.map(x => [`${x.y}-${String(x.m).padStart(2, "0")}`, 0]))
  for (const r of residuos) {
    const { y, m } = getYM(r.data)
    const key = `${y}-${String(m).padStart(2, "0")}`
    if (porMes.has(key)) porMes.set(key, porMes.get(key) + Number(r.quantidade || 0))
  }

  chartData.value = {
    labels: meses.map(x => labelMes(x.y, x.m)),
    datasets: [{
      label: "Resíduos registados (ton)",
      data: meses.map(x => porMes.get(`${x.y}-${String(x.m).padStart(2, "0")}`) || 0),
      backgroundColor: "#3B82F6"
    }]
  }
})
</script>

<template>
<div class="space-y-6">

  <h1 class="text-2xl font-bold">
    Dashboard Funcionário
  </h1>

  <div class="grid grid-cols-4 gap-4">
    <DashboardCard title="Total Resíduos" :value="resumo.total_residuos"/>
    <DashboardCard title="Total Destinos" :value="resumo.total_destinos"/>
    <DashboardCard title="Reutilizado" :value="resumo.total_reutilizado"/>
    <DashboardCard title="Aterro" :value="resumo.total_aterro"/>
  </div>

  <BarChart v-if="chartData.labels.length" :chartData="chartData"/>

</div>
</template>