const monthNames = [
  "Январь",
  "Февраль",
  "Март",
  "Апрель",
  "Май",
  "Июнь",
  "Июль",
  "Август",
  "Сентябрь",
  "Октябрь",
  "Ноябрь",
  "Декабрь"
];

const dayClasses = [
  "mon",
  "tue",
  "wed",
  "thu",
  "fri",
  "sat",
  "sun"
];

function renderCalendar() {
  const now = new Date();

  const year = now.getFullYear();
  const month = now.getMonth();
  const today = now.getDate();

  const firstDay = new Date(year, month, 1);
  const daysInMonth = new Date(year, month + 1, 0).getDate();

  // В JavaScript воскресенье = 0.
  // Здесь мы делаем так, чтобы первым днём был понедельник.
  const startOffset = (firstDay.getDay() + 6) % 7;

  let cells = [];

  // Пустые ячейки до первого числа месяца
  for (let i = 0; i < startOffset; i++) {
    cells.push('<td class="noday"></td>');
  }

  // Дни месяца
  for (let day = 1; day <= daysInMonth; day++) {
    const date = new Date(year, month, day);
    const weekday = (date.getDay() + 6) % 7;

    let className = dayClasses[weekday];

    // Подсветка сегодняшнего дня
    if (day === today) {
      className += " today";
    }

    cells.push(`<td class="${className}">${day}</td>`);
  }

  // Заполняем пустые ячейки после последнего числа месяца,
  // чтобы таблица была кратна 7 дням
  while (cells.length % 7 !== 0) {
    cells.push('<td class="noday"></td>');
  }

  // Собираем строки по 7 ячеек
  let rows = "";

  for (let i = 0; i < cells.length; i += 7) {
    rows += `<tr>${cells.slice(i, i + 7).join("")}</tr>`;
  }

  document.getElementById("calendar").innerHTML = `
    <table class="calendar">
      <tr>
        <th colspan="7" class="month">
          ${monthNames[month]} ${year}
        </th>
      </tr>

      <tr>
        <th>Пн</th>
        <th>Вт</th>
        <th>Ср</th>
        <th>Чт</th>
        <th>Пт</th>
        <th>Сб</th>
        <th>Вс</th>
      </tr>

      ${rows}
    </table>
  `;
}

// Показываем календарь сразу
renderCalendar();

// Обновляем календарь ровно в 00:00
function scheduleNextMidnightUpdate() {
  const now = new Date();

  const nextMidnight = new Date(
    now.getFullYear(),
    now.getMonth(),
    now.getDate() + 1,
    0,
    0,
    0,
    0
  );

  const delay = nextMidnight.getTime() - now.getTime();

  setTimeout(() => {
    renderCalendar();
    scheduleNextMidnightUpdate();
  }, delay);
}

scheduleNextMidnightUpdate();