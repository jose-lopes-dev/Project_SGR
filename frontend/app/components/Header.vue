<script setup>

import { computed, onMounted, onUnmounted, ref } from "vue"

const { user, logout } = useAuth()
const route = useRoute()

const menu = ref(false)

const pageTitle = computed(() => {
  const p = route.path || ""
  if (p.includes("/admin/dashboard")) return "Dashboard"
  if (p.includes("/admin/operacional")) return "Operacional"
  if (p.includes("/admin/financeiro")) return "Financeiro"
  if (p.includes("/admin/ambiental")) return "Ambiental"
  if (p.includes("/admin/previsao")) return "Previsão"
  if (p.includes("/funcionario/dashboard")) return "Dashboard"
  if (p.includes("/funcionario/residuos")) return "Resíduos"
  if (p.includes("/funcionario/destino_residuos")) return "Destino de Resíduos"
  return "Sistema Resíduos"
})

const initials = computed(() => {
  const name = user.value?.nome || ""
  const parts = name.trim().split(/\s+/).filter(Boolean)
  const a = parts[0]?.[0] || "U"
  const b = parts[1]?.[0] || ""
  return (a + b).toUpperCase()
})

const onDocClick = (e) => {
  const el = e.target
  if (!(el instanceof Element)) return
  if (!el.closest("[data-user-menu]")) menu.value = false
}

onMounted(() => document.addEventListener("click", onDocClick))
onUnmounted(() => document.removeEventListener("click", onDocClick))
</script>

<template>

<header class="sticky top-0 z-40 flex justify-between items-center bg-white/80 backdrop-blur border-b px-6 py-4">

  <div class="flex items-center gap-3">
    <h1 class="font-bold text-lg text-slate-900">{{ pageTitle }}</h1>
    <span v-if="route.path?.startsWith('/admin')" class="text-xs px-2 py-1 rounded-full bg-slate-100 text-slate-700">
      Admin
    </span>
    <span v-else-if="route.path?.startsWith('/funcionario')" class="text-xs px-2 py-1 rounded-full bg-slate-100 text-slate-700">
      Funcionário
    </span>
  </div>

  <div class="relative" data-user-menu>

    <button
      class="flex items-center gap-3 hover:bg-slate-50 rounded-lg px-2 py-1 transition"
      @click="menu = !menu"
      type="button"
    >
      <div class="w-9 h-9 rounded-full bg-slate-900 text-white flex items-center justify-center font-semibold text-sm">
        {{ initials }}
      </div>
      <div class="hidden sm:flex flex-col items-start leading-tight">
        <div class="text-sm font-semibold text-slate-900">{{ user?.nome || "Utilizador" }}</div>
        <div class="text-xs text-slate-500">{{ user?.email || "" }}</div>
      </div>
      <svg viewBox="0 0 24 24" fill="none" class="w-4 h-4 text-slate-600" stroke="currentColor" stroke-width="2">
        <path d="M6 9l6 6 6-6" />
      </svg>
    </button>

    <div
      v-if="menu"
      class="absolute right-0 mt-2 bg-white shadow-lg rounded-xl p-2 w-56 border"
    >

      <div class="px-3 py-2">
        <div class="text-xs text-slate-500">Sessão</div>
        <div class="text-sm font-medium text-slate-900">
          {{ user?.role || "—" }}
        </div>
      </div>

      <div class="border-t my-1"></div>

      <button
        @click="logout"
        class="w-full text-left px-3 py-2 rounded-lg hover:bg-red-50 text-red-600 font-medium"
        type="button"
      >
        Logout
      </button>

    </div>

  </div>

</header>

</template>