<template>
  <div class="flex min-h-screen">
    <SidebarAdmin />
    <div class="flex-1 flex flex-col">
      <Header />
      <main class="flex-1 p-6">
        <slot />
      </main>
    </div>
  </div>
</template>

<script setup>

import SidebarAdmin from "~/components/SidebarAdmin.vue"
import Header from "~/components/Header.vue"

</script>