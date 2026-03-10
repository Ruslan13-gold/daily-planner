from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import calendar
from extensions import db
from models import Task, DiaryEntry

app = Flask(__name__)
# Настраиваем базу данных SQLite (файл будет в корне проекта)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
# Отключаем отслеживание изменений объектов (экономит ресурсы, не нужно на старте)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

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
@app.route('/day/<date>', methods=['GET', 'POST'])
def day_detail(date):
    if request.method == 'POST':
        # Получаем текст из формы
        task_text = request.form.get('text', '').strip()

        if task_text: # проверяем, что не пустая строка
            new_task = Task(
                date=date,
                text=task_text.strip(),
                done = False
            )
            db.session.add(new_task)
            db.session.commit()
            # После сохранения — редирект на ту же страницу (чтобы избежать повторной отправки формы)
            return redirect(url_for('day_detail', date=date))
        else:
            # Можно добавить flash-сообщение об ошибке (позже)
            print("Попытка добавить пустую задачу — игнорируем")

    # GET-запрос или после редиректа — показываем страницу
    tasks = Task.query.filter_by(date=date).all()
    return render_template(
        'day.html',
        tasks=tasks,
        date=date
    )

@app.route('/toggle/<int:task_id>', methods = ['POST'])
def toggle_task(task_id):
    """
    Переключает статус задачи (выполнена / не выполнена).
    Используется для чекбокса.
    """
    # Находим задачу по ID или возвращаем 404, если не найдена
    task = Task.query.get_or_404(task_id)

    task.done = not task.done

    db.session.commit()

    # Возвращаем JSON-ответ для фронтенда
    return {
        'success': True,
        'task_id': task.id,
        'done': task.done
    }, 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)