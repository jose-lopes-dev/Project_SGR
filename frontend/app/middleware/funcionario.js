export default defineNuxtRouteMiddleware(() => {
  if (process.server) return

  const role = localStorage.getItem("role")

  if (role !== "funcionario") {
    return navigateTo("/login")
  }
})