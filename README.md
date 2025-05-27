---
# 📢 CartolaFC AlertBot – Alerta de Fechamento do Mercado via WhatsApp

## 📌 Sobre o Projeto

O **CartolaFC AlertBot** é uma aplicação simples que envia um alerta via **WhatsApp** avisando quando o mercado do **Cartola FC** está prestes a fechar (faltando 1 hora).
Utiliza a **API oficial do Cartola**, o serviço de mensagens da **Twilio**, e é hospedado gratuitamente no **Render**, com **monitoramento periódico pelo UptimeRobot**.
---

## 🔎 Como Funciona

1. ⏱ A cada 5 minutos, o UptimeRobot acessa a rota da aplicação hospedada no Render.
2. 🧠 O servidor consulta o fechamento do mercado via API do Cartola.
3. 📲 Se estiver faltando 1 hora ou menos para o fechamento, uma mensagem é enviada por **WhatsApp** via **Twilio**.

---

## 🧰 Tecnologias Utilizadas

- **Python + Flask** – servidor web simples
- **Twilio** – envio de mensagens via WhatsApp
- **UptimeRobot** – monitoramento automático (ping na API)
- **Render.com** – deploy gratuito da aplicação
- **requests** – requisições HTTP para API do Cartola
- **dotenv/os.environ** – uso de variáveis de ambiente para segurança

---

## 🚀 Como Utilizar

### ✅ Pré-requisitos:

- Conta na [Twilio](https://www.twilio.com/)
- Número verificado no **sandbox do Twilio WhatsApp**
- Conta no [Render](https://render.com/)
- Conta no [UptimeRobot](https://uptimerobot.com/)
- Git instalado

---

### 🛠️ Passo a Passo

1. **Clone o repositório:**

```bash
git clone https://github.com/henrique151/CartolaFC.git
```

2. **Crie um arquivo `.env` com suas credenciais:**

```env
NUMERO_DESTINO=xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_SID=xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
PORT=5000
```

3. **Configure seu projeto no Render:**

   - Crie um novo serviço web no Render.
   - Conecte ao repositório GitHub.
   - No painel de variáveis de ambiente do Render, adicione:

     - `TWILIO_SID`
     - `TWILIO_AUTH_TOKEN`
     - `NUMERO_DESTINO`
     - `PORT` = `5000`

---

## 📞 Exemplo de Alerta no WhatsApp:

```
🚨 O mercado do Cartola FC fecha em 1 hora! Faça seu time!
```

---

## 🤝 Contribuições

Sinta-se livre para abrir issues ou pull requests. Melhorias são sempre bem-vindas! ⚽

---

## 📄 Licença

Este projeto está sob a licença [MIT](LICENSE).

---
