document.addEventListener('DOMContentLoaded', function () {
  var map = L.map('map').setView([35.6762, 139.6503], 11);

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '© OpenStreetMap contributors'
  }).addTo(map);

  L.marker([35.6762, 139.6503]).addTo(map).bindPopup('🏯 Tóquio (Centro)').openPopup();

  L.circle([35.7, 139.8], {
    color: '#e74c3c',
    fillColor: '#e74c3c',
    fillOpacity: 0.15,
    radius: 35000
  }).addTo(map).bindPopup('⚠️ Zona de Alerta Máximo — Tufão Hagibis');

  L.circle([35.5, 139.5], {
    color: '#e67e22',
    fillColor: '#e67e22',
    fillOpacity: 0.15,
    radius: 25000
  }).addTo(map).bindPopup('🌊 Zona de Alerta de Inundação — Rios Arakawa e Sumida');

  L.circle([35.8, 139.7], {
    color: '#f1c40f',
    fillColor: '#f1c40f',
    fillOpacity: 0.1,
    radius: 15000
  }).addTo(map).bindPopup('📢 Atenção — Réplicas de terremoto monitoradas');

  var ctx1 = document.getElementById('tempChart').getContext('2d');
  new Chart(ctx1, {
    type: 'line',
    data: {
      labels: ['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb', 'Dom'],
      datasets: [{
        label: 'Temperatura (°C)',
        data: [22, 25, 27, 26, 24, 23, 28],
        borderColor: '#e67e22',
        backgroundColor: 'rgba(230, 126, 34, 0.1)',
        fill: true,
        tension: 0.4,
        pointBackgroundColor: '#f1c40f',
        pointBorderColor: '#f1c40f',
        borderWidth: 3
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { labels: { color: '#cfd8e6', font: { size: 12 } } }
      },
      scales: {
        x: { ticks: { color: '#8892a8' }, grid: { color: '#1a212e' } },
        y: { ticks: { color: '#8892a8', stepSize: 5 }, grid: { color: '#1a212e' } }
      }
    }
  });

  var ctx2 = document.getElementById('disasterChart').getContext('2d');
  new Chart(ctx2, {
    type: 'doughnut',
    data: {
      labels: ['Inundação', 'Terremoto', 'Tufão', 'Incêndio'],
      datasets: [{
        data: [45, 20, 70, 15],
        backgroundColor: ['#3498db', '#e74c3c', '#f1c40f', '#e67e22'],
        borderColor: '#12171f',
        borderWidth: 4
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { position: 'bottom', labels: { color: '#cfd8e6', padding: 15, font: { size: 12 } } }
      }
    }
  });

  const toggle = document.getElementById('chatbot-toggle');
  const body = document.getElementById('chatbot-body');
  let isOpen = true;

  toggle.addEventListener('click', () => {
    if (isOpen) {
      body.style.display = 'none';
      toggle.textContent = '+';
    } else {
      body.style.display = 'flex';
      toggle.textContent = '−';
    }
    isOpen = !isOpen;
  });

  const input = document.getElementById('chatbot-input');
  const send = document.getElementById('chatbot-send');
  const messages = document.getElementById('chatbot-messages');

  function addMessage(text, sender) {
    const div = document.createElement('div');
    div.classList.add('message', sender);
    div.textContent = text;
    messages.appendChild(div);
    messages.scrollTop = messages.scrollHeight;
  }

  function chatbotResponse(userText) {
    let response = 'Desculpe, não entendi. Pergunte sobre "tufão", "terremoto", "clima", "alerta" ou "evacuação".';
    const t = userText.toLowerCase();
    if (t.includes('tufão') || t.includes('tufao') || t.includes('hagibis')) {
      response = '⚠️ O tufão Hagibis está se aproximando rapidamente! Ventos de até 150 km/h são esperados. Recomendações:\n1. Evacue áreas costeiras.\n2. Mantenha-se em abrigos seguros.\n3. Tenha água e alimentos não perecíveis.';
    } else if (t.includes('terremoto') || t.includes('abalo') || t.includes('sísmico')) {
      response = '📢 Último boletim sísmico: Magnitude 3.2 em Chiba. Nenhum dano estrutural reportado. A rede de monitoramento está ativa 24h.';
    } else if (t.includes('clima') || t.includes('temperatura') || t.includes('chuva')) {
      response = '🌤️ Clima atual em Tóquio: 26°C, parcialmente nublado. Previsão de chuva forte para as próximas horas devido à aproximação do tufão.';
    } else if (t.includes('alerta') || t.includes('perigo')) {
      response = '🚨 Alertas ativos:\n• Tufão Hagibis (Vermelho)\n• Inundação em Sumida e Edogawa (Laranja)\n• Ventos fortes (Amarelo)\nAcompanhe as autoridades locais.';
    } else if (t.includes('evacuação') || t.includes('rota') || t.includes('abrigo')) {
      response = '🗺️ Rotas de evacuação disponíveis:\n• Abrigo 1: Escola Primária de Sumida (Leste)\n• Abrigo 2: Ginásio de Edogawa (Oeste)\n• Abrigo 3: Centro Comunitário de Chuo (Sul)\nSiga as sinalizações e orientações da polícia.';
    } else if (t.includes('obrigado') || t.includes('valeu')) {
      response = '😊 De nada! Estou aqui para ajudar. Permaneça seguro e siga as instruções das autoridades.';
    }
    return response;
  }

  send.addEventListener('click', () => {
    const text = input.value.trim();
    if (text === '') return;
    addMessage(text, 'user');
    input.value = '';
    setTimeout(() => {
      const response = chatbotResponse(text);
      addMessage(response, 'bot');
    }, 600);
  });

  input.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
      send.click();
    }
  });
});