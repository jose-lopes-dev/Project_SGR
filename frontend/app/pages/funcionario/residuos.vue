<script setup>
import { ref, onMounted } from "vue";
import DataTable from "~/components/DataTable.vue";
import Modal from "~/components/Modal.vue";
import { useApi } from "~/composables/useAPI.js";

definePageMeta({
  layout: "funcionario",
  middleware: ["auth", "funcionario"]
});

const { $swal } = useNuxtApp();

const {
  getResiduos,
  createResiduo,
  updateResiduo,
  deleteResiduo,
  getTiposResiduos,
  getLocalizacoes,
  getMateriasPrimas
} = useApi();

const residuos = ref([]);
const tipos = ref([]);
const locais = ref([]);
const materias = ref([]);

const showModal = ref(false);
const editando = ref(false);
const residuoEditId = ref(null);

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

const exportarResiduosFiltrados = async (formato="csv") => {
  const paramsObj = { ...filtros.value }

  // Remove campos vazios
  Object.keys(paramsObj).forEach(key => {
    if (paramsObj[key] === "" || paramsObj[key] === null) delete paramsObj[key]
  })

  const params = new URLSearchParams(paramsObj).toString()
  const { public: { apiBase } } = useRuntimeConfig()
  const res = await fetch(`${apiBase}/export/residuos?${params}formato=${formato}`)
  const blob = await res.blob()
  const url = window.URL.createObjectURL(blob)
  const link = document.createElement("a")
  link.href = url
  link.download = `residuos.${formato}`
  document.body.appendChild(link)
  link.click()
  link.remove()
}

// Dados do formulário
const formData = ref({
  local_id: null,
  tipo_residuo_id: null,
  materia_prima_id: null,
  quantidade: 0,
  data: new Date().toISOString().substring(0, 10),
});

// Cabeçalhos da tabela
const headers = [
  "ID",
  "Tipo Resíduo",
  "Local",
  "Matéria Prima",
  "Quantidade",
  "Data",
  "Utilizador",
  "Ações"
];

const fields = [
  "id",
  "tipo_nome",
  "local_nome",
  "materia_nome",
  "quantidade",
  "data",
  "utilizador_nome",
  "acoes"
];

// Carregar todos os dados necessários
const carregarDados = async () => {
  const dados = await getResiduos();
  residuos.value = dados.map(r => ({
    ...r,
    tipo_nome: r.tipo_residuo?.nome || "N/A",
    local_nome: r.local?.tipo_local || "N/A",
    materia_nome: r.materia_prima?.nome || "N/A",
    utilizador_nome: r.utilizador?.nome || "N/A",
    tipo_residuo_id: r.tipo_residuo?.id,
    local_id: r.local?.id,
    materia_prima_id: r.materia_prima?.id
  }));

  tipos.value = await getTiposResiduos();
  locais.value = await getLocalizacoes();
  materias.value = await getMateriasPrimas();
};

onMounted(carregarDados);

// Abrir modal para criar novo resíduo
const abrirNovoResiduo = () => {
  editando.value = false;
  residuoEditId.value = null;

  formData.value = {
    local_id: null,
    tipo_residuo_id: null,
    materia_prima_id: null,
    quantidade: 0,
    data: new Date().toISOString().substring(0,10),
  };

  showModal.value = true;
};

// Abrir modal para editar resíduo existente
const editarResiduo = (row) => {
  editando.value = true;
  residuoEditId.value = row.id;

  formData.value = {
    local_id: row.local_id,
    tipo_residuo_id: row.tipo_residuo_id,
    materia_prima_id: row.materia_prima_id,
    quantidade: row.quantidade,
    data: row.data,
  };

  showModal.value = true;
};

// Guardar resíduo (criar ou atualizar)
const guardarResiduo = async () => {
  try {
    if(editando.value){
      await updateResiduo(residuoEditId.value, formData.value);
      $swal.fire("Atualizado!", "Resíduo atualizado com sucesso", "success");
    } else {
      await createResiduo(formData.value);
      $swal.fire("Sucesso!", "Resíduo criado com sucesso", "success");
    }

    showModal.value = false;
    await carregarDados();
  } catch(err){
    $swal.fire("Erro", "Erro ao guardar resíduo", "error");
    console.error(err);
  }
};

// Eliminar resíduo
const eliminarResiduo = async (id) => {
  const confirm = await $swal.fire({
    title: "Tem certeza?",
    text: "Este resíduo será eliminado",
    icon: "warning",
    showCancelButton: true
  });

  if(!confirm.isConfirmed) return;

  try {
    await deleteResiduo(id);
    $swal.fire("Eliminado!", "Resíduo removido com sucesso", "success");
    await carregarDados();
  } catch(err){
    $swal.fire("Erro", "Erro ao eliminar", "error");
    console.error(err);
  }
};
</script>

<template>
<div class="space-y-6">
  <h1 class="text-2xl font-bold">Resíduos</h1>

  <button
    @click="abrirNovoResiduo"
    class="bg-green-600 text-white px-4 py-2 rounded"
  >
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
    <button class="bg-blue-600 text-white px-4 py-2 rounded" @click="exportarResiduosFiltrados('csv')">Exportar CSV</button>
    <button class="bg-red-600 text-white px-4 py-2 rounded" @click="exportarResiduosFiltrados('pdf')">Exportar PDF</button>
  </div>
</div>

  <DataTable
    :headers="headers"
    :fields="fields"
    :rows="residuos"
  >
    <template #acoes="{ row }">
      <div class="flex gap-2">
        <button
          @click="editarResiduo(row)"
          class="bg-yellow-500 text-white px-2 py-1 rounded"
        >
          Editar
        </button>
        <button
          @click="eliminarResiduo(row.id)"
          class="bg-red-600 text-white px-2 py-1 rounded"
        >
          Eliminar
        </button>
      </div>
    </template>
  </DataTable>

  <Modal v-model:show="showModal" title="Resíduo">
    <div class="space-y-4">

      <div>
        <label>Tipo de Resíduo</label>
        <select v-model="formData.tipo_residuo_id" class="border rounded p-2 w-full">
          <option v-for="t in tipos" :key="t.id" :value="t.id">
            {{ t.nome }}
          </option>
        </select>
      </div>

      <div>
        <label>Local</label>
        <select v-model="formData.local_id" class="border rounded p-2 w-full">
          <option v-for="l in locais" :key="l.id" :value="l.id">
            {{ l.tipo_local }}
          </option>
        </select>
      </div>

      <div>
        <label>Matéria Prima</label>
        <select v-model="formData.materia_prima_id" class="border rounded p-2 w-full">
          <option v-for="m in materias" :key="m.id" :value="m.id">
            {{ m.nome }}
          </option>
        </select>
      </div>

      <div>
        <label>Quantidade</label>
        <input type="number" v-model="formData.quantidade" class="border rounded p-2 w-full"/>
      </div>

      <div>
        <label>Data</label>
        <input type="date" v-model="formData.data" class="border rounded p-2 w-full"/>
      </div>

      <div class="flex gap-4">
        <button @click="guardarResiduo" class="bg-blue-600 text-white px-4 py-2 rounded">
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

