import csv
import json
from datetime import date, datetime

NOME_ARQUIVO = "dados_materias.json"


# ============================================================
# MÓDULO A - DADOS & PERSISTÊNCIA
# ============================================================

def carregar_dados():
    try:
        with open(NOME_ARQUIVO, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except FileNotFoundError:
        return {}
    except Exception:
        return {}


def salvar_dados(dados):
    try:
        with open(NOME_ARQUIVO, "w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Erro ao salvar dados: {e}")


# ============================================================
# MÓDULO A - CADASTRO
# ============================================================

def cadastrar_materia(dados):
    novo_id = str(max(map(int, dados.keys()), default=0) + 1)

    # Nome
    while True:
        materia = input("Nome da matéria: ").strip()
        if materia:
            break
        print("O nome da matéria não pode ficar vazio.")

    # Meta de horas
    while True:
        try:
            meta_horas = float(input("Meta de horas de estudo: "))
            if meta_horas <= 0:
                print("A meta deve ser maior que zero.")
                continue
            break
        except ValueError:
            print("Digite um número válido.")

    # Data da prova
    while True:
        data_prova = input("Data da prova (AAAA-MM-DD): ").strip()
        try:
            datetime.strptime(data_prova, "%Y-%m-%d")
            break
        except ValueError:
            print("Data inválida. Use o formato AAAA-MM-DD.")

    # Média de aprovação
    while True:
        try:
            media_aprovacao = float(input("Média necessária para aprovação: "))
            if not 0 <= media_aprovacao <= 10:
                print("A média deve estar entre 0 e 10.")
                continue
            break
        except ValueError:
            print("Digite um número válido.")

    # Quantidade de avaliações
    while True:
        try:
            quantidade = int(input("Quantidade de avaliações: "))
            if quantidade <= 0:
                print("Cadastre pelo menos uma avaliação.")
                continue
            break
        except ValueError:
            print("Digite um número inteiro válido.")

    # Cadastro das avaliações
    while True:
        avaliacoes = []
        soma_pesos = 0

        for i in range(quantidade):
            print(f"\n--- Avaliação {i + 1} ---")

            while True:
                nome = input("Nome da avaliação: ").strip()
                if nome:
                    break
                print("O nome não pode ficar vazio.")

            while True:
                try:
                    peso = float(input("Peso da avaliação (%): "))
                    if peso <= 0:
                        print("O peso deve ser maior que zero.")
                        continue
                    break
                except ValueError:
                    print("Digite um número válido.")

            peso = peso / 100
            soma_pesos += peso

            avaliacoes.append({
                "nome": nome,
                "peso": peso,
                "nota": None
            })

        if abs(soma_pesos - 1.0) > 0.0001:
            print(f"\nOs pesos cadastrados totalizam {soma_pesos * 100:.2f}%.")
            print("A soma dos pesos precisa ser exatamente 100%.")
            print("\nCadastre os pesos novamente.")
        else:
            break

    dados[novo_id] = {
        "materia": materia,
        "meta_horas": meta_horas,
        "horas_estudadas": 0,
        "data_prova": data_prova,
        "media_aprovacao": media_aprovacao,
        "avaliacoes": avaliacoes
    }

    salvar_dados(dados)
    print(f"\nMatéria '{materia}' cadastrada com sucesso!")


# ============================================================
# MÓDULO A - URGÊNCIA & RANKING
# ============================================================

def calcular_urgencia(materia):
    data_prova = datetime.strptime(materia["data_prova"], "%Y-%m-%d").date()
    dias_restantes = (data_prova - date.today()).days
    horas_pendentes = materia["meta_horas"] - materia["horas_estudadas"]

    if horas_pendentes <= 0:
        return 0.0

    if dias_restantes <= 0:
        return float("inf")

    return float(horas_pendentes / dias_restantes)


def obter_rotulo_urgencia(urgencia):
    if urgencia == float("inf"):
        return "URGENTE"
    elif urgencia > 1.5:
        return "PRIORIDADE ALTA"
    elif urgencia > 0.5:
        return "MODERADO"
    elif urgencia > 0:
        return "CONFORTÁVEL"
    else:
        return "CONCLUÍDO"


def exibir_ranking(dados):
    if not dados:
        print("\nNenhuma matéria cadastrada.")
        return

    materias_ordenadas = sorted(
        dados.items(),
        key=lambda item: calcular_urgencia(item[1]),
        reverse=True
    )

    print("\n========== RANKING DE PRIORIDADE ==========")
    for posicao, (id_materia, materia) in enumerate(materias_ordenadas, start=1):
        horas_pendentes = materia["meta_horas"] - materia["horas_estudadas"]
        urgencia = calcular_urgencia(materia)
        rotulo = obter_rotulo_urgencia(urgencia)

        if urgencia == float("inf"):
            score = f"{rotulo}"
        else:
            score = f"{urgencia:.2f} ({rotulo})"

        print(
            f"{posicao}. [ID {id_materia}] {materia['materia']} | "
            f"Prova: {materia['data_prova']} | "
            f"Horas pendentes: {horas_pendentes:.2f} | "
            f"Urgência: {score}"
        )
    print("============================================")


# ============================================================
# MÓDULO A - REGISTRO DE SESSÃO
# ============================================================

def registrar_sessao(dados):
    if not dados:
        print("\nNenhuma matéria cadastrada.")
        return

    print("\n========== MATÉRIAS ==========")
    for id_materia, materia in dados.items():
        print(f"{id_materia} - {materia['materia']}")
    print("===============================")

    while True:
        id_materia = input("Digite o ID da matéria estudada: ").strip()
        if id_materia in dados:
            break
        print("ID não encontrado.")

    while True:
        try:
            horas = float(input("Quantas horas você estudou? "))
            if horas <= 0:
                print("A quantidade de horas deve ser maior que zero.")
                continue
            break
        except ValueError:
            print("Digite um número válido. Exemplo: 1.5")

    dados[id_materia]["horas_estudadas"] += horas
    salvar_dados(dados)

    print("\nSessão registrada com sucesso!")
    print(f"Matéria: {dados[id_materia]['materia']}")
    print(f"Horas adicionadas: {horas:.2f}")
    print(f"Total estudado: {dados[id_materia]['horas_estudadas']:.2f} horas")


# ============================================================
# MÓDULO B - LANÇAMENTO DE NOTAS
# ============================================================

def lancar_notas(dados):
    if not dados:
        print("\nNenhuma matéria cadastrada.")
        return

    print("\n========== MATÉRIAS ==========")
    for id_materia, materia in dados.items():
        print(f"{id_materia} - {materia['materia']}")
    print("===============================")

    while True:
        id_materia = input("Digite o ID da matéria: ").strip()
        if id_materia in dados:
            break
        print("ID não encontrado.")

    materia = dados[id_materia]

    print(f"\nAvaliações de {materia['materia']}:")
    for i, avaliacao in enumerate(materia["avaliacoes"], start=1):
        if avaliacao["nota"] is None:
            nota = "Não lançada"
        else:
            nota = f"{avaliacao['nota']:.2f}"
        print(f"{i} - {avaliacao['nome']} | Peso: {avaliacao['peso'] * 100:.0f}% | Nota: {nota}")

    while True:
        try:
            numero = int(input("\nDigite o número da avaliação: "))
            if 1 <= numero <= len(materia["avaliacoes"]):
                break
            print("Avaliação inexistente.")
        except ValueError:
            print("Digite um número inteiro válido.")

    avaliacao = materia["avaliacoes"][numero - 1]

    while True:
        try:
            nota = float(input(f"Digite a nota de {avaliacao['nome']} (0 a 10): "))
            if not 0 <= nota <= 10:
                print("A nota deve estar entre 0 e 10.")
                continue
            break
        except ValueError:
            print("Digite uma nota válida.")

    avaliacao["nota"] = nota
    salvar_dados(dados)
    print(f"\nNota {nota:.2f} lançada em {avaliacao['nome']}!")


# ============================================================
# MÓDULO B - SIMULADOR DE RISCO & STATUS ACADÊMICO
# ============================================================

def simular_risco(materia):
    pontos_acumulados = 0.0
    peso_restante = 0.0

    for avaliacao in materia["avaliacoes"]:
        peso = avaliacao["peso"]
        nota = avaliacao["nota"]

        if nota is None:
            peso_restante += peso
        else:
            pontos_acumulados += (nota * peso)

    media_aprovacao = materia["media_aprovacao"]

    if pontos_acumulados >= media_aprovacao:
        return {
            "pontos_acumulados": pontos_acumulados,
            "peso_restante": peso_restante,
            "media_necessaria": 0.0,
            "status": "Aprovado / Garantido"
        }

    if peso_restante <= 0:
        return {
            "pontos_acumulados": pontos_acumulados,
            "peso_restante": 0.0,
            "media_necessaria": float("inf"),
            "status": "Risco Crítico / Reprovado"
        }

    pontos_faltantes = media_aprovacao - pontos_acumulados
    media_necessaria = pontos_faltantes / peso_restante

    if media_necessaria > 10:
        status = "Risco Crítico / Reprovado"
    elif media_necessaria > 6:
        status = "Atenção"
    else:
        status = "Confortável"

    return {
        "pontos_acumulados": pontos_acumulados,
        "peso_restante": peso_restante,
        "media_necessaria": media_necessaria,
        "status": status
    }


def exibir_status_academicos(dados):
    if not dados:
        print("\nNenhuma matéria cadastrada.")
        return

    print("\n========== STATUS ACADÊMICO ==========")
    for id_materia, materia in dados.items():
        resultado = simular_risco(materia)
        print(f"\n[{id_materia}] {materia['materia']}")
        print(f"Média para aprovação: {materia['media_aprovacao']:.2f}")
        print(f"Média acumulada: {resultado['pontos_acumulados']:.2f}")

        if resultado["peso_restante"] > 0:
            print(f"Peso restante: {resultado['peso_restante'] * 100:.0f}%")
            if resultado["media_necessaria"] == float("inf"):
                print("Média necessária: impossível")
            else:
                print(f"Média necessária nas próximas: {resultado['media_necessaria']:.2f}")

        print(f"Status: {resultado['status']}")
        print("Avaliações:")
        for avaliacao in materia["avaliacoes"]:
            if avaliacao["nota"] is None:
                nota = "Pendente"
            else:
                nota = f"{avaliacao['nota']:.2f}"
            print(f"  - {avaliacao['nome']}: {nota} ({avaliacao['peso'] * 100:.0f}%)")

    print("\n=======================================")


# ============================================================
# MÓDULO D - EXPORTAÇÃO CSV
# ============================================================

def exportar_csv(dados):
    if not dados:
        print("Nenhuma matéria cadastrada para exportar.")
        return

    nome_arquivo = "relatorio_estudos.csv"
    campos = [
        "ID", "Matéria", "Meta Horas", "Horas Estudadas", "Horas Pendentes",
        "Data da Prova", "Urgência", "Média de Aprovação", "Média Acumulada", 
        "Média Necessária", "Status de Risco"
    ]

    try:
        with open(nome_arquivo, "w", newline="", encoding="utf-8-sig") as arquivo:
            escritor = csv.DictWriter(arquivo, fieldnames=campos)
            escritor.writeheader()

            for id_materia, materia in dados.items():
                resultado = simular_risco(materia)
                horas_pendentes = materia["meta_horas"] - materia["horas_estudadas"]
                urgencia = calcular_urgencia(materia)
                rotulo_urgencia = obter_rotulo_urgencia(urgencia)

                media_necessaria = resultado["media_necessaria"]
                if media_necessaria == float("inf"):
                    media_necessaria = "Impossível"
                else:
                    media_necessaria = f"{media_necessaria:.2f}"

                escritor.writerow({
                    "ID": id_materia,
                    "Matéria": materia["materia"],
                    "Meta Horas": f"{materia['meta_horas']:.2f}",
                    "Horas Estudadas": f"{materia['horas_estudadas']:.2f}",
                    "Horas Pendentes": f"{horas_pendentes:.2f}",
                    "Data da Prova": materia["data_prova"],
                    "Urgência": rotulo_urgencia,
                    "Média de Aprovação": f"{materia['media_aprovacao']:.2f}",
                    "Média Acumulada": f"{resultado['pontos_acumulados']:.2f}",
                    "Média Necessária": media_necessaria,
                    "Status de Risco": resultado["status"]
                })

        print(f"\nRelatório exportado com sucesso!\nArquivo: {nome_arquivo}")

    except OSError as e:
        print(f"Erro ao criar o relatório: {e}")


# ============================================================
# MENU PRINCIPAL
# ============================================================

if __name__ == "__main__":
    dados = carregar_dados()

    while True:
        print("\n======================================")
        print("       GERENCIADOR DE ESTUDOS")
        print("======================================")
        print("1 - Cadastrar Matéria")
        print("2 - Registrar Sessão de Estudo")
        print("3 - Ver Ranking de Prioridade")
        print("4 - Lançar Notas")
        print("5 - Ver Status Acadêmico")
        print("6 - Exportar Relatório CSV")
        print("0 - Sair")
        print("======================================")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            cadastrar_materia(dados)
        elif opcao == "2":
            registrar_sessao(dados)
        elif opcao == "3":
            exibir_ranking(dados)
        elif opcao == "4":
            lancar_notas(dados)
        elif opcao == "5":
            exibir_status_academicos(dados)
        elif opcao == "6":
            exportar_csv(dados)
        elif opcao == "0":
            print("\nEncerrando o programa...")
            break
        else:
            print("\nOpção inválida. Escolha uma opção do menu.")
            