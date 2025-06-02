function enviarAlerta() {
  fetch("/forcar-envio")
    .then((response) => response.text())
    .then((data) => {
      document.getElementById("resposta").innerText = data;
    });
}

function atualizarStatus() {
  fetch("/status")
    .then((response) => response.json())
    .then((data) => {
      document.getElementById("contador").innerText = data.contador;
      document.getElementById("horario_atual").innerText =
        data.horario_atual || "Indisponível";
      document.getElementById("fechamento").innerText =
        data.fechamento || "Indisponível";
      document.getElementById("dias_restantes").innerText =
        data.dias_restantes !== null ? data.dias_restantes : "Indisponível";
      document.getElementById("horario_previsto_1d").innerText =
        data.horario_previsto_1d || "Indisponível";
      document.getElementById("horario_previsto_1h").innerText =
        data.horario_previsto_1h || "Indisponível";
      document.getElementById("alerta_1d").innerText = data.alerta_1d
        ? "Sim"
        : "Não";
      document.getElementById("alerta_1h").innerText = data.alerta_1h
        ? "Sim"
        : "Não";
    });
}

setInterval(atualizarStatus, 10000);

atualizarStatus();
