from app import db
from datetime import datetime

class Task(db.Model):
    """Таблица задач - одна запись = одна задача на определенный день"""
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(50), nullable=False)
    text = db.Column(db.String(200), nullable=False)
    done = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Task "{self.id}" ({self.date})>'

class DiaryEntry(db.Model):
    """Таблица дневника - одна запись один день (заметки)"""
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(50), nullable=False, unique=True)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<DiaryEntry {self.date}>'
