<template>
  <div class="flex min-h-screen">
    <SidebarFuncionario />
    <div class="flex-1 flex flex-col">
      <HeaderFuncionario />
      <main class="flex-1 p-6 bg-gray-100">
        <slot />
      </main>
    </div>
  </div>
</template>

<script setup>
import HeaderFuncionario from "~/components/HeaderFuncionario.vue";
import SidebarFuncionario from "~/components/SidebarFuncionario.vue";
</script>