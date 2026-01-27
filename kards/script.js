document.addEventListener('DOMContentLoaded', () => {

  const softwareData = [
    { name: 'Windows 11', type: 'System Software' },
    { name: 'Windows 10', type: 'System Software' },
    { name: 'Linux', type: 'System Software' },
    { name: 'Ubuntu', type: 'System Software' },
    { name: 'macOS', type: 'System Software' },
    { name: 'Android OS', type: 'System Software' },
    { name: 'iOS', type: 'System Software' },
    { name: 'BIOS', type: 'System Software' },
    { name: 'UEFI', type: 'System Software' },
    { name: 'MS-DOS', type: 'System Software' },
    { name: 'Chrome OS', type: 'System Software' },
    { name: 'FreeBSD', type: 'System Software' },
    { name: 'Debian', type: 'System Software' },
    { name: 'Fedora', type: 'System Software' },
    { name: 'CentOS', type: 'System Software' },
    { name: 'Unix', type: 'System Software' },
    { name: 'Solaris', type: 'System Software' },
    { name: 'Red Hat Enterprise Linux', type: 'System Software' },
    { name: 'Windows Server', type: 'System Software' },
    { name: 'VMware ESXi', type: 'System Software' },
    { name: 'Microsoft Word', type: 'Application Software' },
    { name: 'Microsoft Excel', type: 'Application Software' },
    { name: 'Microsoft PowerPoint', type: 'Application Software' },
    { name: 'Adobe Photoshop', type: 'Application Software' },
    { name: 'Adobe Illustrator', type: 'Application Software' },
    { name: 'Adobe Premiere Pro', type: 'Application Software' },
    { name: 'Google Chrome', type: 'Application Software' },
    { name: 'Mozilla Firefox', type: 'Application Software' },
    { name: 'Visual Studio Code', type: 'Application Software' },
    { name: 'IntelliJ IDEA', type: 'Application Software' },
    { name: 'PyCharm', type: 'Application Software' },
    { name: 'Notepad++', type: 'Application Software' },
    { name: 'Slack', type: 'Application Software' },
    { name: 'Discord', type: 'Application Software' },
    { name: 'Zoom', type: 'Application Software' },
    { name: 'Skype', type: 'Application Software' },
    { name: 'Telegram', type: 'Application Software' },
    { name: 'WhatsApp', type: 'Application Software' },
    { name: 'Spotify', type: 'Application Software' },
    { name: 'VLC Media Player', type: 'Application Software' },
    { name: 'AutoCAD', type: 'Application Software' },
    { name: 'Blender', type: 'Application Software' },
    { name: 'Figma', type: 'Application Software' },
    { name: 'CorelDRAW', type: 'Application Software' },
    { name: 'WinRAR', type: 'Application Software' },
    { name: '7-Zip', type: 'Application Software' },
    { name: 'Steam', type: 'Application Software' },
    { name: 'OBS Studio', type: 'Application Software' },
    { name: 'Microsoft Access', type: 'Application Software' },
    { name: 'Google Docs', type: 'Application Software' }
];

  const learnContainer = document.getElementById('card-container');
  const learnedContainer = document.getElementById('learned-cards'); // Новая область для изученных
  const startTestBtn = document.getElementById('start-test-btn');
  const testArea = document.getElementById('test-area');
  const sourceCardsContainer = document.getElementById('source-cards');
  const dropZones = document.querySelectorAll('.drop-zone');
  const checkBtn = document.getElementById('check-btn');
  const resultsContainer = document.getElementById('results');
  const shuffleBtn = document.getElementById('shuffle-btn');

  // Массив изученных карточек
  let learnedCards = JSON.parse(localStorage.getItem('learnedCards')) || [];

  function createLearningCards() {
    learnContainer.innerHTML = '';
    learnedContainer.innerHTML = ''; // Очистка области изученных карточек

    softwareData.forEach(item => {
      const card = document.createElement('div');
      card.classList.add('card');
      card.innerHTML = `
        <div class="card-face card-front">${item.name}</div>
        <div class="card-face card-back">
          <h3>${item.type}</h3>
          <button class="mark-learned-btn">Изучено</button>
        </div>
      `;
      card.addEventListener('click', () => card.classList.toggle('is-flipped'));

      const markBtn = card.querySelector('.mark-learned-btn');

      markBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        if (!learnedCards.includes(item.name)) learnedCards.push(item.name);
        localStorage.setItem('learnedCards', JSON.stringify(learnedCards));
        moveToLearned(card);
      });

      // Если карточка уже изучена, сразу помещаем её в область изученных
      if (learnedCards.includes(item.name)) {
        moveToLearned(card);
      } else {
        learnContainer.appendChild(card);
      }
    });
  }

  // Перемещаем карточку в область изученных
  function moveToLearned(card) {
    const returnBtn = document.createElement('button');
    returnBtn.textContent = 'Вернуть';
    returnBtn.classList.add('return-btn');
    returnBtn.addEventListener('click', () => {
      learnedCards = learnedCards.filter(name => name !== card.querySelector('.card-front').textContent);
      localStorage.setItem('learnedCards', JSON.stringify(learnedCards));
      returnToLearn(card);
    });

    // Убираем старую кнопку "Изучено"
    const oldBtn = card.querySelector('.mark-learned-btn');
    if (oldBtn) oldBtn.remove();

    card.querySelector('.card-back').appendChild(returnBtn);
    learnedContainer.appendChild(card);
    card.classList.remove('is-flipped');
  }

  // Возвращаем карточку обратно в обучение
  function returnToLearn(card) {
  // Удаляем кнопку "Вернуть"
  const returnBtn = card.querySelector('.return-btn');
  if (returnBtn) returnBtn.remove();

  // Создаём кнопку "Изучено" заново
  const markBtn = document.createElement('button');
  markBtn.textContent = 'Изучено';
  markBtn.classList.add('mark-learned-btn');
  markBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    const name = card.querySelector('.card-front').textContent;
    moveToLearned(card, name);
  });

  // Добавляем на обратную сторону карточки
  card.querySelector('.card-back').appendChild(markBtn);

  // Перемещаем карточку обратно в обучающие
  learnContainer.appendChild(card);
}

  function initializeTest() {
  learnContainer.classList.add('hidden');
  startTestBtn.classList.add('hidden');
  testArea.classList.remove('hidden');
  shuffleBtn.classList.remove('hidden');

  sourceCardsContainer.innerHTML = '';
  resultsContainer.innerHTML = '';
  checkBtn.classList.add('hidden');
  dropZones.forEach(zone => zone.innerHTML = `<h3>${zone.dataset.type}</h3>`);

  // Фильтруем изученные карточки
  const availableCards = softwareData.filter(item => !learnedCards.includes(item.name));

  // Берём случайные 20 карточек
  const shuffledData = availableCards.sort(() => Math.random() - 0.5).slice(0, 20);

  // Создаём перетаскиваемые карточки
  shuffledData.forEach((item, index) => {
    const card = document.createElement('div');
    card.id = `card-${index}`;
    card.classList.add('card');
    card.draggable = true;
    card.textContent = item.name;
    card.dataset.type = item.type;
    sourceCardsContainer.appendChild(card);
  });

  addDragAndDropListeners();
}


  function addDragAndDropListeners() {
    const draggableCards = document.querySelectorAll('#source-cards .card');
    draggableCards.forEach(card => {
      card.addEventListener('dragstart', e => {
        e.dataTransfer.setData('text/plain', e.target.id);
        setTimeout(() => card.classList.add('hidden'), 0);
      });
      card.addEventListener('dragend', () => card.classList.remove('hidden'));
    });
  }

  dropZones.forEach(zone => {
    zone.addEventListener('dragover', e => { e.preventDefault(); zone.classList.add('drag-over'); });
    zone.addEventListener('dragleave', () => zone.classList.remove('drag-over'));
    zone.addEventListener('drop', e => {
      e.preventDefault();
      zone.classList.remove('drag-over');
      const id = e.dataTransfer.getData('text/plain');
      const draggable = document.getElementById(id);
      if (draggable) zone.appendChild(draggable);
      checkTestCompletion();
    });
  });

  function checkTestCompletion() {
    if (sourceCardsContainer.children.length === 0) checkBtn.classList.remove('hidden');
  }

  function calculateResults() {
    let correctAnswers = 0;
    let incorrectAnswers = 0;

    dropZones.forEach(zone => {
      const zoneType = zone.dataset.type;
      const cardsInZone = zone.querySelectorAll('.card');

      cardsInZone.forEach(card => {
        card.draggable = false;
        card.style.cursor = 'default';
        if (card.dataset.type === zoneType) {
          correctAnswers++;
          card.classList.add('correct');
        } else {
          incorrectAnswers++;
          card.classList.add('incorrect');
        }
      });
    });

    resultsContainer.textContent = `Правильно: ${correctAnswers}, Ошибочно: ${incorrectAnswers}`;
    checkBtn.classList.add('hidden');
    shuffleBtn.classList.add('hidden');
  }

  function shuffleCards() {
    const cards = Array.from(sourceCardsContainer.children);
    const shuffled = cards.sort(() => Math.random() - 0.5);
    sourceCardsContainer.innerHTML = '';
    shuffled.forEach(card => sourceCardsContainer.appendChild(card));
  }

  // --- инициализация ---
  createLearningCards();
  startTestBtn.addEventListener('click', initializeTest);
  checkBtn.addEventListener('click', calculateResults);
  shuffleBtn.addEventListener('click', shuffleCards);

});
