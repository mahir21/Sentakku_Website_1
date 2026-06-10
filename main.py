import gspread
import traceback
import json
import os
from google.oauth2.service_account import Credentials
from flask import Flask, render_template, request, flash, redirect, url_for, jsonify
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'change-this-secret-key')
CORS(app)

SPREADSHEET_ID = '14uRL-NBWBkilnJgKDeyFaj4_FO869ZgEyO5KPQ__Lv0'

SCOPES = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive',
]


def get_sheet():
    creds_json = os.environ.get('GOOGLE_CREDENTIALS_JSON')
    if creds_json:
        creds_dict = json.loads(creds_json)
        creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
        client = gspread.authorize(creds)
    else:
        client = gspread.service_account(filename='credentials.json')
    spreadsheet = client.open_by_key(SPREADSHEET_ID)
    return spreadsheet.sheet1


@app.route('/')
def index():
    return render_template('sentakku-portfolio.html')


@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip()
    phone = request.form.get('phone', '').strip()
    message = request.form.get('message', '').strip()

    if not name or not email:
        return jsonify({'error': 'Name and email are required.'}), 400

    try:
        sheet = get_sheet()
        if not sheet.row_values(1):
            sheet.append_row(['Timestamp', 'Name', 'Email', 'Phone', 'Message'])
        sheet.append_row([
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            name, email, phone, message
        ])
        return jsonify({'success': True}), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)
