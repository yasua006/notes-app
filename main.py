import json
import hashlib

from flask import Flask, render_template, request, jsonify
app: Flask = Flask(__name__)


@app.route("/")
def home() -> str:
    # TODO: Flytt til hjelper funksjon (neste commit)
    notes_json = open("notes.json")
    notes = json.load(notes_json)

    return render_template("index.html", notes=notes)

# TODO: Håndtere tom notater (neste commit)
@app.route("/notes", methods=["GET"])
def get_notes():
    # TODO: Flytt til hjelper funksjon (neste commit)
    notes_json = open("notes.json")
    notes = json.load(notes_json)

    return jsonify(notes), 200

def handle_empty_note(title: str | None, description: str | None):
    if not title or not description:  # reason: terminal users
        note: dict[str, str] = {
            "error": "Title or description - empty!"
        }

        return jsonify(note), 400

@app.route("/add", methods=["POST"])
def add_note():
    title: str | None = request.form.get("title")
    description: str | None = request.form.get("description")
    
    log_file = open("log.txt", "a+")
    log_file.seek(0)
    log_file.write("\n–––––––––––––––––––––––––––––––––––\n\n")
    # log_file.write(f"tittel og beskrivelse: {title, description}\n")

    response = handle_empty_note(title=title, description=description)
    if response: return response

    # log_file.write("før notat dict\n")

    index: str = hashlib.sha512().hexdigest()

    note: dict[str, dict[str, str | None]] = {
        f"note_{index}": {
            "title": title,
            "description": description
        }
    }

    # log_file.write(f"notat `dict`: {json.dumps(note)}\n")

    try:
        with open("notes.json", "a+") as notes_json:
            notes_json.seek(0)

            log_file.write("før json load (add)\n")
            log_file.write(f"Stream posisjon før readlines: {str(notes_json.tell())}\n")
            notes: str = notes_json.read()
            
            if not notes:
                log_file.write("notater - tom\n")

            log_file.write(f"notater før ny notat: {notes or "null"}\n")
            notes += (json.dumps(note))
            log_file.write(f"notater etter ny notat: {notes or "null"}\n")

            log_file.write(f"Stream posisjon etter readlines: {str(notes_json.tell())}")

            # * Etter siste logg
            log_file.close()

            json.dump(notes, notes_json, indent=4, separators=(",", ":"))
    except FileNotFoundError as fnfe:
        app.logger.error("`notes.json` doesn't exist!", fnfe)
        return jsonify({"error": "notes.json doesn't exist!"}), 500
    except json.JSONDecodeError as jde:
        app.logger.error("`notes.json` couldn't update!", jde)
        return jsonify({"error": "notes.json couldn't update!"}), 500
    except Exception as ex:
        app.logger.error("Cannot add note!", ex)
        return jsonify({"error": "Cannot add note!"}), 500

    return jsonify(note), 201

if __name__ == "__main__":
    app.run()
