from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import calendar
from models import Task, DiaryEntry

app = Flask(__name__)
# Настраиваем базу данных SQLite (файл будет в корне проекта)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
# Отключаем отслеживание изменений объектов (экономит ресурсы, не нужно на старте)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
# Функция генерирует HTML-календарь для указанного года и месяца
def generate_calendat_html(year=2026, month=3):
    cal = calendar.monthcalendar(year, month)

    #Заголовок месяца и года
    month_name = calendar.month_name[month]
    header = f"<h2>{month_name} {year}</h2>"

    #Таблица календаря
    html = '<table class="calendar">'
    html += '<thead><tr><th>Пн</th><th>Вт</th><th>Ср</th><th>Чт</th><th>Пт</th><th>Сб</th><th>Вс</th></tr></thead>'
    html += '<tbody>'

    for week in cal:
        html += '<tr>'
        for day in week:
            if day == 0:
                html += '<td class="empty"></td>' # Пустые клетки до/после месяца
            else:
                # Формируем дату в формате YYYY-MM-DD
                date_str = f"{year}-{month:02d}-{day:02d}"
                # Ссылка на страницу дня
                html += f'<td><a href="/day/{date_str}">{day}</a></td>'
        html += '</tr>'
    html += '</tbody></table>'

    return header + html


@app.route('/')
def home():
    calendar_html = generate_calendat_html(2026, 3)
    return render_template('index.html', calendar_html=calendar_html)

# Маршрут страницы конкретного дня
@app.route('/day/<date>')
def day_detail(date):
    # Запрашиваем все задачи для этой даты
    tasks= Task.query.filter(Task.date == date).all()

    # date приходит как строка '2026-03-05'
    return render_template(
        'day.html',
        date=date,
        tasks=tasks)

if __name__ == '__main__':
    # Перед первым запуском создаём таблицы (только один раз!)
    with app.app_context():
        db.create_all()

    app.run(debug=True)