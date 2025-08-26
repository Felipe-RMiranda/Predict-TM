# 🧠 Predict-TM – Análise de Tomografias com IA

Este projeto utiliza redes neurais para realizar **análises automáticas de tomografias cerebrais (TC)** com o auxílio de **Inteligência Artificial**, visando a detecção de possíveis **tumores**.

## 📸 Demonstração

![Input](/diagnostics/static/demo-layout-imput.png)
![Output](/diagnostics/static/demo-layout-output.png)

---

## 🚀 Como executar o projeto

### ✅ Pré-requisitos

- Python 3.8+
- pip
- virtualenv (opcional, mas recomendado)

### 🔧 Instalação

```bash
# Clone o repositório
git clone https://github.com/Felipe-RMiranda/Predict-TM.git
cd Predict-TM

# Crie um ambiente virtual
python -m venv venv
source venv/bin/activate  # ou .\venv\Scripts\activate no Windows

# Instale as dependências
pip install -r requirements.txt

# Execute o servidor Django
python manage.py runserver
```

---

## 🧠 Tecnologias utilizadas

- [Python](https://www.python.org/)
- [Django](https://www.djangoproject.com/)
- [TensorFlow / Keras](https://www.tensorflow.org/)
- [Bootstrap](https://getbootstrap.com/)
- HTML5 / CSS3 / JavaScript

---

## 📁 Estrutura principal

```
Predict-TM/
├── eeg_diagnosis_backend/   # Backend Django com lógica de predição
├── static/                  # Imagens, CSS, JS
├── templates/               # Páginas HTML renderizadas
├── manage.py
└── requirements.txt
```

---

## 👨‍💻 Autor

- Felipe R. Miranda – [@Felipe-RMiranda](https://github.com/Felipe-RMiranda)
