
<template>
  <router-link 
  to="/login"
  class="bg-white text-green-700 px-6 py-3 rounded-lg font-semibold"
>
Login
</router-link>

  <div class="bg-white text-gray-900">

    <!-- HERO -->
    <section class="relative overflow-hidden pt-32">
      <div class="absolute inset-0 bg-gradient-to-br from-green-600 via-emerald-500 to-teal-600 opacity-90"></div>

      <div class="relative max-w-7xl mx-auto px-6 py-32 text-center text-white">
        <h1 class="text-5xl md:text-6xl font-extrabold leading-tight mb-6">
          Gestão Inteligente de Resíduos
        </h1>

        <p class="text-xl md:text-2xl text-green-100 max-w-3xl mx-auto mb-10">
          Transformamos resíduos industriais em valor sustentável através de tecnologia e inovação.
        </p>

        <div class="flex justify-center gap-6">
          <a href="#sobre"
             class="bg-white text-green-700 px-8 py-4 rounded-xl font-semibold shadow-lg hover:scale-105 transition">
            Explorar
          </a>

          <a href="contactos"
             class="border border-white px-8 py-4 rounded-xl hover:bg-white hover:text-green-700 transition">
            Fale Connosco
          </a>
        </div>
      </div>
    </section>

    <!-- SOBRE -->
    <section id="sobre" class="py-24 bg-gray-50">
      <div class="max-w-6xl mx-auto px-6 text-center">
        <h2 class="text-4xl font-bold mb-6">
          Tecnologia ao Serviço da Sustentabilidade
        </h2>

        <p class="text-lg text-gray-600 max-w-3xl mx-auto">
          O nosso sistema permite rastrear, mapear e analisar resíduos provenientes de pedreiras e transformação de mármore e granito,
          promovendo a economia circular e a valorização de recursos.
        </p>
      </div>
    </section>

    <!-- FEATURES -->
    <section class="py-24 bg-white">
      <div class="max-w-7xl mx-auto px-6">

        <div class="text-center mb-16">
          <h2 class="text-4xl font-bold">Soluções Inteligentes</h2>
          <p class="text-gray-500 mt-4">
            Plataforma digital para monitorização e valorização sustentável
          </p>
        </div>

        <div class="grid md:grid-cols-3 gap-10">

          <div class="bg-gray-50 p-10 rounded-2xl shadow-sm hover:shadow-xl transition">
            <h3 class="text-xl font-semibold mb-4">Rastreabilidade</h3>
            <p class="text-gray-600">
              Monitorização em tempo real dos resíduos gerados e classificação automática por tipo.
            </p>
          </div>

          <div class="bg-gray-50 p-10 rounded-2xl shadow-sm hover:shadow-xl transition">
            <h3 class="text-xl font-semibold mb-4">Análise de Dados</h3>
            <p class="text-gray-600">
              Dashboards inteligentes que identificam padrões e oportunidades de reutilização.
            </p>
          </div>

          <div class="bg-gray-50 p-10 rounded-2xl shadow-sm hover:shadow-xl transition">
            <h3 class="text-xl font-semibold mb-4">Economia Circular</h3>
            <p class="text-gray-600">
              Transformação de resíduos em novos produtos e oportunidades sustentáveis.
            </p>
          </div>

        </div>
      </div>
    </section>

    <!-- IMPACTO VISUAL -->
    <section class="py-24 bg-gradient-to-r from-green-50 to-emerald-50">
      <div class="max-w-6xl mx-auto px-6 grid md:grid-cols-2 gap-16 items-center">

        <div>
          <h2 class="text-4xl font-bold mb-6">
            Impacto Ambiental Positivo
          </h2>

          <p class="text-gray-600 mb-6">
            Reabilitação de pedreiras desativadas e reaproveitamento sustentável dos materiais,
            reduzindo a pegada ecológica e promovendo inovação verde.
          </p>

          <a href="https://www.galrao.com/stome/"
            target="_blank"
            rel="noopener noreferrer"
            class="bg-white text-green-700 px-8 py-4 rounded-xl font-semibold shadow-lg hover:scale-105 transition">
            Ver Projeto Real
          </a>
        </div>
        
        <div class="rounded-2xl overflow-hidden shadow-2xl">
          <img src="/images/pedreira.jpg" alt="Pedreira Reabilitada" class="w-full">
        </div>
      </div>

    </section>

    <!-- CTA FINAL -->
    <section class="py-24 bg-gray-900 text-white text-center">
      <h2 class="text-4xl font-bold mb-6">
        Pronto para tornar a sua empresa mais sustentável?
      </h2>

      <p class="text-gray-300 mb-8">
        Adote soluções inteligentes e transforme resíduos em valor.
      </p>

      <a href="contactos"
         class="bg-green-500 px-8 py-4 rounded-xl font-semibold hover:bg-green-600 transition">
        Começar Agora
      </a>
    </section>


  </div>

</template>