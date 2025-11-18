## Language Translator

A modern, browser-based language translator that converts text from Indian languages (Tamil, Hindi, Telugu) to English using neural machine translation APIs, wrapped in a clean Gradio UI.

### Features

- **Indian → English translation**: Supports Tamil, Hindi, and Telugu as source languages.
- **Simple web UI**: Clean two-column layout with input and translation panels.
- **API-based translation**: Uses `deep-translator` (Google Translate under the hood).
- **Auto port selection**: Falls back to a free port if `7860` is already in use.
- **Windows-friendly output**: Handles Unicode console output gracefully.

---

## Project Structure

- **`web_app.py`**: Main Gradio web interface and application entrypoint.
- **`src/api_translator.py`**: API-based translation backend using `GoogleTranslator`.
- **`src/utils.py`**: Utility helpers (language names, validation, etc.).
- **`requirements.txt`**: Python dependencies for running the app.

---

## Requirements

- **Python**: 3.10 or later is recommended.
- **OS**: Windows, macOS, or Linux.
- **Internet access**: Required for calling the translation API.

Python packages are managed via `requirements.txt` and include:

- `gradio`
- `deep-translator`
- `langdetect`
- `requests`
- `pyyaml`
- `fastapi` (indirect dependency for Gradio)

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/Praveenjeya77/Language_translator.git
cd Language_translator
```

### 2. (Optional but recommended) Create a virtual environment

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

If you are using Python 3.13 and hit an `audioop`-related error (from `pydub` / Gradio), install:

```bash
pip install audioop-lts
```

---

## Running the App

From the project root:

```bash
python web_app.py
```

What happens:

- The backend translator and Gradio UI are initialized.
- The app tries to use port `7860`. If it is already in use, it will automatically pick a free port and print it in the terminal.
- Your default browser will open automatically; if not, copy the printed `http://localhost:PORT` URL into your browser.

---

## Using the Web Interface

1. **Choose source language**: Tamil, Hindi, or Telugu.
2. **Enter text**: Type or paste the text you want to translate.
3. **Click “⚡ Translate Now”**: The translated English text appears in the right-hand panel.
4. **Click “🧹 Clear Text”** to reset the input and output fields.

---

## Notes and Limitations

- **Accuracy**: Depends on the underlying Google Translate models (`deep-translator`).
- **Rate limits**: Heavy usage may be subject to upstream API limits or throttling.
- **Offline use**: Not supported; translation requires internet access.

---

## Extending the Project

Some ideas for future enhancements:

- **Add more languages**: Extend `LANGUAGE_MAP` in `src/api_translator.py`.
- **Model-based translation**: Integrate transformer models (e.g. MarianMT) for offline or custom translation.
- **History & export**: Save translated pairs to a file for later reference.

---

## License

This project is for educational and personal-use purposes. Add a license section here if you intend to open-source or distribute it.


