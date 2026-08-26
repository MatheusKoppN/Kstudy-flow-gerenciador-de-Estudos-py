# 📚 KStudy Flow — Study Manager & Academic Simulator

A **Full-Stack Python application** designed to optimize academic routines for higher education and technical students. The system automatically calculates **study priority levels (urgency algorithm)** based on pending study hours and upcoming exam dates, while simulating **required weighted averages** and **academic failure risks** in real time.

> 🇧🇷 **Read this in Portuguese:** [README_PT.md](./README_PT.md)

---

## 💡 Key Features

* 📊 **Dynamic Prioritization Algorithm:** Categorizes subjects by urgency level (`URGENT`, `HIGH PRIORITY`, `MODERATE`, `COMFORTABLE`, `COMPLETED`) calculated from pending study hours versus remaining days until assessment.
* 🎯 **Academic Risk Simulator ($N$ Assessments):** Supports subjects with custom weights and exam counts. Computes the exact required passing grade on upcoming exams to reach target passing scores.
* ⏱️ **Study Session Tracking:** Logs cumulative study time with persistent storage updates.
* 📝 **Flexible Grade Entry:** Tracks partial scores across the semester and updates academic risk metrics instantaneously.
* 📁 **CSV Report Export:** Generates Excel/Google Sheets compatible reports containing consolidated metrics (`utf-8-sig` encoded).
* 💻 **Dual Interface (CLI & Web Dashboard):** Decoupled backend supporting both an interactive Terminal CLI and an interactive Streamlit Dashboard.

---

## 🛠️ Tech Stack

* **Language:** [Python 3.10+](https://www.python.org/)
* **Web Framework:** [Streamlit](https://streamlit.io/)
* **Data Manipulation:** [Pandas](https://pandas.pydata.org/)
* **Data Persistence:** Structured `JSON` files (ISO date standards)
* **Export Engine:** Native `CSV` module with dynamic headers

---

## 🧮 Mathematical Logic & Business Rules

### 1. Urgency Score Formula

$$\text{Urgency Score} = \frac{\text{Target Hours} - \text{Completed Hours}}{\text{Exam Date} - \text{Current Date (Days)}}$$

### 2. Required Average on Remaining Exams

$$\text{Required Average} = \frac{\text{Target Grade} \times (\sum \text{Weights}) - \sum (\text{Obtained Grade} \times \text{Weight})}{\sum \text{Remaining Weights}}$$

---

## 📁 Repository Structure

```text
.
├── app.py                  # Main Web Dashboard interface (Streamlit)
├── estudos.py              # Backend logic, business rules, calculations, and CLI
├── dados_materias.json     # Local persistent database (auto-generated)
├── relatorio_estudos.csv   # Exported academic performance report
├── requirements.txt        # Python dependencies manifest
└── README.md               # Project documentation

```

---

## 🚀 Getting Started

### Prerequisites

Ensure you have **Python 3.10+** installed on your machine.

### Setup Instructions

1. **Clone the repository:**

```bash
git clone [https://github.com/MatheusKoppN/Kstudy-flow-gerenciador-de-Estudos-py.git](https://github.com/MatheusKoppN/Kstudy-flow-gerenciador-de-Estudos-py.git)
cd Kstudy-flow-gerenciador-de-Estudos-py

```

2. **Create and activate a virtual environment (Optional):**

* **Windows:**

```powershell
python -m venv venv
.\venv\Scripts\activate

```

* **Linux / macOS:**

```bash
python3 -m venv venv
source venv/bin/activate

```

3. **Install dependencies:**

```bash
pip install -r requirements.txt

```

4. **Launch the Web Dashboard (Streamlit):**

```bash
streamlit run app.py

```

5. **Run via Terminal (CLI Mode):**

```bash
python estudos.py

```

---

## 👨‍💻 Author & Contact

**Matheus Kopp do Nascimento**

*Software & Data Engineering Student | Electrical Engineering Student*

* 📧 **Email:** [matheuskoppn@gmail.com](https://www.google.com/search?q=mailto%3Amatheuskoppn%40gmail.com)
* 💼 **LinkedIn:** [linkedin.com/in/matheus-kopp-do-nascimento-426a783b5](https://www.linkedin.com/in/matheus-kopp-do-nascimento-426a783b5/)
* 🐙 **GitHub:** [github.com/MatheusKoppN](https://www.google.com/url?sa=E&source=gmail&q=https://github.com/MatheusKoppN)

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.
