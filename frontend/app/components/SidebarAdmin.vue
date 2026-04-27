<script setup>
const route = useRoute()

const items = [
  {
    to: "/admin/dashboard",
    label: "Dashboard",
    icon: "dashboard",
  },
  {
    to: "/admin/operacional",
    label: "Operacional",
    icon: "operacional",
  },
  {
    to: "/admin/financeiro",
    label: "Financeiro",
    icon: "financeiro",
  },
  {
    to: "/admin/ambiental",
    label: "Ambiental",
    icon: "ambiental",
  },
  {
    to: "/admin/previsao",
    label: "Previsão",
    icon: "previsao",
  },
]

const isActive = (to) => route.path === to
</script>

<template>
  <aside class="w-72 bg-slate-900 text-white min-h-screen p-6 flex flex-col">
    <div class="mb-8">
      <div class="text-xl font-bold leading-tight">Sistema Resíduos</div>
      <div class="text-xs text-slate-300 mt-1">Conta Admin</div>
    </div>

    <nav class="flex flex-col gap-1">
      <NuxtLink
        v-for="it in items"
        :key="it.to"
        :to="it.to"
        class="flex items-center gap-3 px-3 py-2 rounded-lg transition"
        :class="isActive(it.to) ? 'bg-slate-800 text-white' : 'text-slate-200 hover:bg-slate-800/70 hover:text-white'"
      >
        <span class="w-5 h-5 inline-flex items-center justify-center">
          <svg v-if="it.icon === 'dashboard'" viewBox="0 0 24 24" fill="none" class="w-5 h-5" stroke="currentColor" stroke-width="2">
            <path d="M4 13h7V4H4v9zm9 7h7V11h-7v9zM4 20h7v-5H4v5zm9-9h7V4h-7v7z" />
          </svg>
          <svg v-else-if="it.icon === 'operacional'" viewBox="0 0 24 24" fill="none" class="w-5 h-5" stroke="currentColor" stroke-width="2">
            <path d="M3 12h6l3-8 3 16 3-8h3" />
          </svg>
          <svg v-else-if="it.icon === 'financeiro'" viewBox="0 0 24 24" fill="none" class="w-5 h-5" stroke="currentColor" stroke-width="2">
            <path d="M12 1v22M17 5H9.5a3.5 3.5 0 000 7H14a3.5 3.5 0 010 7H6" />
          </svg>
          <svg v-else-if="it.icon === 'ambiental'" viewBox="0 0 24 24" fill="none" class="w-5 h-5" stroke="currentColor" stroke-width="2">
            <path d="M12 22s8-4 8-12V6l-8-4-8 4v4c0 8 8 12 8 12z" />
          </svg>
          <svg v-else viewBox="0 0 24 24" fill="none" class="w-5 h-5" stroke="currentColor" stroke-width="2">
            <path d="M3 3v18h18M7 15l3-3 3 2 5-6" />
          </svg>
        </span>
        <span class="font-medium">{{ it.label }}</span>
      </NuxtLink>
    </nav>

    <div class="mt-auto pt-6 text-xs text-slate-400">
      ESG • 2026
    </div>
  </aside>
</template>