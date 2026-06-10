

# Consultation Form → Google Sheets

## What Was Built

A web application where users fill out a consultation form (name, email, phone, message) and their details are automatically saved as a new row in a Google Sheet.

**Stack:**
- Python + Flask (web server)
- gspread (Google Sheets API client)
- Google Service Account (authentication)
- HTML/CSS (frontend form)

**Files created:**
- `main.py` — Flask server with form handling and Google Sheets integration
- `templates/index.html` — Consultation form UI
- `credentials.json` — Google service account key (downloaded from Google Cloud)

---

## Setup Steps

1. Created a Google Cloud project and enabled the **Google Sheets API** and **Google Drive API**
2. Created a **service account** (`id-form-submissions@license-478215.iam.gserviceaccount.com`)
3. Downloaded the service account JSON key → saved as `credentials.json` in the project folder
4. Created a Google Sheet and shared it with the service account email as **Editor**
5. Installed dependencies: `pip install flask gspread google-auth`

---

## Errors Encountered & Fixes

### 1. Flask not installed
**Error:** `ModuleNotFoundError: No module named 'flask'`
**Fix:** Ran `pip install flask gspread google-auth`

---

### 2. Chrome blocked localhost
**Error:** `Access to localhost was denied — HTTP ERROR 403`
**Fix:** Used `127.0.0.1:5000` in the browser address bar instead of `localhost:5000`

---

### 3. Insufficient authentication scopes
**Error:** `APIError: [403]: Request had insufficient authentication scopes`
**Cause:** Only the Sheets API scope was included — opening a sheet by name also requires the Drive API scope.
**Fix:** Added `https://www.googleapis.com/auth/drive` to the scopes list. Also enabled the Drive API in Google Cloud Console.

---

### 4. Wrong gspread authentication method
**Error:** `Something went wrong: <Response [200]>`
**Cause:** Used the old `gspread.authorize()` method which is deprecated in gspread 6.x.
**Fix:** Switched to `gspread.service_account(filename='credentials.json')`

---

### 5. Spreadsheet not found
**Error:** `gspread.exceptions.SpreadsheetNotFound`
**Cause:** `client.open()` searches by name using the Drive API, and the sheet name either didn't match exactly or wasn't accessible.
**Fix:** Used `client.open_by_key(SPREADSHEET_ID)` with the spreadsheet ID extracted directly from the sheet URL.

---

### 6. Service account permission denied
**Error:** `PermissionError: [403]: The caller does not have permission`
**Cause:** The Google Sheet was not shared with the service account email.
**Fix:** Shared the Google Sheet with `id-form-submissions@license-478215.iam.gserviceaccount.com` as **Editor**.

---

## How It Works (Final Flow)

1. User visits `http://127.0.0.1:5000` in the browser
2. Fills out the consultation form and clicks **Request Consultation**
3. Flask receives the form data and calls the Google Sheets API
4. A new row is appended to the Google Sheet with timestamp, name, email, phone, and message
5. User sees a success message on the page
