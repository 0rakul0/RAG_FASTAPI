# 📌 Projeto: API de Recuperação de Documentos com RAG

## 📖 Descrição
Este projeto implementa uma API para recuperação de documentos utilizando **FastAPI**, **Sentence Transformers** para embeddings de texto, e **Ollama** para geração de respostas baseadas nos documentos mais relevantes. O sistema processa arquivos de texto e PDF, divide-os em chunks e encontra o documento mais relevante para responder às perguntas dos usuários.

## 🚀 Funcionalidades
- Carregamento automático de documentos `.txt` e `.pdf` da pasta `data/`.
- Opção de carregar apenas arquivos `.txt`, apenas `.pdf` ou ambos.
- Segmentação de documentos em chunks para melhor indexação.
- Uso de **embeddings** para encontrar o documento mais relevante para uma consulta.
- Integração com **Ollama** para geração de respostas baseadas no conteúdo do documento.
- Retorno do nome do documento de origem na resposta.

---

## 🛠️ Tecnologias Utilizadas
- **FastAPI** - Framework para criação de APIs.
- **Sentence Transformers** - Para criação de embeddings dos documentos.
- **Ollama** - Para geração de respostas baseadas nos documentos.
- **Uvicorn** - Servidor para rodar a API.
- **Logging** - Para monitoramento e debug.

---

## 📂 Estrutura do Projeto
```
📁 projeto_rag_api
│── 📂 data/               # Pasta contendo os arquivos de texto e PDF
│── 📜 rag.py              # rag sem llm FastAPI
│── 📜 rag_llm.py         # rag com llm FastAPI
│── 📜 service_document.py # Processamento dos documentos e embeddings
│── 📜 README.md           # Documentação do projeto
│── 📜 requirements.txt    # Dependências do projeto
│── 📜 teste_rag.http      # teste do rag
│── 📜 teste_rag_llm.http  # teste da rag com llm
```

---

## 📌 Como Executar
### 1️⃣ Instalar dependências
```sh
pip install -r requirements.txt
```
### 2️⃣ Iniciar a API
```sh
python rag_llm.py
```
A API será iniciada em **http://localhost:8000**

```sh
python rag.py
```
A API será iniciada em **http://localhost:8080**

---

## 📡 Uso da API
### 🔎 **Endpoint: /query**
- **Método:** `POST`
- **Descrição:** Retorna a resposta baseada no documento mais relevante.
- **Entrada:**
  ```json
  {
    "query": "Como dividir textos em segmentos menores?"
  }
  ```
- **Saída:**
  ```json
  {
    "pergunta": "Como dividir textos em segmentos menores?",
    "resposta": "A segmentação de textos em chunks facilita a indexação...",
    "documento_fonte": "documento1.txt"
  }
  ```

---

## 🛠️ Desenvolvimento
### 📜 **`rag.py`**
- Configura a API com **FastAPI**.
- Recebe a consulta do usuário.
- Usa **embeddings** para encontrar o documento mais relevante.
- Retorna a resposta junto com o nome do documento fonte.

### 📜 **`rag_llm.py`**
- Configura a API com **FastAPI**.
- Recebe a consulta do usuário.
- Usa **embeddings** para encontrar o documento mais relevante.
- Envia o documento para **Ollama** para gerar uma resposta.
- Retorna a resposta junto com o nome do documento fonte.

### 📜 **`service_document.py`**
- Carrega os arquivos `.txt` e `.pdf` da pasta `data/`.
- Opção de carregar apenas `.txt`, apenas `.pdf` ou ambos.
- Divide os documentos em chunks (parágrafos).
- Gera embeddings usando **Sentence Transformers**.

---

## 📌 Melhorias Futuras
- Armazenamento de embeddings em um banco de dados para otimizar a busca.
- Suporte a mais formatos de documentos (DOCX, HTML).
- Implementação de cache para evitar recomputação de embeddings.

---

## 📧 Contato
Caso tenha dúvidas ou sugestões, sinta-se à vontade para contribuir! 😊
