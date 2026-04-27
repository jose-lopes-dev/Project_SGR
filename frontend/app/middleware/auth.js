export default defineNuxtRouteMiddleware(async () => {

if (process.server) return

const token = localStorage.getItem("token")

if (!token) {
return navigateTo("/login")
}

// garante que o estado do auth está sincronizado e o utilizador carregado
const auth = useAuth()
await auth.restore()

})