export const useApi = () => {

const config = useRuntimeConfig()

const request = async (url, options = {}) => {
  const token = process.client ? localStorage.getItem("token") : null

  return await $fetch(config.public.apiBase + url, {

    ...options,

    headers: {
      Authorization: token ? `Bearer ${token}` : "",
      ...options.headers
    }

  })

}


// RESIDUOS

const getResiduos = () => request("/residuos")

const getResiduo = (id) => request(`/residuos/${id}`)

const createResiduo = (data) =>
  request("/residuos", {
    method: "POST",
    body: data
  })

const deleteResiduo = (id) =>
  request(`/residuos/${id}`, {
    method: "DELETE"
  })



// TIPOS RESIDUOS

const getTiposResiduos = () => request("/tipos-residuos")

const createTipoResiduo = (data) =>
  request("/tipos-residuos", {
    method: "POST",
    body: data
  })

const updateResiduo = (id, data) =>
  request(`/residuos/${id}`, {
    method: "PUT",
    body: data
  })

const deleteTipoResiduo = (id) =>
  request(`/tipos-residuos/${id}`, {
    method: "DELETE"
  })


// MATERIAS PRIMAS

const getMateriasPrimas = () => request("/materias-primas")

const createMateriaPrima = (data) =>
  request("/materias-primas", {
    method: "POST",
    body: data
  })

const deleteMateriaPrima = (id) =>
  request(`/materias-primas/${id}`, {
    method: "DELETE"
  })



// LOCALIZACOES


const getLocalizacoes = () => request("/localizacoes")

const getLocalizacao = (id) => request(`/localizacoes/${id}`)

const createLocalizacao = (data) =>
  request("/localizacoes", {
    method: "POST",
    body: data
  })

const deleteLocalizacao = (id) =>
  request(`/localizacoes/${id}`, {
    method: "DELETE"
  })


// DESTINOS RESIDUOS


const getDestinos = () => request("/destinos-residuos")

const createDestino = (data) =>
  request("/destinos-residuos", {
    method: "POST",
    body: data
  })

const updateDestino = (id, data) =>
  request(`/destinos-residuos/${id}`, {
    method: "PUT",
    body: data
  })

const deleteDestino = (id) =>
  request(`/destinos-residuos/${id}`, {
    method: "DELETE"
  })



// UTILIZADORES


const getUtilizadores = () => request("/utilizadores")

const createUtilizador = (data) =>
  request("/utilizadores", {
    method: "POST",
    body: data
  })

const deleteUtilizador = (id) =>
  request(`/utilizadores/${id}`, {
    method: "DELETE"
  })


//DASHBOARD


const getDashboardResumo = () =>
  request("/dashboard/resumo")

const getDashboardKpis = (params) =>
  request("/dashboard/kpis", {
    query: params
  })

const getReceitaMensal = (ano) =>
  request(`/dashboard/receita-mensal?ano=${ano}`)

const getReceitaUltimos3Meses = (ref_ano = 2026, ref_mes = 3) =>
  request(`/dashboard/receita-ultimos-3-meses?ref_ano=${ref_ano}&ref_mes=${ref_mes}`)

const getFinanceiro = () =>
  request("/dashboard/financeiro")

const getFinanceiroUltimos3Meses = (ref_ano = 2026, ref_mes = 3) =>
  request(`/dashboard/financeiro-ultimos-3-meses?ref_ano=${ref_ano}&ref_mes=${ref_mes}`)

const getOperacional = () =>
  request("/dashboard/operacional")

const getOperacionalUltimos3Meses = (ref_ano = 2026, ref_mes = 3) =>
  request(`/dashboard/operacional-ultimos-3-meses?ref_ano=${ref_ano}&ref_mes=${ref_mes}`)

const getAmbiental = () =>
  request("/dashboard/ambiental")

const getAmbientalUltimos3Meses = (ref_ano = 2026, ref_mes = 3) =>
  request(`/dashboard/ambiental-ultimos-3-meses?ref_ano=${ref_ano}&ref_mes=${ref_mes}`)

const getPrevisaoReceita = () =>
  request("/dashboard/previsao-receita")


return {

// residuos
getResiduos,
getResiduo,
createResiduo,
deleteResiduo,
updateResiduo,

// tipos residuos
getTiposResiduos,
createTipoResiduo,
deleteTipoResiduo,

// materias primas
getMateriasPrimas,
createMateriaPrima,
deleteMateriaPrima,

// localizacoes
getLocalizacoes,
getLocalizacao,
createLocalizacao,
deleteLocalizacao,

// destinos
getDestinos,
createDestino,
deleteDestino,
updateDestino,

// utilizadores
getUtilizadores,
createUtilizador,
deleteUtilizador,

// dashboard
getDashboardResumo,
getDashboardKpis,
getReceitaMensal,
getReceitaUltimos3Meses,
getDashboardFinanceiro: getFinanceiro,
getFinanceiroUltimos3Meses,
getDashboardOperacional: getOperacional,
getOperacionalUltimos3Meses,
getDashboardAmbiental: getAmbiental,
getAmbientalUltimos3Meses,
getPrevisaoReceita

}

}