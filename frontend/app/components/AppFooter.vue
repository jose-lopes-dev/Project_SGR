<template>
  <footer class="bg-gray-900 text-gray-300 py-12">

    <div class="max-w-7xl mx-auto px-6 grid md:grid-cols-4 gap-10">

      <!-- LOGO -->
      <div>
        <h2 class="text-xl font-bold text-white mb-4">SGR</h2>
        <p class="text-sm">
          Sistema de Gestão de Resíduos focado na valorização sustentável
          e economia circular.
        </p>
      </div>

      <!-- LINKS -->
      <div>
        <h3 class="text-white font-semibold mb-4">Navegação</h3>
        <ul class="space-y-2">
          <li><NuxtLink to="/" class="hover:text-white">Home</NuxtLink></li>
          <li><NuxtLink to="/sobre" class="hover:text-white">Sobre</NuxtLink></li>
          <li><NuxtLink to="/impacto" class="hover:text-white">Impacto</NuxtLink></li>
          <li><NuxtLink to="/contactos" class="hover:text-white">Contactos</NuxtLink></li>
        </ul>
      </div>

      <!-- LEGAL -->
      <div>
        <h3 class="text-white font-semibold mb-4">Legal</h3>
        <ul class="space-y-2 text-sm">
          <li>Política de Privacidade</li>
          <li>Termos e Condições</li>
        </ul>
      </div>

      <!-- EXTERNO -->
      <div>
        <h3 class="text-white font-semibold mb-4">Projeto de Referência</h3>
        <a href="https://www.galrao.com/stome/"
           target="_blank"
           rel="noopener noreferrer"
           class="text-green-400 hover:text-green-300">
           Ver Projeto Externo
        </a>
      </div>

    </div>

    <div class="border-t border-gray-700 mt-10 pt-6 text-center text-sm text-gray-500">
      © 2026 Sistema de Gestão de Resíduos. Todos os direitos reservados.
    </div>

  </footer>
</template>