import { get_matching_id } from "./get_matching_id";
export const handle_note_deletions = async (delete_note_btn) => {
    const id = delete_note_btn.id.replaceAll("delete-note-btn-", "note-id-");
    const matching_note_id = get_matching_id(id);
    const confirm_result = confirm("Are you sure you want to delete the note? ");
    if (!confirm_result)
        return;
    try {
        const res = await fetch(`/delete-note?id=${matching_note_id}`, { method: "DELETE" });
        if (!res.ok) {
            throw new Error("Note deletion not ok!");
        }
        // console.info("Delete note result:", res.json());
        location.reload();
    }
    catch (err) {
        alert("Error: Note deletion failed! Please try again later!");
        throw new Error(`Cannot delete matching note! ${err}`);
    }
};
export const handle_todo_deletions = async (delete_todo_btn) => {
    const id = delete_todo_btn.id.replaceAll("delete-todo-btn-", "todo-id-");
    const matching_todo_id = get_matching_id(id);
    const confirm_result = confirm("Are you sure you want to delete the TODO? ");
    if (!confirm_result)
        return;
    try {
        const res = await fetch(`/delete-todo?id=${matching_todo_id}`, { method: "DELETE" });
        if (!res.ok) {
            throw new Error("TODO deletion not ok!");
        }
        // console.info("Delete TODO result:", res.json());
        location.reload();
    }
    catch (err) {
        alert("Error: TODO deletion failed! Please try again later!");
        throw new Error(`Cannot delete matching TODO! ${err}`);
    }
};
