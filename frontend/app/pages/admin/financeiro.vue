<script setup>
definePageMeta({
  middleware: ["auth", "admin"],
  layout: "admin"
})

import BarChart from '~/components/BarChart.vue'
import DashboardCard from '~/components/DashboardCard.vue'
import Dashboard from './dashboard.vue'
import Destino_residuos from '../funcionario/destino_residuos.vue'
import jsPDF from 'jspdf'
import 'jspdf-autotable'
import html2canvas from 'html2canvas'

const financeiro = ref([])

const { getFinanceiroUltimos3Meses, getDashboardKpis, getDashboardResumo } = useApi()

const chartData = ref({ labels: [], datasets: [] })
const receitaMarco = ref(0)
const receitaTotal = ref(0)
const chartContainer = ref(null)

const mesesPt = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]
const formatMes = (ym) => {
  const [y, m] = (ym || "").split("-").map(Number)
  if (!y || !m) return ym
  return `${mesesPt[m - 1]} ${y}`
}

onMounted(async () => {
  const kpisMarco = await getDashboardKpis({ data_inicio: "2026-03-01", data_fim: "2026-03-31" })
  receitaMarco.value = kpisMarco?.receita_total || 0

  financeiro.value = kpisMarco?.financeiro || []

  const resumo = await getDashboardResumo()
  receitaTotal.value = resumo?.receita_total || 0

  const dados = await getFinanceiroUltimos3Meses(2026, 3)
  if (dados && dados.length) {
    chartData.value = {
      labels: dados.map(d => formatMes(d.mes)),
      datasets: [{
        label: "Receita (€) - últimos 3 meses",
        data: dados.map(d => d.receita)
      }]
    }
  }
})

const exportCSV = () => {
  const headers = ["Mês", "Receita (€)"]
  const rows = chartData.value.labels.map((label, i) => [label, chartData.value.datasets[0].data[i]])
  const csvContent = [headers, ...rows].map(e => e.join(";")).join("\n")
  const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" })
  const link = document.createElement("a")
  link.href = URL.createObjectURL(blob)
  link.setAttribute("download", "financeiro.csv")
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)

  console.log(rows)
}

const exportPDF = async () => {
  if (!chartContainer.value) {
    console.error("Gráfico não encontrado")
    return
  }

  try {
    const doc = new jsPDF()
    const title = "Relatório Financeiro - Últimos 3 Meses"
    doc.setFontSize(18)
    doc.text(title, 14, 22)

    const canvas = await html2canvas(chartContainer.value)
    const imgData = canvas.toDataURL("image/png")
    doc.addImage(imgData, "PNG", 15, 30, 180, 100)

    doc.save("relatorio_financeiro.pdf")
  } catch (error) {
    console.error("Erro ao gerar PDF:", error)
  }
}

</script>

<template>
<div>
  <h1 class="text-2xl font-bold mb-6">Financeiro</h1>

  <div class="grid grid-cols-1 md:grid-cols-6 gap-4 mb-6">
    <button @click="exportCSV" class="bg-blue-600 text-white px-4 py-2 rounded mb-4">
      Exportar Dados (CSV)
    </button>  
  
    <button @click="exportPDF" class="bg-green-600 text-white px-4 py-2 rounded mb-4">
      Exportar Dados (PDF)
    </button>
  </div>

  <div class="grid grid-cols-2 gap-4 mb-6">
    <DashboardCard title="Receita (Mar/2026)" :value="receitaMarco" format="currency" />
    <DashboardCard title="Receita total (até ao momento)" :value="receitaTotal" format="currency" />
  </div>

  <div ref="chartContainer">
    <BarChart v-if="chartData.labels.length" :chartData="chartData"/>
  </div>
</div>
</template>