Claro! Aqui está o arquivo `README.md` atualizado para refletir as alterações no código, incluindo a troca do Twilio pela UltraMsg:

---

# 📢 CartolaFC AlertBot – Alerta de Fechamento do Mercado via WhatsApp

## 📌 Sobre o Projeto

O **CartolaFC AlertBot** é uma aplicação simples que envia um alerta via **WhatsApp** avisando quando o mercado do **Cartola FC** está prestes a fechar (faltando 1 hora).
Utiliza a **API oficial do Cartola**, o serviço de mensagens da **UltraMsg**, e é hospedado gratuitamente no **Render**, com **monitoramento periódico pelo UptimeRobot**.

---

## 🔎 Como Funciona

1. ⏱ A cada 5 minutos, o UptimeRobot acessa a rota `/verificar` da aplicação hospedada no Render.
2. 🧠 O servidor consulta o fechamento do mercado via API do Cartola.
3. 📲 Se estiver faltando 1 hora ou menos para o fechamento, uma mensagem é enviada por **WhatsApp** via **UltraMsg**.

---

## 🧰 Tecnologias Utilizadas

- **Python + Flask** – servidor web simples
- **UltraMsg API** – envio de mensagens via WhatsApp
- **UptimeRobot** – monitoramento automático (ping na API)
- **Render.com** – deploy gratuito da aplicação
- **requests** – requisições HTTP para API do Cartola
- **dotenv/os.environ** – uso de variáveis de ambiente para segurança

---

## 🚀 Como Utilizar

### ✅ Pré-requisitos:

- Conta na [UltraMsg](https://www.ultramsg.com/)
- Número verificado no **sandbox do UltraMsg WhatsApp**
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
INSTANCE_ID=xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
NUMERO_DESTINO=+55xxxxxxxxxxxx
PORT=5000
```

3. **Configure seu projeto no Render:**

   - Crie um novo serviço web no Render.
   - Conecte ao repositório GitHub.
   - No painel de variáveis de ambiente do Render, adicione:

     - `INSTANCE_ID`
     - `TOKEN`
     - `NUMERO_DESTINO`
     - `PORT` = `5000`

4. **Adicione o link da rota `/verificar` no UptimeRobot:**

   - Exemplo: `https://cartola-alerta.onrender.com/verificar`
   - Configure para checar a cada 5 minutos.

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

Agora o **Twilio** foi substituído pelo **UltraMsg**, como no seu código, e os passos estão atualizados para refletir isso.
