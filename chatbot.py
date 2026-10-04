import json
import random
import re

# Words that do not help in finding the intent, so we remove them
STOP_WORDS = {"is", "am", "are", "the", "a", "an", "to", "of", "in", "on",
              "my", "i", "me", "you", "your", "do", "does", "can", "how",
              "what", "please", "it", "for", "and", "or", "be", "will"}

MAX_LENGTH = 200


def load_intents(path="intents.json"):
    """Read the FAQ data from the JSON file."""
    with open(path, encoding="utf-8") as file:
        return json.load(file)


def simple_stem(word):
    """Very small stemmer: 'orders' -> 'order', 'refunds' -> 'refund'."""
    if len(word) > 3 and word.endswith("s"):
        return word[:-1]
    return word


def preprocess(text):
    """Text preprocessing: lowercase -> remove symbols -> split -> remove stop words -> stem."""
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", "", text)
    words = text.split()
    words = [w for w in words if w not in STOP_WORDS]
    return [simple_stem(w) for w in words]


def validate_message(message):
    """Input validation. Returns (True, '') if ok, else (False, error message)."""
    if not message or not message.strip():
        return False, "Please type a message."
    if len(message) > MAX_LENGTH:
        return False, "Message is too long. Please keep it under 200 characters."
    return True, ""


def find_intent(words, data):
    """Keyword based intent matching: the intent with most matching keywords wins."""
    best_intent = None
    best_score = 0

    for intent in data["intents"]:
        keywords = [simple_stem(k) for k in intent["keywords"]]
        score = 0
        for word in words:
            if word in keywords:
                score += 1
        if score > best_score:
            best_score = score
            best_intent = intent

    return best_intent  # None if nothing matched


def validate_response(response):
    """Response validation: never send an empty reply."""
    if not response or not response.strip():
        return "Sorry, something went wrong. Please try again."
    return response


def get_response(message, data):
    """Returns (reply, tag). tag is 'fallback' when the bot does not know."""
    words = preprocess(message)
    intent = find_intent(words, data)

    if intent is None:
        reply = random.choice(data["fallback"])
        return validate_response(reply), "fallback"

    reply = random.choice(intent["responses"])
    return validate_response(reply), intent["tag"]


# Run this file directly to test the bot in the terminal
if __name__ == "__main__":
    data = load_intents()
    print("Bot: Hi! Type 'bye' to exit.")
    while True:
        user = input("You: ")
        ok, error = validate_message(user)
        if not ok:
            print("Bot:", error)
            continue
        reply, tag = get_response(user, data)
        print("Bot:", reply)
        if tag == "goodbye":
            break
