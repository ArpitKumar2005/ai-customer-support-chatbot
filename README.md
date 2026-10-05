# AI Customer Support Chatbot

A simple customer support chatbot built with **Python, NLP basics and Flask**.
It answers frequently asked questions about orders, shipping, refunds, payments and more.

## Features
- Text preprocessing (lowercase, remove symbols, stop words removal, simple stemming)
- Keyword-based intent matching
- Intent-response system with fallback handling for unknown questions
- FAQ data stored in `intents.json`, so it is easy to maintain
- Flask web chat interface
- Conversation handling (remembers chat history, suggests human support after repeated failures)
- Input and response validation

## Technologies Used
- Python 3
- Flask
- HTML, CSS, JavaScript

## How to Run
1. Install Python from python.org
2. Open the project folder in VS Code terminal
3. Install Flask:
   ```
   pip install -r requirements.txt
   ```
4. Start the app:
   ```
   python app.py
   ```
5. Open `http://127.0.0.1:5000` in your browser

## Project Structure
```
ai-chatbot/
├── app.py            # Flask server and routes
├── chatbot.py        # Chatbot logic (preprocessing, intent matching)
├── intents.json      # FAQ data
├── requirements.txt
├── templates/
│   └── index.html
└── static/
    ├── style.css
    └── script.js
```

## How to Add a New Question
Add a new block in `intents.json` with a `tag`, `keywords` and `responses`.

## Author
Arpit Kumar
