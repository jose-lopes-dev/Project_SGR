<script setup>

definePageMeta({
layout: "auth"
})

const email = ref("")
const password = ref("")
const error = ref("")
const loading = ref(false)

const { login } = useAuth()

const fazerLogin = async () => {

error.value = ""
loading.value = true

try {

await login(email.value, password.value)

} catch (e) {

error.value = "Email ou password inválidos"

}

loading.value = false

}

</script>

<template>

<div class="bg-white p-8 rounded-xl shadow-lg">

<h2 class="text-3xl font-bold text-center mb-6">
Sistema de Gestão de Resíduos
</h2>

<input
v-model="email"
placeholder="Email"
class="w-full border p-3 mb-4 rounded"
/>

<input
v-model="password"
type="password"
placeholder="Password"
class="w-full border p-3 mb-4 rounded"
/>

<button
@click="fazerLogin"
class="w-full bg-green-600 text-white p-3 rounded hover:bg-green-700"
>

<span v-if="loading">Entrando...</span>
<span v-else>Entrar</span>

</button>

<p v-if="error" class="text-red-500 mt-4 text-center">
{{ error }}
</p>

</div>

</template>