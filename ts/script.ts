const main = async() => {
    const main: HTMLElement = document.body
    .querySelector("main");

    const note_id: HTMLSpanElement = main
    .querySelector("#note-id");

    const delete_note_btn: HTMLButtonElement = main
    .querySelector("#delete-note-btn");
    const delete_todo_btn: HTMLButtonElement = main
    .querySelector("#delete-todo-btn");

    delete_note_btn.addEventListener("click", async() => {
        const res: Response = await fetch(
            `/delete-note?id=${note_id.textContent}`,
            {"method": "DELETE"}
        );

        if (!res.ok) {
            throw new Error("Note deletion not ok!");
        }

        // console.info("Delete note result:", res.json());
    });
    delete_todo_btn.addEventListener("click", async() => {
        const res: Response = await fetch(
            `/delete-todo?id=${note_id.textContent}`,
            {"method": "DELETE"}
        );

        if (!res.ok) {
            throw new Error("TODO deletion not ok!");
        }

        // console.info("Delete TODO result:", res.json());
    });
}

main();