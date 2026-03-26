import { main_elem } from "./modules/main_elem_var";
import {
    handle_note_deletions,
    handle_todo_deletions
} from "./modules/handle_deletions";
import {
    handle_note_edits,
    handle_todo_edits
} from "./modules/handle_edits";

const edit_requests = async () => {
    const edit_note_buttons: NodeListOf<HTMLButtonElement> =
        main_elem.querySelectorAll(
            "button[id^='edit-note-btn-']"
        );
    const edit_todo_buttons: NodeListOf<HTMLButtonElement> =
        main_elem.querySelectorAll(
            "button[id^='edit-todo-btn-']"
        );

    edit_note_buttons.forEach((edit_note_btn) => {
        (edit_note_btn.addEventListener("click", async () =>
            handle_note_edits(edit_note_btn)
        ),
            { passive: true });
    });
    edit_todo_buttons.forEach((edit_todo_btn) => {
        (edit_todo_btn.addEventListener("click", async () =>
            handle_todo_edits(edit_todo_btn)
        ),
            { passive: true });
    });
};

const delete_requests = async () => {
    const delete_note_buttons: NodeListOf<HTMLButtonElement> =
        main_elem.querySelectorAll(
            "button[id^='delete-note-btn-']"
        );
    const delete_todo_buttons: NodeListOf<HTMLButtonElement> =
        main_elem.querySelectorAll(
            "button[id^='delete-todo-btn-']"
        );

    delete_note_buttons.forEach(
        (delete_note_btn) => {
            delete_note_btn.addEventListener(
                "click",
                async () =>
                    handle_note_deletions(delete_note_btn)
            );
        },
        { passive: true }
    );
    delete_todo_buttons.forEach(
        (delete_todo_btn) => {
            delete_todo_btn.addEventListener(
                "click",
                async () =>
                    handle_todo_deletions(delete_todo_btn)
            );
        },
        { passive: true }
    );
};

const main = async () => {
    edit_requests();
    delete_requests();
};

main();
