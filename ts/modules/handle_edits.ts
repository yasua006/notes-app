import { main_elem } from "./main_elem_var";
import { get_matching_id } from "./get_matching_id";

export const handle_note_edits = async (
    edit_note_btn: HTMLButtonElement
): Promise<void> => {
    const id: string = edit_note_btn.id.replaceAll(
        "edit-note-btn-",
        "note-id-"
    );
    const title_id = "[id^='note-title-']";
    const desc_id = "[id^='note-description-']";

    const matching_note_id: string = get_matching_id(id);
    const matching_note_title: string = main_elem
        .querySelector(title_id)
        .querySelector("h3").textContent;
    const matching_note_desc: string =
        main_elem.querySelector(desc_id).textContent;

    const edit_title_prompt: string = prompt(
        `Current title: ${matching_note_title}`
    );
    const edit_desc_prompt: string = prompt(
        `Current description: ${matching_note_desc}`
    );

    if (!edit_title_prompt) return;
    if (!edit_desc_prompt) return;

    try {
        const res: Response = await fetch(
            `/patch-note?title=${edit_title_prompt}&description=${edit_desc_prompt}&id=${matching_note_id}`,
            { method: "PATCH" }
        );

        if (!res.ok) {
            throw new Error("Note editing not ok!");
        }

        // console.info("Edit note result:", res.json());

        location.reload();
    } catch (err) {
        alert(
            "Error: Note editing failed! Please try again later!"
        );
        throw new Error(
            `Cannot edit matching note! ${err}`
        );
    }
};

export const handle_todo_edits = async (
    edit_todo_btn: HTMLButtonElement
): Promise<void> => {
    const id: string = edit_todo_btn.id.replaceAll(
        "edit-todo-btn-",
        "todo-id-"
    );
    const title_id = "[id^='todo-title-']";
    const desc_id = "[id^='todo-description-']";
    const task_done_id = "[id^='task-done-']";

    const matching_todo_id: string = get_matching_id(id);
    const matching_todo_title: string = main_elem
        .querySelector(title_id)
        .querySelector("h3").textContent;
    const matching_todo_desc: string =
        main_elem.querySelector(desc_id).textContent;
    const matching_task_done: string = main_elem
        .querySelector(task_done_id)
        .querySelector(
            "input[type='checkbox']"
        ).textContent;

    const edit_title_prompt: string = prompt(
        `Current title: ${matching_todo_title}`
    );
    const edit_desc_prompt: string = prompt(
        `Current description: ${matching_todo_desc}`
    );
    const edit_task_done_prompt: string = prompt(
        `Current task done: ${matching_task_done}`
    );

    if (!edit_title_prompt) return;
    if (!edit_desc_prompt) return;
    if (!edit_task_done_prompt) return;

    try {
        const res: Response = await fetch(
            `/patch-todo?title=${edit_title_prompt}&description=${edit_desc_prompt}&task_done=${edit_task_done_prompt}&id=${matching_todo_id}`,
            { method: "PATCH" }
        );

        if (!res.ok) {
            throw new Error("TODO editing not ok!");
        }

        // console.info("Edit TODO result:", res.json());

        location.reload();
    } catch (err) {
        alert(
            "Error: TODO editing failed! Please try again later!"
        );
        throw new Error(
            `Cannot edit matching TODO! ${err}`
        );
    }
};
