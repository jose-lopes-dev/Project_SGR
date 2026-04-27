export const useAuth = () => {

const token = useState("token")
const role = useState("role")
const user = useState("user")

const restore = async () => {
  if (process.server) return

  const storedToken = localStorage.getItem("token")
  const storedRole = localStorage.getItem("role")

  if (storedToken) token.value = storedToken
  if (storedRole) role.value = storedRole

  if (storedToken) {
    await fetchMe()
  }
}

const fetchMe = async () => {
  if (process.server) return null
  if (!token.value) return null

  const config = useRuntimeConfig()

  try {
    const me = await $fetch(config.public.apiBase + "/utilizadores/me", {
      headers: {
        Authorization: `Bearer ${token.value}`
      }
    })

    user.value = me
    return me
  } catch (e) {
    user.value = null
    return null
  }
}

const login = async (email, password) => {

const config = useRuntimeConfig()

const formData = new URLSearchParams()

formData.append("username", email)
formData.append("password", password)

const res = await $fetch(config.public.apiBase + "/auth/login", {
  method: "POST",
  body: formData
})

token.value = res.access_token
role.value = res.role

localStorage.setItem("token", res.access_token)
localStorage.setItem("role", res.role)

await fetchMe()

if (res.role === "admin") {
navigateTo("/admin/dashboard")
} else {
navigateTo("/funcionario/dashboard")
}

}

const logout = () => {

token.value = null
role.value = null
user.value = null

localStorage.removeItem("token")
localStorage.removeItem("role")

navigateTo("/login")

}

return { token, role, user, login, logout, restore, fetchMe }

}