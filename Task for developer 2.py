import sqlite3
con = sqlite3.connect("Rolls storage.db")
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, HttpUrl
import requests

rolls_storage = []

@app.route('/rolls', methods=['POST'])
def add_roll():
    data = request.get()
    roll = {
        'id': str(uuid.uuid4()),
        'length': data['length'],
        'weight': data['weight'],
        'date_added': datetime.now(),
        'date_removed': None
    }
    rolls_storage.append(roll)
    return jsonify(roll), 201

@app.route('/rolls/<roll_id>', methods=['DELETE'])
def remove_roll(roll_id):
    global rolls_storage
    roll = next((r for r in rolls_storage if r['id'] == roll_id), None)
    if roll:
        roll['date_removed'] = datetime.now()
        rolls_storage = [r for r in rolls_storage if r['id'] != roll_id]
        return (roll), 200
    else:
        return ({'message': 'Roll not found'}), 404

@app.route('/rolls', methods=['GET'])
def get_rolls():
    # Добавить фильтрацию по параметрам
    return (rolls_storage)

@app.route('/rolls/stats', methods=['GET'])
def get_stats():
    #  Логика для статистики
    pass

if __name__ == '__main__':
    app.run(debug=True)
    cur.execute("CREATE TABLE rolls (id, length, weight, date added, date removed)")
    def calculate_stats(start_date, end_date):
    addedrolls = [roll for roll in rolls_storage if start_date <= roll['date_added'] <= end_date]
    removed_rolls = [roll for roll in rolls_storage if roll['date_removed'] and start_date <= roll['date_removed'] <= end_date]

    total_added = len(added_rolls)
    total_removed = len(removed_rolls)

    # Средние значения
    average_length = sum(roll['length'] for roll in added_rolls) / total_added if total_added > 0 else 0
    average_weight = sum(roll['weight'] for roll in added_rolls) / total_added if total_added > 0 else 0

    # Максимальные и минимальные значения
    max_length = max(roll['length'] for roll in added_rolls) if added_rolls else 0
    min_length = min(roll['length'] for roll in added_rolls) if added_rolls else 0
    max_weight = max(roll['weight'] for roll in added_rolls) if added_rolls else 0
    min_weight = min(roll['weight'] for roll in added_rolls) if added_rolls else 0

    # Суммарный вес
    total_weight = sum(roll['weight'] for roll in added_rolls)

    # Промежутки между добавлением и удалением
    time_periods = [(roll['date_removed'] - roll['date_added']).total_seconds() for roll in rolls_storage if roll['date_removed']]
    max_time_period= max(time_periods) if time_periods else 0
    min_time_period = min(time_periods) if time_periods else 0

    return {
        'total_added': total_added,
        'total_removed': total_removed,
        'average_length': average_length,
        'average_weight': average_weight,
        'max_length': max_length,
        'min_length': min_length,
        'max_weight': max_weight,
        'min_weight': min_weight,
        'total_weight': total_weight,
        'max_time_period': max_time_period,
        'min_time_period': min_time_period,
    }

# Пример вызова функции
stats = calculate_stats(datetime(2024, 1, 1), datetime(2024, 5, 31))