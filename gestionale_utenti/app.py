from datetime import datetime
import json
import os
import re

from flask import Flask, jsonify, render_template, request


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "users.json")

ID_REGEX = re.compile(r"^\d+$")
NAME_REGEX = re.compile(r"^[A-Za-zÀ-ÖØ-öø-ÿ' -]{2,40}$")
DATE_REGEX = re.compile(r"^\d{4}-\d{2}-\d{2}$")

app = Flask(
    __name__,
    static_url_path="/gestionale_utenti/static",
    template_folder="templates",
    static_folder="static",
)


def ensure_data_file():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as data_file:
            json.dump([], data_file)


def load_users():
    ensure_data_file()
    with open(DATA_FILE, "r") as data_file:
        try:
            users = json.load(data_file)
        except ValueError:
            users = []
    if not isinstance(users, list):
        return []
    return users


def save_users(users):
    with open(DATA_FILE, "w") as data_file:
        json.dump(users, data_file, indent=2, ensure_ascii=False)


def validate_user_payload(payload, require_all_fields=True):
    if not isinstance(payload, dict):
        return False, "Richiesta JSON non valida"

    required_fields = ["nome", "cognome", "data_nascita", "mansione"]
    if require_all_fields:
        for field in required_fields:
            if field not in payload:
                return False, "Campi mancanti"

    nome = str(payload.get("nome", "")).strip()
    cognome = str(payload.get("cognome", "")).strip()
    data_nascita = str(payload.get("data_nascita", "")).strip()
    mansione = str(payload.get("mansione", "")).strip()

    if not NAME_REGEX.match(nome):
        return False, "Nome non valido"
    if not NAME_REGEX.match(cognome):
        return False, "Cognome non valido"
    if not NAME_REGEX.match(mansione):
        return False, "Mansione non valida"
    if not DATE_REGEX.match(data_nascita):
        return False, "Data di nascita non valida"

    try:
        datetime.strptime(data_nascita, "%Y-%m-%d")
    except ValueError:
        return False, "Data di nascita non valida"

    return True, ""


def next_user_id(users):
    if not users:
        return 1
    max_id = 0
    for user in users:
        try:
            current_id = int(user.get("id", 0))
        except (TypeError, ValueError):
            current_id = 0
        if current_id > max_id:
            max_id = current_id
    return max_id + 1


def json_error(message, status_code):
    response = jsonify({"error": message})
    response.status_code = status_code
    return response


@app.route("/gestionale_utenti/")
@app.route("/gestionale_utenti")
def home():
    return render_template("index.html")


@app.route("/gestionale_utenti/users/", methods=["GET", "POST"])
def users_collection():
    if request.method == "GET":
        users = load_users()
        search = request.args.get("q", "").strip().lower()
        if search:
            users = [
                user for user in users
                if search in str(user.get("nome", "")).lower()
                or search in str(user.get("cognome", "")).lower()
                or search in str(user.get("mansione", "")).lower()
            ]
        response = jsonify({"users": users})
        response.status_code = 200
        return response

    payload = request.get_json(silent=True)
    is_valid, error_message = validate_user_payload(payload)
    if not is_valid:
        return json_error(error_message, 400)

    users = load_users()
    new_user = {
        "id": next_user_id(users),
        "nome": payload["nome"].strip(),
        "cognome": payload["cognome"].strip(),
        "data_nascita": payload["data_nascita"],
        "mansione": payload["mansione"].strip(),
    }
    users.append(new_user)
    save_users(users)

    response = jsonify({"user": new_user})
    response.status_code = 201
    return response


@app.route("/gestionale_utenti/users/<user_id>", methods=["GET", "PUT", "DELETE"])
def user_detail(user_id):
    if not ID_REGEX.match(user_id):
        return json_error("ID non valido", 400)

    users = load_users()
    current_user = None
    current_index = None
    for index, user in enumerate(users):
        if str(user.get("id")) == user_id:
            current_user = user
            current_index = index
            break

    if current_user is None:
        return json_error("Risorsa non trovata", 404)

    if request.method == "GET":
        response = jsonify({"user": current_user})
        response.status_code = 200
        return response

    if request.method == "DELETE":
        users.pop(current_index)
        save_users(users)
        response = jsonify({"message": "Utente eliminato"})
        response.status_code = 200
        return response

    payload = request.get_json(silent=True)
    is_valid, error_message = validate_user_payload(payload)
    if not is_valid:
        return json_error(error_message, 400)

    updated_user = {
        "id": current_user["id"],
        "nome": payload["nome"].strip(),
        "cognome": payload["cognome"].strip(),
        "data_nascita": payload["data_nascita"],
        "mansione": payload["mansione"].strip(),
    }

    users[current_index] = updated_user
    save_users(users)

    response = jsonify({"user": updated_user})
    response.status_code = 200
    return response


if __name__ == "__main__":
    ensure_data_file()
    app.run(debug=True)