# 📋 Unidraft — Sistema de Seletivas Esportivas

> **Um sistema completo para gerenciamento de seletivas esportivas com notificações por e-mail.**

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)
![Status](https://img.shields.io/badge/Status-Release%202%20-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 📚 Visão Geral

**Unidraft** é um sistema simples e modular desenvolvido em **Python puro** para:

- ✅ **Cadastro de usuários** (Atletas e Técnicos) com validações robustas
- ✅ **Seleção de esportes** no perfil do usuário
- ✅ **Criação e gerenciamento de seletivas** por técnicos
- ✅ **Inscrição e cancelamento** de atletas em seletivas
- ✅ **Notificações automáticas por e-mail** via SMTP (Gmail)
- ✅ **Persistência de dados** em JSON simples e inspecionável

---

## 🛠️ Arquitetura Técnica

### Bibliotecas Utilizadas

| Biblioteca | Tipo | Função | Justificativa |
|-----------|------|--------|---------------|
| `json` | stdlib | Leitura/escrita de dados | Persistência leve sem dependências externas; ideal para protótipos |
| `os` | stdlib | Verificação de arquivos | Gerenciar existência e caminhos de arquivos de dados |
| `re` | stdlib | Validação (email, senha) | Padrões regex para validar formato de email (UFRPE) e força de senha |
| `smtplib` | stdlib | Envio SMTP | Integração com Gmail para notificações automatizadas |
| `email.message` | stdlib | Composição de mensagens | Criar e-mails estruturados conforme RFC 5322 |

**Total de dependências externas (pip):** **0 (zero)**
> Projeto usa apenas a biblioteca padrão do Python — sem necessidade de `requirements.txt`.

---

## 🚀 Como Executar

### Requisitos

- **Python 3.8+** instalado
- Terminal ou PowerShell (Windows/Linux/macOS)

### Instalação e Execução

```powershell

cd c:\Users\adeil\Desktop\Estudos\Unidraft\Unidraft-master

python main.py
```

**Primeira execução:**
- Os arquivos `usuarios.json` e `seletivas.json` serão criados automaticamente
- Preencha cadastro com dados válidos:
  - Email: `nome.sobrenome@ufrpe.br`
  - Senha: mín. 6 caracteres, 1 maiúscula, 1 número, 1 especial

---

## 📦 Organização dos Módulos

```
Unidraft-master/
├── main.py                 # Ponto de entrada da aplicação
├── interface.py            # Utilidades de UI (limpeza, pausas)
├── usuario.py              # Modelo Usuario + GerenciadorUsuarios
├── cadastro.py             # Fluxo de registro com ValidadorDados
├── autenticacao.py         # Fluxo de login/autenticação
├── seletivasatleta.py      # Lógica principal: MenuTreinador, MenuAtleta
├── email_utils.py          # Funções de notificação por e-mail (novo!)
├── esportes.py             # Gerenciamento de modalidades
├── seletivas.json          # Persistência de seletivas
└── usuarios.json           # Persistência de usuários
```

### Detalhamento dos Módulos Principais

#### `seletivasatleta.py` — Núcleo do Sistema
- **`GerenciadorSeletivas`:** CRUD de seletivas persistidas em JSON
- **`MenuTreinador`:** 
  - Criar seletivas
  - Visualizar inscritos
  - **Cancelar seletivas** (notifica inscritos)
- **`MenuAtleta`:**
  - Ver seletivas disponíveis
  - Inscrever-se (recebe confirmação por e-mail ao técnico)
  - Cancelar inscrição (notifica técnico)

#### `email_utils.py` — Notificações Automáticas (Nova funcionalidade!)
```python
send_registration_email(treinador_email, atleta_email, seletiva)
send_cancellation_email(treinador_email, atleta_email, seletiva)
send_seletiva_canceled_email(lista_inscritos, seletiva)
```
- Usa **SMTP_SSL** porta 465 (Gmail)
- Credenciais: `unidraft2026@gmail.com` com senha de app

#### `cadastro.py` — Validação Robusta
- **`ValidadorDados`:**
  - Email: padrão UFRPE (`nome.sobrenome@ufrpe.br`)
  - Senha: mín 6 car., 1 maiúscula, 1 número, 1 especial ✨
  - Nome: 3–100 caracteres, apenas letras

---

## 💡 Funcionalidades de Inovação

### 1️⃣ Notificações por E-mail Integradas
- Automação entre técnicos e atletas **sem serviços pagos** (apenas Gmail)
- Notificações em tempo real ao:
  - Atleta se inscrever em uma seletiva
  - Atleta cancelar inscrição
  - Técnico cancelar uma seletiva (avisa todos inscritos)

### 2️⃣ Persistência JSON Simples
- Dados salvos em JSON legível → fácil debug e testes manuais
- IDs incrementais automáticos para rastreabilidade

### 3️⃣ Validação de Senha Forte
- Requisitos: maiúscula + número + caractere especial (mín. 6 car.)
- Previne senhas fracas e ataques simples

---

## 📅 Releases — Histórico de Evolução

### Release 1 — v1.0 (Início)
- ✅ CRUD completo de usuários
- ✅ Escolha de esporte/modalidade no perfil
- ✅ Persistência em `usuarios.json`

### Release 2 — v2.0 (Atual)
- ✅ Criação e visualização de seletivas
- ✅ Inscrição e cancelamento de inscrições
- ✅ Interface CLI limpa e intuitiva
- ✅ **Integração SMTP:** envio automático de e-mails
- ✅ Cancelamento de seletivas pelo técnico
- ✅ Validação de senha forte (maiúscula, número, especial)

### Release 3 — v3.0 (Planejado)
- 🎯 Atualização visual da interface (possível refactor para `curses` ou web)
- 🎯 Resultado/classificação de seletivas
- 🎯 **Tabela de rankings** mostrando classificação de cada atleta por modalidade

---

## ⚙️ Configuração para Envio de E-mail

### Pré-requisito: Conta Gmail com Senha de App

1. **Ativar 2FA** na conta Google
2. **Gerar Senha de App:**
   - Ir para: `https://myaccount.google.com/apppasswords`
   - Selecionar "Mail" e "Windows Computer"
   - Copiar a senha gerada

3. **Atualizar credenciais em `email_utils.py`:**
   ```python
   SENDER_EMAIL = "seu.email@gmail.com"
   SENDER_PASSWORD = "xxxx xxxx xxxx xxxx" 
   ```

**Alternativa (Recomendada em Produção):**
Usar variáveis de ambiente — veja seção **Segurança**.


## 🔒 Segurança & Observações

⚠️ **Prototipo — Não use em produção sem:**

1. **Mover credenciais para variáveis de ambiente:**
   ```python
   import os
   SENDER_EMAIL = os.getenv("UNIDRAFT_EMAIL")
   SENDER_PASSWORD = os.getenv("UNIDRAFT_PASSWORD")
   ```

2. **Hash de senhas:** Atualmente armazenadas em texto plano em JSON
   - Implementar: `bcrypt` ou `argon2` em produção

3. **Banco de dados:** Migrar JSON para SQLite/PostgreSQL
   - Permite consultas complexas (ranking, filtros)
   - Melhor performance com muitos registros

4. **Logging e monitoramento:** Adicionar `logging` estruturado
   - Rastrear tentativas de login/e-mail
   - Auditoria de ações de técnicos

---

## 🧪 Testando E-mail (Local)

```powershell
# 1. Executar a aplicação
python main.py

# 2. Crie uma conta (Técnico) com email de teste
# Exemplo: joao.silva@ufrpe.br

# 3. Crie uma seletiva (ID 1, Futebol, data 15/06/2026)

# 4. Em outra sessão/usuário, crie conta (Atleta)
# Exemplo: maria.oliveira@ufrpe.br

# 5. Inscreva-se na seletiva do técnico
# → Verifique se joao.silva@ufrpe.br recebeu e-mail ✉️

# 6. Cancele a inscrição
# → Novo e-mail de cancelamento ✉️
```

---

## 📖 Referências de Código

| Arquivo | Descrição | Ver |
|---------|-----------|-----|
| `seletivasatleta.py` | Lógica principal (CRUD + menus) | [Abrir](Unidraft-master/seletivasatleta.py) |
| `email_utils.py` | Notificações por e-mail | [Abrir](Unidraft-master/email_utils.py) |
| `cadastro.py` | Validação e cadastro de usuários | [Abrir](Unidraft-master/cadastro.py) |
| `usuario.py` | Modelo de dados e persistência | [Abrir](Unidraft-master/usuario.py) |

---

## 🚀 Próximos Passos (Roadmap)

| Prioridade | Tarefa | Release |
|------------|--------|---------|
| 🔴 Alto | Migrar para SQLite | v3.0 |
| 🔴 Alto | Hash de senhas (bcrypt) | v3.0 |
| 🟡 Médio | Variáveis de ambiente para credenciais | v2.1 |
| 🟡 Médio | Testes automatizados | v2.1 |
| 🟢 Baixo | Interface web (Flask/FastAPI) | v4.0 |
| 🟢 Baixo | Relatório de classificações em PDF | v3.0 |

---

## 📧 Contato & Suporte

Dúvidas ou sugestões? Abra uma issue no repositório ou contacte a equipe de desenvolvimento.

---

**Última atualização:** Junho 2026  
**Versão:** 2.0 (Release 2)  


