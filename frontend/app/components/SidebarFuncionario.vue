<script setup>
const route = useRoute()

const items = [
  { to: "/funcionario/dashboard", label: "Dashboard", icon: "dashboard" },
  { to: "/funcionario/residuos", label: "Resíduos", icon: "residuos" },
  { to: "/funcionario/destino_residuos", label: "Destino Resíduos", icon: "destinos" },
]

const isActive = (to) => route.path === to
</script>

<template>
  <aside class="w-72 bg-slate-900 text-white min-h-screen p-6 flex flex-col">
    <div class="mb-8">
      <div class="text-xl font-bold leading-tight">Sistema Resíduos</div>
      <div class="text-xs text-slate-300 mt-1">Conta Funcionário</div>
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
          <svg v-else-if="it.icon === 'residuos'" viewBox="0 0 24 24" fill="none" class="w-5 h-5" stroke="currentColor" stroke-width="2">
            <path d="M4 19h16M6 17V7a2 2 0 012-2h8a2 2 0 012 2v10" />
            <path d="M9 9h6M9 13h6" />
          </svg>
          <svg v-else viewBox="0 0 24 24" fill="none" class="w-5 h-5" stroke="currentColor" stroke-width="2">
            <path d="M4 6h16M4 12h16M4 18h16" />
            <path d="M8 6v12" />
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