<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const scrolled = ref(false)

const handleScroll = () => {
  scrolled.value = window.scrollY > 50
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll)
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})
</script>

<template>
  <header
    :class="[
      'fixed w-full z-50 transition-all duration-300',
      scrolled
        ? 'bg-white/80 backdrop-blur-md shadow-md'
        : 'bg-white'
    ]"
  >
    <div class="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">

      <!-- LOGO -->
      <div class="text-xl font-bold"
           :class="{ 'text-gray-900': scrolled }">
        SGR
        </div>

      <!-- MENU -->
      <nav class="hidden md:flex gap-8 font-medium"
           :class="{ 'text-gray-800': scrolled, 'text-gray-900': !scrolled }">

        <NuxtLink to="/">Home</NuxtLink>
        <NuxtLink to="/sobre">Sobre</NuxtLink>
        <NuxtLink to="/impacto">Impacto</NuxtLink>
        <NuxtLink to="/contactos">Contactos</NuxtLink>        
        <NuxtLink to="/login" class="bg-green-500 text-white px-8 py-1 rounded-xl font-semibold hover:bg-green-600 transition inline-block h-8">Login</NuxtLink>

      </nav>

    </div>
  </header>
</template>