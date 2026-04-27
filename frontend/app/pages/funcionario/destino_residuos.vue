<script setup>
import { ref, onMounted } from "vue"
import DataTable from "~/components/DataTable.vue"
import Modal from "~/components/Modal.vue"
import { useApi } from "~/composables/useAPI.js"

definePageMeta({
  layout: "funcionario",
  middleware: ["auth", "funcionario"]
})

const { $swal } = useNuxtApp()
const { getDestinos, createDestino, updateDestino, deleteDestino, getResiduos } = useApi()

const destinos = ref([])
const residuos = ref([])

const showModal = ref(false)
const editando = ref(false)
const destinoEditId = ref(null)

const filtros = ref({
  data_inicio: "",
  data_fim: "",
  tipo_residuo_id: ""
})

const tiposResiduos = ref([])

onMounted(async () => {
  tiposResiduos.value = await useApi().getTiposResiduos()
})

const { public: { apiBase } } = useRuntimeConfig()

const exportarDestinosFiltrados = async (formato="csv") => {
  const paramsObj = { ...filtros.value }

  // Remove campos vazios
  Object.keys(paramsObj).forEach(key => {
    if (paramsObj[key] === "" || paramsObj[key] === null) delete paramsObj[key]
  })

  const params = new URLSearchParams(paramsObj).toString()
  const { public: { apiBase } } = useRuntimeConfig()
  const res = await fetch(`${apiBase}/export/destinos?${params}formato=${formato}`)
  const blob = await res.blob()
  const url = window.URL.createObjectURL(blob)
  const link = document.createElement("a")
  link.href = url
  link.download = `destinos.${formato}`
  document.body.appendChild(link)
  link.click()
  link.remove()
}

const formData = ref({
  residuo_id: null,
  destino: "reutilizacao",
  quantidade: 0,
  receita: 0,
  data: new Date().toISOString().substring(0,10),
  observacoes: ""
})

const headers = [
  "ID",
  "Resíduo",
  "Destino",
  "Quantidade",
  "Receita",
  "Data",
  "Observações",
  "Ações"
]

const fields = [
  "id",
  "residuo_nome",
  "destino",
  "quantidade",
  "receita",
  "data",
  "observacoes",
  "acoes"
]

// Carregar dados
const carregarDados = async () => {
  const listaDestinos = await getDestinos()
  destinos.value = listaDestinos.map(d => ({
    ...d,
    residuo_nome: d.residuo?.tipo_residuo?.nome || "N/A"
  }))

  residuos.value = await getResiduos()
}

onMounted(carregarDados)

// Abrir modal para novo destino
const abrirNovoDestino = () => {
  editando.value = false
  destinoEditId.value = null
  formData.value = {
    residuo_id: null,
    destino: "reutilizacao",
    quantidade: 0,
    receita: 0,
    data: new Date().toISOString().substring(0,10),
    observacoes: ""
  }
  showModal.value = true
}

// Abrir modal para editar destino
const editarDestino = (row) => {
  editando.value = true
  destinoEditId.value = row.id
  formData.value = {
    residuo_id: row.residuo_id,
    destino: row.destino,
    quantidade: row.quantidade,
    receita: row.receita,
    data: row.data,
    observacoes: row.observacoes
  }
  showModal.value = true
}

// Guardar destino (criar ou atualizar)
const guardarDestino = async () => {
  try {
    if(editando.value){
      await updateDestino(destinoEditId.value, formData.value)
      $swal.fire("Atualizado!", "Destino atualizado com sucesso", "success")
    } else {
      await createDestino(formData.value)
      $swal.fire("Sucesso!", "Destino criado com sucesso", "success")
    }

    showModal.value = false
    await carregarDados()
  } catch(err){
    $swal.fire("Erro", "Erro ao guardar destino", "error")
    console.error(err)
  }
}

// Eliminar destino
const eliminarDestino = async (id) => {
  const confirm = await $swal.fire({
    title:"Tem certeza?",
    text:"Este destino será eliminado",
    icon:"warning",
    showCancelButton:true
  })
  if(!confirm.isConfirmed) return

  try{
    await deleteDestino(id)
    $swal.fire("Eliminado!", "Destino removido com sucesso", "success")
    await carregarDados()
  } catch(err){
    $swal.fire("Erro", "Erro ao eliminar", "error")
  }
}
</script>

<template>
<div class="space-y-6">
  <h1 class="text-2xl font-bold">Destinos de Resíduos</h1>

  <button @click="abrirNovoDestino" class="bg-green-600 text-white px-4 py-2 rounded">
    Adicionar
  </button>

   <div class="space-y-4">
  <div class="flex gap-2">
    <input type="date" v-model="filtros.data_inicio" />
    <input type="date" v-model="filtros.data_fim" />
    <select v-model="filtros.tipo_residuo_id">
      <option value="">Todos</option>
      <option v-for="t in tiposResiduos" :key="t.id" :value="t.id">{{ t.nome }}</option>
    </select>
    <button class="bg-blue-600 text-white px-4 py-2 rounded" @click="exportarDestinosFiltrados('csv')">Exportar CSV</button>
    <button class="bg-red-600 text-white px-4 py-2 rounded" @click="exportarDestinosFiltrados('pdf')">Exportar PDF</button>
  </div>
</div>

  <DataTable :headers="headers" :fields="fields" :rows="destinos">
    <template #acoes="{ row }">
      <div class="flex gap-2">
        <button @click="editarDestino(row)" class="bg-yellow-500 text-white px-2 py-1 rounded">
          Editar
        </button>
        <button @click="eliminarDestino(row.id)" class="bg-red-600 text-white px-2 py-1 rounded">
          Eliminar
        </button>
      </div>
    </template>
  </DataTable>

  <Modal v-model:show="showModal" title="Destino de Resíduo">
    <div class="space-y-4">
      <div>
        <label>Resíduo</label>
        <select v-model="formData.residuo_id" class="border rounded p-2 w-full">
          <option v-for="r in residuos" :key="r.id" :value="r.id">
            {{ r.tipo_residuo?.nome || "N/A" }} - {{ r.local?.tipo_local || "N/A" }}
          </option>
        </select>
      </div>

      <div>
        <label>Destino</label>
        <select v-model="formData.destino" class="border rounded p-2 w-full">
          <option value="reutilizacao">Reutilização</option>
          <option value="reciclagem">Reciclagem</option>
          <option value="reabilitacao">Reabilitação</option>
          <option value="aterro">Aterro</option>
        </select>
      </div>

      <div>
        <label>Quantidade</label>
        <input type="number" v-model="formData.quantidade" class="border rounded p-2 w-full"/>
      </div>

      <div>
        <label>Receita</label>
        <input type="number" v-model="formData.receita" class="border rounded p-2 w-full"/>
      </div>

      <div>
        <label>Data</label>
        <input type="date" v-model="formData.data" class="border rounded p-2 w-full"/>
      </div>

      <div>
        <label>Observações</label>
        <textarea v-model="formData.observacoes" class="border rounded p-2 w-full"></textarea>
      </div>

      <div class="flex gap-4">
        <button @click="guardarDestino" class="bg-blue-600 text-white px-4 py-2 rounded">
          Guardar
        </button>
        <button @click="showModal=false" class="bg-gray-500 text-white px-4 py-2 rounded">
          Cancelar
        </button>
      </div>
    </div>
  </Modal>
</div>
</template>