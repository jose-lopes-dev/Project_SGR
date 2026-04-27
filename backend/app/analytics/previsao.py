import numpy as np
from sklearn.linear_model import LinearRegression


def prever_receita(dados_receita):

    # dados_receita = [1000, 1200, 1400...]

    X = np.array(range(len(dados_receita))).reshape(-1, 1)
    y = np.array(dados_receita)

    modelo = LinearRegression()
    modelo.fit(X, y)

    # prever próximos 3 meses
    futuro = np.array(range(len(dados_receita), len(dados_receita) + 3)).reshape(-1, 1)

    previsao = modelo.predict(futuro)

    return previsao.tolist()