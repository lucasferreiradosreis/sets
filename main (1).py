import streamlit as st

def calcular_sets(dados_corte_final):
    comprimento_principal_min, comprimento_principal_max = dados_corte_final["comprimento_principal"]
    faixa_curtos = dados_corte_final.get("faixa_curtos", None)
    tipo_multiplo = dados_corte_final.get("tipo_multiplo", False)
    valor_multiplo = dados_corte_final.get("valor_multiplo", None)
    porcentagem_curtos = dados_corte_final.get("porcentagem_curtos", 0)
    contracao = dados_corte_final["contracao"]

    batentes_serra1 = {
        1: (3000, 7500),
        2: (7500, 12000),
        3: (17000, 24000)
    }

    def comprimento_com_contracao(comprimento, quantidade=1):
        return (comprimento + contracao) * quantidade

    def esta_na_faixa(comprimento, faixa):
        return faixa[0] <= comprimento <= faixa[1]

    def gerar_comprimentos_permitidos(faixa, multiplo):
        comprimentos = []
        minimo, maximo = faixa
        for comprimento in range(minimo, maximo + 1, multiplo):
            comprimentos.append((comprimento, comprimento + 100))
        return comprimentos

    comprimentos_principais = gerar_comprimentos_permitidos(
        (comprimento_principal_min, comprimento_principal_max), valor_multiplo
    )

    comprimentos_curtos = []
    if faixa_curtos:
        comprimentos_curtos = gerar_comprimentos_permitidos(
            faixa_curtos, valor_multiplo
        )

    resultados = {1: [], 2: [], 3: []}

    for minimo, maximo in comprimentos_principais:
        for comprimento in range(minimo, maximo + 1, 100):
            for batente, faixa in batentes_serra1.items():
                quantidade = 1
                while True:
                    comprimento_total = comprimento_com_contracao(comprimento, quantidade)
                    if comprimento_total > faixa[1]:
                        break
                    if esta_na_faixa(comprimento_total, faixa):
                        resultados[batente].append((comprimento_total, f"{comprimento}x{quantidade} + {contracao} aplicado no máx."))

                        if faixa_curtos:
                            for curto_min, curto_max in comprimentos_curtos:
                                for curto_comprimento in range(curto_min, curto_max + 1, 100):
                                    comprimento_total_curto = comprimento_total + comprimento_com_contracao(curto_comprimento, 1)
                                    if comprimento_total_curto <= faixa[1]:
                                        resultados[batente].append((comprimento_total_curto, f"{comprimento}x{quantidade} + {curto_comprimento}x1 + {contracao} aplicado no máx."))
                    quantidade += 1

    if porcentagem_curtos > 0:
        for batente in resultados:
            sets_principais = [set_ for set_ in resultados[batente] if "+ Curto" not in set_[1]]
            sets_curtos = [set_ for set_ in resultados[batente] if "+ Curto" in set_[1]]

            total_barras = len(sets_principais) + len(sets_curtos)
            max_curtos = int(total_barras * porcentagem_curtos / 100)

            resultados[batente] = sets_principais + sets_curtos[:max_curtos]

    return resultados

def app():
    st.title('Calculadora de Sets de Corte')

    comprimento_principal_min = st.number_input('Comprimento Principal Mínimo', min_value=1000, value=6000)
    comprimento_principal_max = st.number_input('Comprimento Principal Máximo', min_value=1000, value=7000)
    faixa_curtos_min = st.number_input('Faixa Curtos Mínima', min_value=0, value=5000)
    faixa_curtos_max = st.number_input('Faixa Curtos Máxima', min_value=0, value=5500)
    tipo_multiplo = st.checkbox('É Múltiplo?', value=True)
    valor_multiplo = st.number_input('Valor do Múltiplo', min_value=0, value=500)
    porcentagem_curtos = st.number_input('Porcentagem de Curtos', min_value=0, max_value=100, value=15)
    contracao = st.number_input('Valor da Contração', min_value=0, value=45)

    if st.button('Calcular'):
        dados_corte_final = {
            "comprimento_principal": (comprimento_principal_min, comprimento_principal_max),
            "faixa_curtos": (faixa_curtos_min, faixa_curtos_max) if faixa_curtos_min and faixa_curtos_max else None,
            "tipo_multiplo": tipo_multiplo,
            "valor_multiplo": valor_multiplo,
            "porcentagem_curtos": porcentagem_curtos,
            "contracao": contracao
        }

        sets_possiveis = calcular_sets(dados_corte_final)

        for batente, sets in sets_possiveis.items():
            st.write(f"**Batente {batente}:**")
            for comprimento, detalhes in sets:
                st.write(f"{comprimento} ({detalhes})")

if __name__ == "__main__":
    app()
