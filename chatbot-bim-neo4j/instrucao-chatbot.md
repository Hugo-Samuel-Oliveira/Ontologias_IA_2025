# 🛠️ Como Executar o Projeto

Siga estes passos para configurar e executar o protótipo no seu ambiente local.

---

## 1. ✅ Pré-requisitos

Certifique-se de que os seguintes softwares estão instalados:

- **Java JDK 17+**
- **Neo4j Desktop**
- **Python 3.8, 3.9 ou 3.10**
- **Git**

---

## 2. 📦 Instalação

Clone o repositório para o seu computador:

```bash
git clone <URL_DO_SEU_REPOSITORIO>
cd <NOME_DA_PASTA_DO_PROJETO>
```

Crie e ative um ambiente virtual para o projeto:

**Criar ambiente:**

```bash
python -m venv venv
```

**Ativar no Windows:**

```bash
.\venv\Scripts\activate
```

**Ativar no macOS ou Linux:**

```bash
source venv/bin/activate
```

Se esta for a primeira vez que configura o repositório, gere o arquivo `requirements.txt`:

```bash
pip freeze > requirements.txt
```

Instale todas as dependências:

```bash
pip install -r requirements.txt
```

---

## 3. ⚙️ Configuração

Configure o seu banco de dados Neo4j:

1. Abra o **Neo4j Desktop**.
2. Crie um novo DBMS local com o nome `ifctest`.
3. Defina uma senha e anote-a.
4. Inicie ("Start") o banco de dados.
5. Atualize os arquivos com a senha:
    - Abra `src/ifc_to_neo4j.py` e insira sua senha na variável `NEO4J_PASSWORD`.
    - Abra `actions/actions.py` e insira a mesma senha na variável `NEO4J_PASSWORD`.

---

## 4. 🚀 Execução do Chatbot

Execute o projeto em 3 passos, usando dois terminais.

### 🔹 Passo 1: Popular o Banco de Dados

No primeiro terminal (com ambiente virtual ativo):

```bash
python src/ifc_to_neo4j.py
```

Aguarde pela mensagem de sucesso. Esse passo só precisa ser feito uma vez.

### 🔹 Passo 2: Iniciar o Servidor de Ações do Rasa

Ainda no primeiro terminal:

```bash
rasa run actions
```

Deixe esse terminal aberto.

### 🔹 Passo 3: Treinar e Iniciar o Chatbot

No segundo terminal, ative o ambiente virtual e:

**Treinar o modelo:**

```bash
rasa train
```

**Iniciar a interface de chat:**

```bash
rasa shell
```

Agora você pode interagir com o assistente virtual.

---

## 5. 💬 Como Usar o Chatbot

Converse com o assistente! Comece com uma saudação e faça perguntas sobre os elementos do arquivo de exemplo.

**Exemplos de perguntas:**

- Quantas IfcWall existem?
- Qual a contagem de IfcSlab?
- Me diga o número de IfcRoof.

---