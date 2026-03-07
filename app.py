from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# Настраиваем базу данных SQLite (файл будет в корне проекта)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
# Отключаем отслеживание изменений объектов (экономит ресурсы, не нужно на старте)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    # Перед первым запуском создаём таблицы (только один раз!)
    with app.app_context():
        print("Таблицы созданы. Пример запроса:")
        print(Task.query.all())  # Должно вывести []
        db.create_all()

    app.run(debug=True)