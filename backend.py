from flask import Flask, request, jsonify
from datetime import datetime
import pandas as pd
import os

app = Flask(__name__)

# Pfad zur CSV-Datei
data_file = 'anwesende.csv'

@app.route('/add', methods=['POST'])
def add_attendance():
    data = request.get_json()
    name = data.get('name')
    company = data.get('company')
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Daten speichern
    new_entry = pd.DataFrame([[name, company, timestamp]], columns=['Name', 'Firma', 'Zeitstempel'])

    if os.path.exists(data_file):
        df = pd.read_csv(data_file)
        df = pd.concat([df, new_entry], ignore_index=True)
    else:
        df = new_entry

    df.to_csv(data_file, index=False)

    return jsonify({'status': 'success'}), 200

if __name__ == '__main__':
    app.run(port=5000)
