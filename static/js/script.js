const main_elem = document.body.querySelector("main");
// const edit_requests = async () => {
//     const edit_note_buttons: NodeListOf<HTMLButtonElement> =
//         main_elem.querySelectorAll(
//             "[id^='edit-note-btn-']"
//         );
//     const edit_todo_buttons: NodeListOf<HTMLButtonElement> =
//         main_elem.querySelectorAll(
//             "[id^='edit-todo-btn-']"
//         );
//     edit_note_buttons.forEach((edit_note_btn) => {
//         edit_note_btn.addEventListener(
//             "click",
//             async () => {
//                 const res: Response = await fetch(
//                     `/patch-note?title=${title}&description=${description}&id=${note_id}`,
//                     { method: "PATCH" }
//                 );
//                 if (!res.ok) {
//                     throw new Error("Note editing not ok!");
//                 }
//                 console.info(
//                     "Edit note result:",
//                     res.json()
//                 );
//             }
//         );
//     });
//     edit_todo_buttons.forEach((edit_todo_btn) => {
//         edit_todo_btn.addEventListener(
//             "click",
//             async () => {
//                 const res: Response = await fetch(
//                     `/patch-todo?title=${title}&description=${description}&task_done=${task_done}&id=${todo_id}`,
//                     { method: "PATCH" }
//                 );
//                 if (!res.ok) {
//                     throw new Error("TODO editing not ok!");
//                 }
//                 console.info(
//                     "Edit TODO result:",
//                     res.json()
//                 );
//             }
//         );
//     });
// };
const delete_requests = async () => {
    const delete_note_buttons = main_elem.querySelectorAll("[id^='delete-note-btn-']");
    const delete_todo_buttons = main_elem.querySelectorAll("[id^='delete-todo-btn-']");
    delete_note_buttons.forEach((delete_note_btn) => {
        delete_note_btn.addEventListener("click", async () => {
            const delete_note_btn_id_ending = delete_note_btn.id.replaceAll("delete-note-btn-", "");
            const id = "note-id-" + delete_note_btn_id_ending;
            const matching_note_id = main_elem.querySelector("#" + id).textContent;
            const res = await fetch(`/delete-note?id=${matching_note_id}`, { method: "DELETE" });
            if (!res.ok) {
                throw new Error("Note deletion not ok!");
            }
            // console.info(
            //     "Delete note result:",
            //     res.json()
            // );
            location.reload();
        });
    });
    delete_todo_buttons.forEach((delete_todo_btn) => {
        delete_todo_btn.addEventListener("click", async () => {
            const delete_todo_btn_id_ending = delete_todo_btn.id.replaceAll("delete-todo-btn-", "");
            const id = "todo-id-" + delete_todo_btn_id_ending;
            const matching_todo_id = main_elem.querySelector("#" + id).textContent;
            const res = await fetch(`/delete-todo?id=${matching_todo_id}`, { method: "DELETE" });
            if (!res.ok) {
                throw new Error("TODO deletion not ok!");
            }
            // console.info(
            //     "Delete TODO result:",
            //     res.json()
            // );
            location.reload();
        });
    });
};
const main = async () => {
    // edit_requests();
    delete_requests();
};
main();
