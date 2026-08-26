# 📚 KStudy Flow — O Gerenciador de Estudos & Simulador Acadêmico

Uma aplicação **Full-Stack em Python** desenvolvida para otimizar a rotina de estudantes do ensino superior e técnico. O sistema calcula automaticamente a **prioridade de estudos (algoritmo de urgência)** com base na carga horária pendente e na proximidade das provas, além de simular a **média ponderada necessária** e o **risco de reprovação** em tempo real.

---

## 💡 Funcionalidades Principais

* 📊 **Algoritmo de Priorização Dinâmica:** Classifica as matérias por nível de urgência (`URGENTE`, `PRIORIDADE ALTA`, `MODERADO`, `CONFORTÁVEL`, `CONCLUÍDO`) com base na relação entre horas faltantes e dias restantes para a avaliação.
* 🎯 **Simulador de Risco Acadêmico ($N$ Avaliações):** Suporta disciplinas com quantidades e pesos customizados de provas/trabalhos. Calcula a nota média exata necessária nas avaliações restantes para atingir a aprovação.
* ⏱️ **Registro de Sessões de Estudo:** Incrementa o progresso de horas acumuladas com persistência de dados.
* 📝 **Lançamento Flexível de Notas:** Permite registrar notas parciais ao longo do semestre e atualiza o status de risco instantaneamente.
* 📁 **Exportação de Relatórios (CSV):** Gera planilhas compatíveis com Excel/Google Sheets contendo métricas consolidadas (utilizando encoding `utf-8-sig` para compatibilidade de caracteres).
* 💻 **Interface Dupla (CLI & Web Dashboard):** Backend desacoplado que funciona tanto via Terminal interativo quanto via Dashboard interativo no Streamlit.

---

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** [Python 3.10+](https://www.python.org/)
* **Interface Web:** [Streamlit](https://streamlit.io/)
* **Manipulação de Dados:** [Pandas](https://pandas.pydata.org/)
* **Persistência de Dados:** Arquivos estruturados em `JSON` (padrão ISO para datas)
* **Exportação:** Módulo nativo `CSV` com cabeçalho dinâmico

---

## 🧮 Lógica Matemática & Regras de Negócio

### 1. Score de Urgência

$$\text{Urgência} = \frac{\text{Meta de Horas} - \text{Horas Estudadas}}{\text{Data da Prova} - \text{Data Atual (Dias)}}$$

### 2. Média Necessária nas Próximas Avaliações

$$\text{Nota Média Necessária} = \frac{\text{Média Alvo} \times (\sum \text{Pesos}) - \sum (\text{Nota Obtida} \times \text{Peso})}{\sum \text{Pesos Restantes}}$$

---

## 📁 Estrutura do Projeto

```text
├── app.py                  # Interface visual do Dashboard Web (Streamlit)
├── estudos.py              # Backend com regras de negócio, cálculos e CLI
├── dados_materias.json     # Arquivo de persistência local (gerado automaticamente)
├── relatorio_estudos.csv   # Relatório exportado do desempenho acadêmico
├── requirements.txt        # Dependências do projeto
└── README.md               # Documentação do projeto

```

---

## 🔧 Como Executar o Projeto

### Pré-requisitos

Certifique-se de ter o **Python 3.10+** instalado na sua máquina.

### 1. Criar e ativar um ambiente virtual (Opcional, mas recomendado)

```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate

```

### 2. Instalar as dependências

```bash
pip install -r requirements.txt

```

### 3. Executar a Aplicação Web (Streamlit)

```bash
streamlit run app.py

```

### 4. Executar a Aplicação via Terminal (CLI)

```bash
python estudos.py

```

---

## 👨‍💻 Autor & Contato

**Matheus Kopp do Nascimento**  
Estudante de Engenharia Elétrica & Análise e Desenvolvimento de Sistemas

* 📧 **E-mail:** [matheuskoppn@gmail.com](mailto:matheuskoppn@gmail.com)
* 💼 **LinkedIn:** [linkedin.com/in/matheus-kopp-do-nascimento](https://www.linkedin.com/in/matheus-kopp-do-nascimento-426a783b5)
* 🐙 **GitHub:** [github.com/MatheusKoppN](https://github.com/MatheusKoppN)
---

## 📜 Licença

Este projeto está sob a licença **MIT** — veja o arquivo [LICENSE](https://www.google.com/search?q=LICENSE) para mais detalhes.

---
