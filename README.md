# 📌 Projeto: API de Recuperação de Documentos com RAG

## 📖 Descrição

Este projeto implementa uma API para recuperação de documentos utilizando **FastAPI**, **Sentence Transformers** para embeddings de texto, e **Ollama** para geração de respostas baseadas nos documentos mais relevantes. O sistema processa arquivos de texto e PDF, divide-os em chunks e encontra o documento mais relevante para responder às perguntas dos usuários.

## 🚀 Funcionalidades

- Carregamento automático de documentos `.txt` e `.pdf` da pasta `data/`.
- Opção de carregar apenas arquivos `.txt`, apenas `.pdf` ou ambos.
- Segmentação de documentos em chunks para melhor indexação.
- Uso de **embeddings** para encontrar o documento mais relevante para uma consulta.
- Integração com **Ollama** para geração de respostas baseadas no conteúdo do documento.
- Uso do **Guardian Sail** para garantir controle de acesso e segurança nas consultas.
- Retorno do nome do documento de origem na resposta.

---

## 🛠️ Tecnologias Utilizadas

- **FastAPI** - Framework para criação de APIs.
- **Sentence Transformers** - Para criação de embeddings dos documentos.
- **Ollama** - Para geração de respostas baseadas nos documentos.
- **Uvicorn** - Servidor para rodar a API.
- **Logging** - Para monitoramento e debug.
- **Guardian Sail** - Para controle de acesso e segurança nas respostas da API.

---

## 📂 Estrutura do Projeto

```
RAG_FASTAPI
│── 📂 data/               # Pasta contendo os arquivos de texto e PDF
│── 📂 services/            # Serviços de processamento e consulta
│   │── query_service.py        # Serviço para processar consultas RAG
│   │── document_service.py     # Processamento dos documentos e embeddings
│   │── pdf_service.py          # Carregamento e processamento de PDFs
│   │── txt_service.py          # Carregamento e processamento de textos
│── 📂 utils/              # Utilitários adicionais
│   │── guardian_sail.py        # Implementação do Guardian Sail para controle de acesso
│── 📜 rag.py              # API RAG sem LLM
│── 📜 rag_llm.py         # API RAG com LLM
│── 📜 README.md           # Documentação do projeto
│── 📜 requirements.txt    # Dependências do projeto
│── 📜 test_main.http      # Testes da API RAG
│── 📜 test_main_llm.http  # Testes da API RAG com LLM
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

A API será iniciada em **[http://localhost:8000](http://localhost:8000)**

```sh
python rag.py
```

A API será iniciada em **[http://localhost:8080](http://localhost:8080)**

---

## 🔍 Uso da API

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
- Retorna a resposta com o nome do documento fonte.

### 📜 **`rag_llm.py`**

- Configura a API com **FastAPI**.
- Recebe a consulta do usuário.
- Usa **embeddings** para encontrar o documento mais relevante.
- Envia o documento para **Ollama** para gerar uma resposta.
- Retorna a resposta com o nome do documento fonte.

### 📜 **`services/query_service.py`**

- Responsável por processar a consulta do usuário e encontrar o documento mais relevante.
- Calcula a similaridade entre embeddings da query e dos documentos.
- Utiliza **Guardian Sail** para garantir que respostas respeitem políticas de segurança.

### 📜 **`services/document_service.py`**

- Gerencia o carregamento e processamento de documentos .txt e .pdf.
- Utiliza Sentence Transformers para gerar embeddings dos documentos.
- Permite carregar documentos específicos por tipo (txt, pdf ou ambos).
- Implementa uma função para reconstruir textos eliminando sobreposição de chunks.

### 📜 **`services/service_txt.py`**

- Responsável por carregar e processar arquivos `.txt` do diretório especificado.
- Divide os textos em chunks (trechos menores) para facilitar o processamento posterior.
- Implementa sobreposição (`overlap`) para garantir que a divisão de trechos não perca contexto.

### 📜 **`services/service_pdf.py`**

- Responsável por carregar e processar arquivos `.pdf` do diretório especificado.
- Extrai o texto de cada página do PDF utilizando **PyMuPDF (fitz)**.
- Divide o texto em chunks para facilitar a indexação.
- Adiciona metadados como o número da página ao documento processado.

### 📜 **`utils/guardian_sail.py`**

- Implementa camadas de segurança na API.
- Aplica regras de controle de acesso e auditoria sobre as respostas geradas.
- Evita vazamento de informações sensíveis ou fora do escopo permitido.

---

## 📌 Melhorias Futuras

- Armazenamento de embeddings em um banco de dados para otimizar a busca.
- Suporte a mais formatos de documentos (DOCX, HTML).
- Implementação de cache para evitar recomputação de embeddings.
- Aprimoramento do **Guardian Sail** para validar respostas com base em regras dinâmicas.

---

## 📧 Contato

Caso tenha dúvidas ou sugestões, sinta-se à vontade para contribuir! 😊

