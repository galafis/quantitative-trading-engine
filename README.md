# 📈 Quantitative Trading Engine

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)](https://www.docker.com/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688.svg)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791.svg)](https://www.postgresql.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

[English](#english) | [Português](#português)

---

## English

### 🎯 Overview

**Quantitative Trading Engine** — Algorithmic trading platform with backtesting engine, FastAPI REST API, and multiple strategy types (momentum, mean reversion, breakout). Built with Python, PostgreSQL, and Redis.

Total source lines: **1,823** across **30** files in **1** language.

### ✨ Key Features

- **Production-Ready Architecture**: Modular, well-documented, and following best practices
- **Comprehensive Implementation**: Complete solution with all core functionality
- **Clean Code**: Type-safe, well-tested, and maintainable codebase
- **Easy Deployment**: Docker support for quick setup and deployment

### 🚀 Quick Start

#### Prerequisites
- Python 3.12+
- Docker and Docker Compose (optional)

#### Installation

1. **Clone the repository**
```bash
git clone https://github.com/galafis/quantitative-trading-engine.git
cd quantitative-trading-engine
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

#### Running

```bash
python app/main.py
```

## 🐳 Docker

```bash
# Build and start
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

### 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov --cov-report=html

# Run with verbose output
pytest -v
```

### 📁 Project Structure

```
quantitative-trading-engine/
├── app/
│   ├── api/
│   │   ├── __init__.py
│   │   ├── backtest.py
│   │   ├── health.py
│   │   └── strategies.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   └── database.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── strategy.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── strategy.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── backtest.py
│   │   └── market_data.py
│   ├── strategies/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── breakout.py
│   │   ├── mean_reversion.py
│   │   └── momentum.py
│   ├── utils/
│   │   └── __init__.py
│   ├── __init__.py
│   └── main.py
├── docs/
│   └── images/
├── examples/
│   └── simple_backtest.py
├── tests/
│   ├── integration/
│   │   └── __init__.py
│   ├── unit/
│   │   ├── __init__.py
│   │   ├── test_backtest.py
│   │   ├── test_health.py
│   │   └── test_strategies.py
│   ├── __init__.py
│   └── conftest.py
├── CONTRIBUTING.md
├── README.md
├── docker-compose.yml
├── mypy.ini
├── pytest.ini
└── requirements.txt
```

### 🛠️ Tech Stack

| Technology | Usage |
|------------|-------|
| Python | 30 files |

### 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### 👤 Author

**Gabriel Demetrios Lafis**

- GitHub: [@galafis](https://github.com/galafis)
- LinkedIn: [Gabriel Demetrios Lafis](https://linkedin.com/in/gabriel-demetrios-lafis)

---

## Português

### 🎯 Visão Geral

**Quantitative Trading Engine** — Algorithmic trading platform with backtesting engine, FastAPI REST API, and multiple strategy types (momentum, mean reversion, breakout). Built with Python, PostgreSQL, and Redis.

Total de linhas de código: **1,823** em **30** arquivos em **1** linguagem.

### ✨ Funcionalidades Principais

- **Arquitetura Pronta para Produção**: Modular, bem documentada e seguindo boas práticas
- **Implementação Completa**: Solução completa com todas as funcionalidades principais
- **Código Limpo**: Type-safe, bem testado e manutenível
- **Fácil Implantação**: Suporte Docker para configuração e implantação rápidas

### 🚀 Início Rápido

#### Pré-requisitos
- Python 3.12+
- Docker e Docker Compose (opcional)

#### Instalação

1. **Clone the repository**
```bash
git clone https://github.com/galafis/quantitative-trading-engine.git
cd quantitative-trading-engine
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

#### Execução

```bash
python app/main.py
```

### 🧪 Testes

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov --cov-report=html

# Run with verbose output
pytest -v
```

### 📁 Estrutura do Projeto

```
quantitative-trading-engine/
├── app/
│   ├── api/
│   │   ├── __init__.py
│   │   ├── backtest.py
│   │   ├── health.py
│   │   └── strategies.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   └── database.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── strategy.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── strategy.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── backtest.py
│   │   └── market_data.py
│   ├── strategies/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── breakout.py
│   │   ├── mean_reversion.py
│   │   └── momentum.py
│   ├── utils/
│   │   └── __init__.py
│   ├── __init__.py
│   └── main.py
├── docs/
│   └── images/
├── examples/
│   └── simple_backtest.py
├── tests/
│   ├── integration/
│   │   └── __init__.py
│   ├── unit/
│   │   ├── __init__.py
│   │   ├── test_backtest.py
│   │   ├── test_health.py
│   │   └── test_strategies.py
│   ├── __init__.py
│   └── conftest.py
├── CONTRIBUTING.md
├── README.md
├── docker-compose.yml
├── mypy.ini
├── pytest.ini
└── requirements.txt
```

### 🛠️ Stack Tecnológica

| Tecnologia | Uso |
|------------|-----|
| Python | 30 files |

### 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

### 👤 Autor

**Gabriel Demetrios Lafis**

- GitHub: [@galafis](https://github.com/galafis)
- LinkedIn: [Gabriel Demetrios Lafis](https://linkedin.com/in/gabriel-demetrios-lafis)
