# Ache a Saída

> Sistema web de troubleshooting desenvolvido em Python e Flask que transforma uma planilha Excel em um fluxo interativo de diagnóstico.

---

## 📖 Sobre o projeto

O **Ache a Saída** é uma aplicação web criada para facilitar o atendimento de suporte técnico através de fluxos de decisão.

Os fluxos de troubleshooting são definidos em uma planilha Excel, permitindo que analistas atualizem a base de conhecimento sem modificar o código da aplicação.

Essa abordagem separa a lógica da aplicação do conteúdo dos fluxos, tornando a manutenção simples e permitindo que novos procedimentos sejam adicionados sem alterações no código-fonte. Cada aplicação possui sua própria aba na planilha.

O objetivo é permitir que analistas de suporte encontrem rapidamente a solução correta respondendo apenas perguntas de **Sim** ou **Não**.

---

## ✨ Funcionalidades

- Interface responsiva com busca de aplicações
- Fluxos de decisão ilimitados
- Cada aba da planilha representa uma aplicação diferente
- Carregamento automático dos fluxos
- Perguntas com respostas "Sim" e "Não"
- Exibição automática da solução final
- Barra de progresso, voltar e reiniciar fluxo
- Validação da planilha e mensagens de erro amigáveis
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
├── AcheaSaida.py          # Aplicação Flask e carregador dos fluxos
├── troubleshooting.xlsx   # Base de conhecimento
├── requirements.txt
│
└── Templates/
        ├── Index.html       # Seleção e busca de aplicações
        ├── flow.html        # Perguntas e soluções
        └── error.html       # Erros de navegação
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

Execute a partir de qualquer diretório:

```bash
python AcheaSaida.py
```

A aplicação ficará disponível em:

```
http://localhost:5000
```

O arquivo `troubleshooting.xlsx` é localizado automaticamente na mesma pasta de `AcheaSaida.py`. Abas vazias são ignoradas. Uma aba com referências inválidas é reportada na tela e não impede o carregamento das demais.

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

