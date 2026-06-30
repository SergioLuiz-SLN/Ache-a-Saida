# 🔍 Ache a Saída

> Sistema web de troubleshooting desenvolvido em Python e Flask que transforma uma planilha Excel em um fluxo interativo de diagnóstico.

---

## 📖 Sobre o projeto

O **Ache a Saída** é uma aplicação web criada para facilitar o atendimento de suporte técnico através de fluxos de decisão.

Em vez de programar toda a lógica em código, o sistema utiliza uma planilha Excel como banco de dados dos fluxos de troubleshooting. Cada aplicação possui sua própria aba na planilha, permitindo criar árvores de decisão sem alterar o código da aplicação.

O objetivo é permitir que analistas de suporte encontrem rapidamente a solução correta respondendo apenas perguntas de **Sim** ou **Não**.

---

## ✨ Funcionalidades

- Interface web simples e intuitiva
- Fluxos de decisão ilimitados
- Cada aba da planilha representa uma aplicação diferente
- Carregamento automático dos fluxos
- Perguntas com respostas "Sim" e "Não"
- Exibição automática da solução final
- Fácil manutenção por usuários que conhecem Excel
- Não é necessário alterar código para criar novos fluxos

---

## 🏗 Arquitetura

```
                troubleshooting.xlsx
                         │
                         ▼
              Leitura com Pandas
                         │
                         ▼
          Estrutura em memória (dicionário)
                         │
                         ▼
                  Aplicação Flask
                         │
                         ▼
                Interface HTML (Jinja2)
                         │
                         ▼
              Usuário responde perguntas
                         │
                         ▼
              Navegação pelo fluxo lógico
```

---

## 📁 Estrutura do projeto

```
Ache-a-Saida/

│
├── AcheaSaida.py          # Aplicação Flask
├── troubleshooting.xlsx   # Base de conhecimento
├── requirements.txt
│
└── Templates/
      ├── Index.html
      └── flow.html
```

---

## ⚙ Tecnologias

- Python
- Flask
- Pandas
- OpenPyXL
- HTML
- CSS
- Jinja2

---

## 📊 Como funciona

O sistema lê todas as abas da planilha Excel.

Cada aba representa uma aplicação diferente.

Cada linha da planilha possui um tipo:

| Tipo | Descrição |
|-------|-----------|
| pergunta | Pergunta apresentada ao usuário |
| solucao | Resultado final do troubleshooting |

Para perguntas, também são definidos os próximos passos para as respostas:

- Sim
- Não

Assim, é possível criar uma árvore completa de decisões apenas editando a planilha.

---

## ▶ Executando

Clone o repositório:

```bash
git clone https://github.com/sergioslldsn777-design/Ache-a-Saida.git
```

Entre na pasta:

```bash
cd Ache-a-Saida
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Execute:

```bash
python AcheaSaida.py
```

A aplicação ficará disponível em:

```
http://localhost:5000
```

---

## 📋 Exemplo de fluxo

```
Aplicação

        │

Usuário seleciona

        │

Pergunta 1

     ├── Sim
     │      │
     │      ▼
     │   Pergunta 2
     │
     └── Não
            │
            ▼
        Solução

```

---

## 📄 Estrutura da planilha

Cada aba deve possuir colunas semelhantes a:

| ID | Tipo | Texto | Próx. Sim | Próx. Não |
|----|------|-------|-----------|-----------|

Exemplo:

| ID | Tipo | Texto | Próx. Sim | Próx. Não |
|----|------|-------|-----------|-----------|
| q1 | pergunta | O sistema abre? | q2 | s1 |
| q2 | pergunta | Há conexão? | s2 | s3 |
| s1 | solucao | Reinstalar aplicação | | |
| s2 | solucao | Reiniciar serviço | | |
| s3 | solucao | Verificar rede | | |

---

## 🎯 Casos de uso

Este projeto pode ser utilizado para:

- Service Desk
- Help Desk
- Operações de TI
- Troubleshooting de aplicações
- Documentação operacional
- Runbooks interativos
- Base de conhecimento
- Onboarding de novos analistas

---

## 🚀 Melhorias futuras

- Pesquisa por palavras-chave
- Banco de dados SQL
- Cadastro de fluxos pela interface
- Histórico de atendimentos
- Login de usuários
- Estatísticas de utilização
- Exportação dos fluxos
- Upload de planilhas pela interface
- Interface responsiva
- Integração com IA para sugestão automática de soluções

---

## 👨‍💻 Autor

Desenvolvido por **Sergio Nunes**.

---

## 📜 Licença

Este projeto está disponível para fins de estudo e demonstração.

```

