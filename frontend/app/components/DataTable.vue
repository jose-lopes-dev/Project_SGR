<template>

<div class="bg-white rounded-xl shadow p-6 space-y-4">

<!-- Pesquisa e Exportação -->

<div class="flex justify-between items-center flex-wrap gap-3">

<input
v-model="search"
type="text"
placeholder="Pesquisar..."
class="border rounded px-3 py-2 text-sm w-64"
/>

</div>


<!--  Tabela -->

<table id="datatable" class="w-full border-collapse">

<thead>

<tr class="border-b bg-gray-50">

<th
v-for="(header,index) in headers"
:key="header"
class="py-2 px-3 cursor-pointer"
@click="sortColumn(fields[index])"
>

<div class="flex items-center gap-2">

{{ header }}

<span v-if="sortField === fields[index]">

<span v-if="sortDirection === 'asc'"></span>
<span v-else></span>

</span>

</div>

</th>

</tr>


<!-- filtros por coluna -->

<tr class="border-b bg-gray-50">

<th
v-for="field in fields"
:key="field"
class="px-2 py-1"
>

<input
v-if="field !== 'acoes'"
v-model="columnFilters[field]"
placeholder="filtrar"
class="border rounded px-2 py-1 text-xs w-full"
/>

</th>

</tr>

</thead>


<tbody>

<tr
v-for="row in paginatedRows"
:key="row.id"
class="border-b hover:bg-gray-50"
>

<td
v-for="field in fields"
:key="field"
class="py-2 px-3"
>

<template v-if="field === 'acoes'">

<slot name="acoes" :row="row"></slot>

</template>

<template v-else>

{{ row[field] }}

</template>

</td>

</tr>

<tr v-if="paginatedRows.length === 0">

<td :colspan="fields.length" class="text-center py-6 text-gray-500">

Nenhum resultado encontrado

</td>

</tr>

</tbody>

</table>


<!-- Paginação -->

<div v-if="filteredRows.length" class="flex items-center justify-between">

<div class="text-sm text-gray-600">

{{ startItem }} - {{ endItem }} de {{ filteredRows.length }}

</div>

<div class="flex items-center gap-3">

<select v-model.number="pageSize" class="border rounded px-2 py-1 text-sm">

<option v-for="n in pageSizeOptions" :key="n" :value="n">
{{ n }}/página
</option>

</select>

<button
:disabled="page<=1"
@click="page--"
class="border px-3 py-1 rounded text-sm"
>

Anterior

</button>

<div class="text-sm">

{{ page }} / {{ totalPages }}

</div>

<button
:disabled="page>=totalPages"
@click="page++"
class="border px-3 py-1 rounded text-sm"
>

Seguinte

</button>

</div>

</div>

</div>

</template>


<script setup>

import { ref, computed, watch } from "vue"
import jsPDF from "jspdf"
import html2canvas from "html2canvas"

const props = defineProps({

headers:Array,
fields:Array,

rows:{
type:Array,
default:()=>[]
},

pageSizeOptions:{
type:Array,
default:()=>[5,10,20,50]
},

defaultPageSize:{
type:Number,
default:10
}

})

const search = ref("")

const page = ref(1)

const pageSize = ref(props.defaultPageSize)

const sortField = ref(null)

const sortDirection = ref("asc")

const columnFilters = ref({})

props.fields.forEach(f=>{
columnFilters.value[f]=""
})

watch(
() => [props.rows, search.value, pageSize.value],
() => page.value=1
)


// FILTROS

const filteredRows = computed(()=>{

return props.rows.filter(row=>{

const globalMatch = Object.values(row)
.some(val =>
String(val).toLowerCase().includes(search.value.toLowerCase())
)

const columnMatch = Object.keys(columnFilters.value)
.every(field=>{

if(!columnFilters.value[field]) return true

return String(row[field] ?? "")
.toLowerCase()
.includes(columnFilters.value[field].toLowerCase())

})

return globalMatch && columnMatch

})

})


// ORDENAÇÃO

const sortedRows = computed(()=>{

if(!sortField.value) return filteredRows.value

return [...filteredRows.value].sort((a,b)=>{

const A = a[sortField.value]
const B = b[sortField.value]

if(A<B) return sortDirection.value==="asc"?-1:1
if(A>B) return sortDirection.value==="asc"?1:-1

return 0

})

})

const sortColumn = field=>{

if(field==="acoes") return

if(sortField.value===field){

sortDirection.value =
sortDirection.value==="asc"?"desc":"asc"

}else{

sortField.value = field
sortDirection.value="asc"

}

}


// PAGINAÇÃO

const totalPages = computed(()=>Math.ceil(sortedRows.value.length/pageSize.value)||1)

const paginatedRows = computed(()=>{

const start = (page.value-1)*pageSize.value

return sortedRows.value.slice(start,start+pageSize.value)

})

const startItem = computed(()=>{

if(!sortedRows.value.length) return 0

return (page.value-1)*pageSize.value+1

})

const endItem = computed(()=>{

if(!sortedRows.value.length) return 0

return Math.min(page.value*pageSize.value,sortedRows.value.length)

})


// EXPORTAR CSV/PDF

const exportarResiduos = (formato) => {

  const url = `http://localhost:8000/export/residuos?formato=${formato}`

  window.open(url, "_blank")

}



</script>