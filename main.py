import mariadb
import secrets

from modules.config import db_config

from modules.users_db import *
from modules.sessions_db import *
from modules.notes_db import *
from modules.todos_db import *

from modules.patch_row import *
from modules.delete_row import *
from modules.close_db import *

from asgiref.wsgi import WsgiToAsgi
from flask import Flask, render_template, request, jsonify, abort, make_response

app: Flask = Flask(__name__)

create_log_file_if_not_exists: None = open("log.txt", "w").close()

log_file = open("log.txt", "a+")
log_file.seek(0)
log_file.write("\n–––––––––––––––––––––––––––––––––––\n\n")
log_file.flush()


# @app.before_request
# def debug():
#     log_file.write(f"Method: {request.method} Path: {request.path}\n")
#     log_file.flush()

# Source - https://stackoverflow.com/a/27036691
# Posted by dreyescat, modified by community. See post 'Timeline' for change history
# Retrieved 2026-03-25, License - CC BY-SA 3.0

def create_necessary():
    cursor = None
    conn = None

    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()

        create_users(cursor)
        create_sessions(cursor)
        create_notes(cursor)
        create_todos(cursor)
    except mariadb.Error as err:
        log_file.write(f"Necessary db table creation failed! {err}\n")
        log_file.flush()

        if conn:
            conn.rollback()

    finally:
        close_db(cursor=cursor, conn=conn)

@app.context_processor
def inject_enumerate():
    return dict(enumerate=enumerate)

@app.route("/")
def home():
    cursor = None
    conn = None

    session_id: str = request.cookies.get("session_id")

    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        if not session_id:
            abort(401)

        user_id = is_user_logged_in(cursor, session_id)

        if not user_id:
            abort(403)

        notes = get_notes(cursor, user_id)
        todos = get_todos(cursor, user_id)

        # for i, note in enumerate(notes):
        #     log_file.write(f"{i}")
        #     log_file.write(f"Notat values vist: {note.values()}\n")
        #     log_file.write(f"Notat tittel vist: {note["title"]}\n")
        #     log_file.write(f"Notat beskrivelse vist: {note["description"]}\n")
        #     log_file.flush()

        return render_template("index.html", notes=notes, todos=todos)
    except mariadb.Error as err:
        log_file.write(f"Get notes or get todos failed (home)! {err}\n")
        log_file.flush()

        if conn:
            conn.rollback()

        return jsonify("Data handling failed!"), 500
    finally:
        close_db(cursor=cursor, conn=conn)

@app.route("/signup", methods=["GET"])
def signup_page() -> str:
    return render_template("signup.html")

@app.route("/notes", methods=["GET"])
def show_all_notes():
    cursor = None
    conn = None

    session_id: str = request.cookies.get("session_id")

    if not session_id:
        abort(401)

    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
 
        user_id = is_user_logged_in(cursor, session_id)

        if not user_id:
            abort(403)

        # log_file.write("Før select query - alle notes\n")
        # log_file.flush()
        notes = get_notes(cursor, user_id)

        # log_file.write(f"Notater: {notes}\n")
        # log_file.flush()

        if not len(notes):
            return jsonify({}), 200 

        updated_notes = {}

        for parent in notes:
            updated_notes.update({
                "description": parent.get("description"),
                "id": parent.get("id"),
                "title": parent.get("title")
            })

        return jsonify(updated_notes), 200
    except mariadb.Error as err:
        log_file.write(f"Data handling failed! {err}\n")
        log_file.flush()

        if conn:
            conn.rollback()

        return jsonify("Data handling failed!"), 500
    finally:
        close_db(cursor=cursor, conn=conn)

@app.route("/todos", methods=["GET"])
def show_all_todos():
    cursor = None
    conn = None

    session_id: str = request.cookies.get("session_id")

    if not session_id:
        abort(401)

    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        user_id = is_user_logged_in(cursor, session_id)

        if not user_id:
            abort(403)

        # log_file.write("Før select query - alle todos\n")
        # log_file.flush()
        todos = get_todos(cursor, user_id)

        # log_file.write(f"TODOs: {todos}\n")
        # log_file.flush()

        if not len(todos):
            return jsonify({}), 200

        updated_todos = {}

        for parent in todos:
            # print(parent)

            updated_todos.update({
                "id": parent.get("id"),
                "title": parent.get("title"),
                "tasks": {
                    "description": parent.get("description"),
                    "task_done": parent.get("task_done")
                }
            })

        return jsonify(updated_todos), 200
    except mariadb.Error as err:
        log_file.write(f"Data handling failed! {err}\n")
        log_file.flush()

        if conn:
            conn.rollback()

        return jsonify("Data handling failed!"), 500
    finally:
        close_db(cursor=cursor, conn=conn)

def handle_empty_required(one: str | None, two: str | None, is_signup: bool):
    if not one or not two:  # reason: terminal users
        note: dict[str, str] = {}

        if not is_signup:
            note = {
                "error": "Title or description - empty!"
            }
        else:
            note = {
                "error": "Email or password - empty!"
            }

        return jsonify(note)

@app.route("/signup", methods=["POST"])
def signup():
    cursor = None
    conn = None

    email: str | None = request.form.get("email")
    password: str | None = request.form.get("password")

    response = handle_empty_required(email, password, is_signup=True)
    if response: return response

    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()

        user_id: int = new_user(cursor=cursor, email=email, password=password)
        session_id: str = secrets.token_hex(32)
        insert_session(cursor=cursor, session_id=session_id, user_id=user_id)

        m_response = make_response(render_template("index.html", email=email))
        m_response.set_cookie(
            "session_id",
            session_id,
            httponly=True,
            secure=True,
            samesite="Lax" # top-level GET only
        )

        return m_response
    except mariadb.Error as err:
        log_file.write(f"Data handling failed (user signup)! {err}\n")
        log_file.flush()

        if conn:
            conn.rollback()

        abort(500)
    finally:
        close_db(cursor=cursor, conn=conn)

@app.route("/add-note", methods=["POST"])
def add_note():
    cursor = None
    conn = None

    session_id: str = request.cookies.get("session_id")

    if not session_id:
        abort(401)

    title: str | None = request.form.get("title")
    description: str | None = request.form.get("description")

    response = handle_empty_required(title, description, is_signup=False)
    if response: return response

    # log_file.write(f"tittel og beskrivelse: {title, description}\n")
    # log_file.flush()

    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        user_id = is_user_logged_in(cursor, session_id)

        if not user_id:
            abort(403)

        note_id = insert_note(cursor=cursor, user_id=user_id,
            title=title, description=description)

        return jsonify(f"Note with id {note_id} successfully created"), 201
    except mariadb.IntegrityError as ierr:
        log_file.write(f"NULL value detected while inserting? {ierr}")
        log_file.flush()

        if conn:
            conn.rollback()

        return jsonify("NULL value detected while inserting?"), 500
    except mariadb.Error as err:
        log_file.write(f"Data insertion failed! {err}")
        log_file.flush()

        if conn:
            conn.rollback()

        return jsonify("Data insertion failed!"), 500
    except Exception as ex:
        log_file.write(f"Cannot add note! {ex}")
        log_file.flush()
        return jsonify({"error": "Cannot add note!"}), 500
    finally:
        close_db(cursor=cursor, conn=conn)

@app.route("/add-todo", methods=["POST"])
def add_todo():
    cursor = None
    conn = None

    session_id: str = request.cookies.get("session_id")

    if not session_id:
        abort(401)

    title: str | None = request.form.get("title")
    description: str | None = request.form.get("description")
    # log_file.write("Før task done henting\n")
    # log_file.flush()
    task_done: str | None = request.form.get("task-done")
    # log_file.write(f"Task done: {task_done or None}\n")
    # log_file.flush()

    response = handle_empty_required(title, description, is_signup=False)
    if response: return response

    # håndtere checkbox value
    if task_done == "on":
        # log_file.write("Task done checked\n")
        # log_file.flush()
        task_done = "1"
    else:
        # log_file.write("Task done not checked\n")
        # log_file.flush()
        task_done = "0"

    # log_file.write(f"tittel, beskrivelse, og task done: {title, description, task_done}\n")
    # log_file.flush()

    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        user_id = is_user_logged_in(cursor, session_id)

        if not user_id:
            abort(403)

        todo_id = insert_todo(cursor=cursor, user_id=user_id,
            title=title, description=description, task_done=task_done)

        return jsonify(f"TODO with id {todo_id} successfully created"), 201
    except mariadb.IntegrityError as ierr:
        log_file.write(f"NULL value detected while inserting? {ierr}")
        log_file.flush()

        if conn:
            conn.rollback()

        return jsonify("NULL value detected while inserting?"), 500
    except mariadb.Error as err:
        log_file.write(f"Data insertion failed! {err}")
        log_file.flush()

        if conn:
            conn.rollback()

        return jsonify("Data insertion failed!"), 500
    except Exception as ex:
        log_file.write(f"Cannot add TODO! {ex}")
        log_file.flush()
        return jsonify({"error": "Cannot add TODO!"}), 500
    finally:
        close_db(cursor=cursor, conn=conn)

@app.route("/patch-note", methods=["PATCH"])
def patch_note():
    cursor = None
    conn = None

    session_id: str = request.cookies.get("session_id")

    if not session_id:
        abort(401)
        
    note_title: str | None = request.args.get("title")
    note_description: str | None = request.args.get("description")
    note_id: str | None = request.args.get("id")
    
    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        user_id = is_user_logged_in(cursor, session_id)

        if not user_id:
            abort(403)

        patch_row(cursor=cursor, t_to_patch="Notes",
            title=note_title, description=note_description,
            row_id=int(note_id), user_id=user_id)

        return jsonify(f"Note with id {note_id} successfully edited"), 200
    except mariadb.Error as err:
        log_file.write(f"Data editing failed! {err}")
        log_file.flush()

        if conn:
            conn.rollback()

        return jsonify("Data editing failed!"), 500
    except Exception as ex:
        log_file.write(f"Cannot edit note! {ex}")
        log_file.flush()
        return jsonify({"error": "Cannot edit note!"}), 500
    finally:
        close_db(cursor=cursor, conn=conn)

@app.route("/patch-todo", methods=["PATCH"])
def patch_todo():
    cursor = None
    conn = None

    session_id: str = request.cookies.get("session_id")

    if not session_id:
        abort(401)

    todo_title: str | None = request.args.get("title")
    todo_description: str | None = request.args.get("description")
    task_done: str | None = request.args.get("task-done")
    todo_id: str | None = request.args.get("id")

    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        user_id = is_user_logged_in(cursor, session_id)

        if not user_id:
            abort(403)

        patch_row(cursor=cursor, t_to_patch="TODOs",
            title=todo_title, description=todo_description,
            row_id=int(todo_id), user_id=user_id,
            task_done=task_done)

        return jsonify(f"TODO with id {todo_id} successfully edited"), 200
    except mariadb.Error as err:
        log_file.write(f"Data editing failed! {err}")
        log_file.flush()

        if conn:
            conn.rollback()

        return jsonify("Data editing failed!"), 500
    except Exception as ex:
        log_file.write(f"Cannot edit TODO! {ex}")
        log_file.flush()
        return jsonify({"error": "Cannot edit TODO!"}), 500
    finally:
        close_db(cursor=cursor, conn=conn)

@app.route("/delete-note", methods=["DELETE"])
def delete_note():
    cursor = None
    conn = None

    session_id: str = request.cookies.get("session_id")

    if not session_id:
        abort(401)

    note_id: str | None = request.args.get("id")

    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        user_id = is_user_logged_in(cursor, session_id)

        if not user_id:
            abort(403)

        delete_row(cursor=cursor, t_to_delete="Notes",
        row_id=int(note_id), user_id=user_id)

        return jsonify(f"Note with id {note_id} successfully deleted"), 200
    except mariadb.Error as err:
        log_file.write(f"Data deletion failed! {err}")
        log_file.flush()

        if conn:
            conn.rollback()

        return jsonify("Data deletion failed!"), 500
    except Exception as ex:
        log_file.write(f"Cannot delete note! {ex}")
        log_file.flush()
        return jsonify({"error": "Cannot delete note!"}), 500
    finally:
        close_db(cursor=cursor, conn=conn)

@app.route("/delete-todo", methods=["DELETE"])
def delete_todo():
    cursor = None
    conn = None

    session_id: str = request.cookies.get("session_id")

    if not session_id:
        abort(401)

    todo_id: str | None = request.args.get("id")

    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        user_id = is_user_logged_in(cursor, session_id)

        if not user_id:
            abort(403)

        delete_row(cursor=cursor, t_to_delete="TODOs",
        row_id=int(todo_id), user_id=user_id)

        return jsonify(f"TODO with id {todo_id} successfully deleted"), 200
    except mariadb.Error as err:
        log_file.write(f"Data deletion failed! {err}")
        log_file.flush()

        if conn:
            conn.rollback()

        return jsonify("Data deletion failed!"), 500
    except Exception as ex:
        log_file.write(f"Cannot delete TODO! {ex}")
        log_file.flush()
        return jsonify({"error": "Cannot delete TODO!"}), 500
    finally:
        close_db(cursor=cursor, conn=conn)

asgi_app: WsgiToAsgi = WsgiToAsgi(app)

if __name__ == "__main__":
    create_necessary()
    app.run()
