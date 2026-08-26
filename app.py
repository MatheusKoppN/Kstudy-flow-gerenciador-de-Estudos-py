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

st.set_page_config(page_title="KStudy Flow", layout="wide")

TRANSLATIONS = {
    "EN": {
        "page_title": "KStudy Flow — Study Manager & Academic Simulator",
        "sidebar_settings": "Settings",
        "sidebar_nav": "Navigation",
        "menu_dashboard": "Dashboard & Ranking",
        "menu_add": "Add Subject",
        "menu_session": "Log Study Session",
        "menu_grades": "Enter Grades",
        "menu_status": "Academic Status",
        "menu_export": "Export Data",
        "no_subjects": "No subjects registered yet.",
        "dash_title": "📊 Dashboard & Urgency Ranking",
        "pending_hours": "pending hours",
        "exam_date": "Exam Date:",
        "list_title": "Detailed Priority List",
        "col_subject": "Subject",
        "col_pending": "Pending Hours",
        "col_urgency": "Urgency",
        "col_score": "Score",
        "add_title": "➕ Register New Subject",
        "input_subject_name": "Subject Name",
        "input_target_hours": "Target Study Hours",
        "input_passing_grade": "Passing Grade Required",
        "input_assessment_qty": "Number of Assessments",
        "sub_assessments": "Assessments and Weights",
        "lbl_assessment_name": "Assessment Name",
        "lbl_assessment_weight": "Weight % for Assessment",
        "btn_add_subject": "Register Subject",
        "err_empty_name": "Subject name cannot be empty.",
        "err_weight_sum": "Sum of weights must equal exactly 100%. Current sum:",
        "msg_subject_added": "registered successfully!",
        "session_title": "⏱️ Log Study Session",
        "select_subject": "Select Subject:",
        "input_session_hours": "Hours studied in this session",
        "btn_save_session": "Save Session",
        "msg_hours_added": "hours added to",
        "grades_title": "📝 Enter Assessment Grades",
        "select_assessment": "Select Assessment:",
        "input_obtained_grade": "Grade Obtained (0 to 10)",
        "btn_save_grade": "Save Grade",
        "msg_grade_updated": "Grade updated successfully!",
        "status_title": "🎯 Academic Risk Simulator & Status",
        "lbl_passing_target": "Required Passing Grade:",
        "lbl_accumulated_avg": "Accumulated Average:",
        "lbl_remaining_weight": "Remaining Weight:",
        "err_impossible": "Required Avg on remaining: Impossible to pass via regular exams alone",
        "warn_required_avg": "Required Avg on remaining:",
        "lbl_assessments": "Assessments:",
        "lbl_pending": "Pending",
        "lbl_weight": "Weight",
        "export_title": "📁 Export Report",
        "btn_generate_csv": "Generate CSV File",
        "msg_csv_generated": "File 'relatorio_estudos.csv' generated in project directory!",
        "btn_download_csv": "Download CSV"
    },
    "PT": {
        "page_title": "KStudy Flow — Gerenciador de Estudos & Simulador Acadêmico",
        "sidebar_settings": "Configurações",
        "sidebar_nav": "Navegação",
        "menu_dashboard": "Dashboard & Ranking",
        "menu_add": "Cadastrar Matéria",
        "menu_session": "Registrar Sessão",
        "menu_grades": "Lançar Notas",
        "menu_status": "Status Acadêmico",
        "menu_export": "Exportar Dados",
        "no_subjects": "Nenhuma matéria cadastrada.",
        "dash_title": "📊 Dashboard & Ranking de Urgência",
        "pending_hours": "h pendentes",
        "exam_date": "Data Prova:",
        "list_title": "Lista Detalhada de Prioridade",
        "col_subject": "Matéria",
        "col_pending": "Horas Pendentes",
        "col_urgency": "Urgência",
        "col_score": "Score",
        "add_title": "➕ Cadastrar Nova Matéria",
        "input_subject_name": "Nome da Matéria",
        "input_target_hours": "Meta de horas de estudo",
        "input_passing_grade": "Média necessária para aprovação",
        "input_assessment_qty": "Quantidade de Avaliações",
        "sub_assessments": "Avaliações e Pesos",
        "lbl_assessment_name": "Nome da Avaliação",
        "lbl_assessment_weight": "Peso % da Avaliação",
        "btn_add_subject": "Cadastrar Matéria",
        "err_empty_name": "O nome da matéria não pode ficar vazio.",
        "err_weight_sum": "A soma dos pesos deve ser exatamente 100%. Soma atual:",
        "msg_subject_added": "cadastrada com sucesso!",
        "session_title": "⏱️ Registrar Sessão de Estudo",
        "select_subject": "Selecione a matéria:",
        "input_session_hours": "Horas estudadas nesta sessão",
        "btn_save_session": "Salvar Sessão",
        "msg_hours_added": "Adicionadas",
        "grades_title": "📝 Lançar Notas de Avaliações",
        "select_assessment": "Selecione a avaliação:",
        "input_obtained_grade": "Nota obtida (0 a 10)",
        "btn_save_grade": "Salvar Nota",
        "msg_grade_updated": "Nota atualizada com sucesso!",
        "status_title": "🎯 Simulador de Risco & Status Acadêmico",
        "lbl_passing_target": "Média de Aprovação:",
        "lbl_accumulated_avg": "Média Acumulada:",
        "lbl_remaining_weight": "Peso Restante:",
        "err_impossible": "Média Necessária nas próximas: Impossível passar apenas com provas regulares",
        "warn_required_avg": "Média Necessária nas próximas:",
        "lbl_assessments": "Avaliações:",
        "lbl_pending": "Pendente",
        "lbl_weight": "Peso",
        "export_title": "📁 Exportar Relatório",
        "btn_generate_csv": "Gerar Arquivo CSV",
        "msg_csv_generated": "Arquivo 'relatorio_estudos.csv' gerado no diretório do projeto!",
        "btn_download_csv": "Baixar CSV"
    }
}

st.sidebar.markdown("### Settings")
selected_lang = st.sidebar.selectbox("🌐 Language / Idioma", ["English (EN)", "Português (PT)"], index=0)
lang_code = "EN" if "English" in selected_lang else "PT"
t = TRANSLATIONS[lang_code]

dados = carregar_dados()

st.sidebar.title(t["sidebar_nav"])
menu = st.sidebar.radio(
    "Ir para / Go to:",
    [
        t["menu_dashboard"],
        t["menu_add"],
        t["menu_session"],
        t["menu_grades"],
        t["menu_status"],
        t["menu_export"]
    ]
)

if menu == t["menu_dashboard"]:
    st.title(t["dash_title"])

    if not dados:
        st.info(t["no_subjects"])
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
                    delta=f"{horas_pen:.1f}h {t['pending_hours']}"
                )
                st.caption(f"{t['exam_date']} {mat['data_prova']}")

        st.divider()
        st.subheader(t["list_title"])
        tabela = []
        for id_mat, mat in materias_ordenadas:
            urg_val = calcular_urgencia(mat)
            rotulo = obter_rotulo_urgencia(urg_val)
            horas_pen = mat["meta_horas"] - mat["horas_estudadas"]
            tabela.append({
                "ID": id_mat,
                t["col_subject"]: mat["materia"],
                t["exam_date"].replace(":", ""): mat["data_prova"],
                t["col_pending"]: f"{horas_pen:.2f}",
                t["col_urgency"]: rotulo,
                t["col_score"]: "∞" if urg_val == float("inf") else f"{urg_val:.2f}"
            })
        st.dataframe(pd.DataFrame(tabela), use_container_width=True)

elif menu == t["menu_add"]:
    st.title(t["add_title"])

    with st.form("form_cadastrar"):
        materia = st.text_input(t["input_subject_name"])
        meta_horas = st.number_input(t["input_target_hours"], min_value=0.1, step=0.5)
        data_prova = st.date_input(t["exam_date"].replace(":", ""))
        media_aprovacao = st.number_input(t["input_passing_grade"], min_value=0.0, max_value=10.0, value=7.0, step=0.5)
        qtd_avaliacoes = st.number_input(t["input_assessment_qty"], min_value=1, max_value=10, value=2, step=1)

        st.subheader(t["sub_assessments"])
        avaliacoes_temp = []
        soma_pesos = 0.0

        for i in range(int(qtd_avaliacoes)):
            col1, col2 = st.columns(2)
            with col1:
                nome_aval = st.text_input(f"{t['lbl_assessment_name']} {i+1}", value=f"P{i+1}", key=f"nome_{i}")
            with col2:
                peso_aval = st.number_input(f"{t['lbl_assessment_weight']} {i+1}", min_value=1.0, max_value=100.0, value=100.0/qtd_avaliacoes, key=f"peso_{i}")
            avaliacoes_temp.append({"nome": nome_aval, "peso": peso_aval / 100.0, "nota": None})
            soma_pesos += peso_aval

        cadastrar = st.form_submit_button(t["btn_add_subject"])

        if cadastrar:
            if not materia.strip():
                st.error(t["err_empty_name"])
            elif abs(soma_pesos - 100.0) > 0.01:
                st.error(f"{t['err_weight_sum']} {soma_pesos:.1f}%")
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
                st.success(f"'{materia}' {t['msg_subject_added']}")

elif menu == t["menu_session"]:
    st.title(t["session_title"])

    if not dados:
        st.info(t["no_subjects"])
    else:
        opcoes = {f"{id_m} - {m['materia']}": id_m for id_m, m in dados.items()}
        escolha = st.selectbox(t["select_subject"], list(opcoes.keys()))
        id_selecionado = opcoes[escolha]

        horas_estudadas = st.number_input(t["input_session_hours"], min_value=0.1, step=0.5)

        if st.button(t["btn_save_session"]):
            dados[id_selecionado]["horas_estudadas"] += float(horas_estudadas)
            salvar_dados(dados)
            st.success(f"{t['msg_hours_added']} {horas_estudadas}h -> {dados[id_selecionado]['materia']}!")

elif menu == t["menu_grades"]:
    st.title(t["grades_title"])

    if not dados:
        st.info(t["no_subjects"])
    else:
        opcoes_mat = {f"{id_m} - {m['materia']}": id_m for id_m, m in dados.items()}
        escolha_mat = st.selectbox(t["select_subject"], list(opcoes_mat.keys()))
        materia_obj = dados[opcoes_mat[escolha_mat]]

        opcoes_aval = [f"{i+1} - {av['nome']}" for i, av in enumerate(materia_obj["avaliacoes"])]
        escolha_aval = st.selectbox(t["select_assessment"], opcoes_aval)
        idx_aval = int(escolha_aval.split(" - ")[0]) - 1

        nota_atual = materia_obj["avaliacoes"][idx_aval]["nota"]
        valor_padrao = float(nota_atual) if nota_atual is not None else 0.0

        nova_nota = st.number_input(t["input_obtained_grade"], min_value=0.0, max_value=10.0, value=valor_padrao, step=0.1)

        if st.button(t["btn_save_grade"]):
            materia_obj["avaliacoes"][idx_aval]["nota"] = float(nova_nota)
            salvar_dados(dados)
            st.success(t["msg_grade_updated"])

elif menu == t["menu_status"]:
    st.title(t["status_title"])

    if not dados:
        st.info(t["no_subjects"])
    else:
        for id_mat, mat in dados.items():
            res = simular_risco(mat)
            with st.expander(f"[{id_mat}] {mat['materia']} - Status: {res['status']}"):
                st.write(f"**{t['lbl_passing_target']}** {mat['media_aprovacao']:.2f}")
                st.write(f"**{t['lbl_accumulated_avg']}** {res['pontos_acumulados']:.2f}")

                if res["peso_restante"] > 0:
                    st.write(f"**{t['lbl_remaining_weight']}** {res['peso_restante']*100:.0f}%")
                    if res["media_necessaria"] == float("inf"):
                        st.error(t["err_impossible"])
                    else:
                        st.warning(f"{t['warn_required_avg']} {res['media_necessaria']:.2f}")

                st.write(f"**{t['lbl_assessments']}**")
                for av in mat["avaliacoes"]:
                    n_str = f"{av['nota']:.2f}" if av["nota"] is not None else t["lbl_pending"]
                    st.text(f"- {av['nome']}: {n_str} ({t['lbl_weight']}: {av['peso']*100:.0f}%)")

elif menu == t["menu_export"]:
    st.title(t["export_title"])

    if not dados:
        st.info(t["no_subjects"])
    else:
        if st.button(t["btn_generate_csv"]):
            exportar_csv(dados)
            st.success(t["msg_csv_generated"])

        try:
            with open("relatorio_estudos.csv", "rb") as file:
                st.download_button(
                    label=t["btn_download_csv"],
                    data=file,
                    file_name="relatorio_estudos.csv",
                    mime="text/csv"
                )
        except FileNotFoundError:
            pass
