<template>
  <div class="pt-32 pb-20 bg-gray-50 min-h-screen">

    <div class="max-w-6xl mx-auto px-6">

      <h1 class="text-4xl font-bold text-center mb-12">
        Contactos
      </h1>

      <div class="grid md:grid-cols-2 gap-12">

        <!-- INFORMAÇÕES -->
        <div>
          <h2 class="text-2xl font-semibold mb-6">Fale Connosco</h2>

          <p class="text-gray-600 mb-4">
            Estamos disponíveis para esclarecer dúvidas ou apresentar soluções
            sustentáveis para a sua empresa.
          </p>

          <div class="space-y-3 text-gray-700">
            <p><strong>Email:</strong> contacto@sgr.pt</p>
            <p><strong>Telefone:</strong> +351 999 999 999</p>
            <p><strong>Localização:</strong> Portugal</p>
          </div>
        </div>

        <!-- FORMULÁRIO -->
        <div class="bg-white p-8 rounded-2xl shadow-lg">
          <form class="space-y-6">

            <div>
              <label class="block mb-2 text-sm font-medium">Nome</label>
              <input type="text"
                     class="w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-green-500 outline-none">
            </div>

            <div>
              <label class="block mb-2 text-sm font-medium">Email</label>
              <input type="email"
                     class="w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-green-500 outline-none">
            </div>

            <div>
              <label class="block mb-2 text-sm font-medium">Mensagem</label>
              <textarea rows="4"
                        class="w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-green-500 outline-none"></textarea>
            </div>

            <button
              class="w-full bg-green-600 text-white py-3 rounded-lg hover:bg-green-700 transition">
              Enviar Mensagem
            </button>

          </form>
        </div>

      </div>

    </div>
  </div>
</template>