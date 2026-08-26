import streamlit as st
import pandas as pd
from estudos import (
    carregar_dados,
    salvar_dados,
    calcular_urgencia,
    obter_rotulo_urgencia,
    simular_risco,
    exportar_csv
)

st.set_page_config(page_title="Gerenciador de Estudos", layout="wide")

dados = carregar_dados()

st.sidebar.title("Navegação")
menu = st.sidebar.radio(
    "Ir para:",
    [
        "Dashboard & Ranking",
        "Cadastrar Matéria",
        "Registrar Sessão",
        "Lançar Notas",
        "Status Acadêmico",
        "Exportar Dados"
    ]
)

if menu == "Dashboard & Ranking":
    st.title("📊 Dashboard & Ranking de Urgência")

    if not dados:
        st.info("Nenhuma matéria cadastrada.")
    else:
        materias_ordenadas = sorted(
            dados.items(),
            key=lambda item: calcular_urgencia(item[1]),
            reverse=True
        )

        cols = st.columns(3)
        for idx, (id_mat, mat) in enumerate(materias_ordenadas):
            urg_val = calcular_urgencia(mat)
            rotulo = obter_rotulo_urgencia(urg_val)
            horas_pen = mat["meta_horas"] - mat["horas_estudadas"]

            with cols[idx % 3]:
                st.metric(
                    label=f"ID {id_mat} - {mat['materia']}",
                    value=rotulo,
                    delta=f"{horas_pen:.1f}h pendentes"
                )
                st.caption(f"Data Prova: {mat['data_prova']}")

        st.divider()
        st.subheader("Lista Detalhada de Prioridade")
        tabela = []
        for id_mat, mat in materias_ordenadas:
            urg_val = calcular_urgencia(mat)
            rotulo = obter_rotulo_urgencia(urg_val)
            horas_pen = mat["meta_horas"] - mat["horas_estudadas"]
            tabela.append({
                "ID": id_mat,
                "Matéria": mat["materia"],
                "Data Prova": mat["data_prova"],
                "Horas Pendentes": f"{horas_pen:.2f}",
                "Urgência": rotulo,
                "Score": "∞" if urg_val == float("inf") else f"{urg_val:.2f}"
            })
        st.dataframe(pd.DataFrame(tabela), use_container_width=True)

elif menu == "Cadastrar Matéria":
    st.title("➕ Cadastrar Nova Matéria")

    with st.form("form_cadastrar"):
        materia = st.text_input("Nome da Matéria")
        meta_horas = st.number_input("Meta de horas de estudo", min_value=0.1, step=0.5)
        data_prova = st.date_input("Data da Prova")
        media_aprovacao = st.number_input("Média necessária para aprovação", min_value=0.0, max_value=10.0, value=7.0, step=0.5)
        qtd_avaliacoes = st.number_input("Quantidade de Avaliações", min_value=1, max_value=10, value=2, step=1)

        st.subheader("Avaliações e Pesos")
        avaliacoes_temp = []
        soma_pesos = 0.0

        for i in range(int(qtd_avaliacoes)):
            col1, col2 = st.columns(2)
            with col1:
                nome_aval = st.text_input(f"Nome da Avaliação {i+1}", value=f"P{i+1}", key=f"nome_{i}")
            with col2:
                peso_aval = st.number_input(f"Peso % da Avaliação {i+1}", min_value=1.0, max_value=100.0, value=100.0/qtd_avaliacoes, key=f"peso_{i}")
            avaliacoes_temp.append({"nome": nome_aval, "peso": peso_aval / 100.0, "nota": None})
            soma_pesos += peso_aval

        cadastrar = st.form_submit_button("Cadastrar Matéria")

        if cadastrar:
            if not materia.strip():
                st.error("O nome da matéria não pode ficar vazio.")
            elif abs(soma_pesos - 100.0) > 0.01:
                st.error(f"A soma dos pesos deve ser exatamente 100%. Soma atual: {soma_pesos:.1f}%")
            else:
                novo_id = str(max(map(int, dados.keys()), default=0) + 1)
                dados[novo_id] = {
                    "materia": materia.strip(),
                    "meta_horas": float(meta_horas),
                    "horas_estudadas": 0.0,
                    "data_prova": str(data_prova),
                    "media_aprovacao": float(media_aprovacao),
                    "avaliacoes": avaliacoes_temp
                }
                salvar_dados(dados)
                st.success(f"Matéria '{materia}' cadastrada com sucesso!")

elif menu == "Registrar Sessão":
    st.title("⏱️ Registrar Sessão de Estudo")

    if not dados:
        st.info("Nenhuma matéria cadastrada.")
    else:
        opcoes = {f"{id_m} - {m['materia']}": id_m for id_m, m in dados.items()}
        escolha = st.selectbox("Selecione a matéria:", list(opcoes.keys()))
        id_selecionado = opcoes[escolha]

        horas_estudadas = st.number_input("Horas estudadas nesta sessão", min_value=0.1, step=0.5)

        if st.button("Salvar Sessão"):
            dados[id_selecionado]["horas_estudadas"] += float(horas_estudadas)
            salvar_dados(dados)
            st.success(f"Adicionadas {horas_estudadas}h para {dados[id_selecionado]['materia']}!")

elif menu == "Lançar Notas":
    st.title("📝 Lançar Notas de Avaliações")

    if not dados:
        st.info("Nenhuma matéria cadastrada.")
    else:
        opcoes_mat = {f"{id_m} - {m['materia']}": id_m for id_m, m in dados.items()}
        escolha_mat = st.selectbox("Selecione a matéria:", list(opcoes_mat.keys()))
        materia_obj = dados[opcoes_mat[escolha_mat]]

        opcoes_aval = [f"{i+1} - {av['nome']}" for i, av in enumerate(materia_obj["avaliacoes"])]
        escolha_aval = st.selectbox("Selecione a avaliação:", opcoes_aval)
        idx_aval = int(escolha_aval.split(" - ")[0]) - 1

        nota_atual = materia_obj["avaliacoes"][idx_aval]["nota"]
        valor_padrao = float(nota_atual) if nota_atual is not None else 0.0

        nova_nota = st.number_input("Nota obtida (0 a 10)", min_value=0.0, max_value=10.0, value=valor_padrao, step=0.1)

        if st.button("Salvar Nota"):
            materia_obj["avaliacoes"][idx_aval]["nota"] = float(nova_nota)
            salvar_dados(dados)
            st.success("Nota atualizada com sucesso!")

elif menu == "Status Acadêmico":
    st.title("🎯 Simulador de Risco & Status Acadêmico")

    if not dados:
        st.info("Nenhuma matéria cadastrada.")
    else:
        for id_mat, mat in dados.items():
            res = simular_risco(mat)
            with st.expander(f"[{id_mat}] {mat['materia']} - Status: {res['status']}"):
                st.write(f"**Média de Aprovação:** {mat['media_aprovacao']:.2f}")
                st.write(f"**Média Acumulada:** {res['pontos_acumulados']:.2f}")

                if res["peso_restante"] > 0:
                    st.write(f"**Peso Restante:** {res['peso_restante']*100:.0f}%")
                    if res["media_necessaria"] == float("inf"):
                        st.error("Média Necessária nas próximas: Impossível passar apenas com provas regulares")
                    else:
                        st.warning(f"Média Necessária nas próximas: {res['media_necessaria']:.2f}")

                st.write("**Avaliações:**")
                for av in mat["avaliacoes"]:
                    n_str = f"{av['nota']:.2f}" if av["nota"] is not None else "Pendente"
                    st.text(f"- {av['nome']}: {n_str} (Peso: {av['peso']*100:.0f}%)")

elif menu == "Exportar Dados":
    st.title("📁 Exportar Relatório")

    if not dados:
        st.info("Nenhuma matéria cadastrada.")
    else:
        if st.button("Gerar Arquivo CSV"):
            exportar_csv(dados)
            st.success("Arquivo 'relatorio_estudos.csv' gerado no diretório do projeto!")

        try:
            with open("relatorio_estudos.csv", "rb") as file:
                st.download_button(
                    label="Baixar CSV",
                    data=file,
                    file_name="relatorio_estudos.csv",
                    mime="text/csv"
                )
        except FileNotFoundError:
            pass