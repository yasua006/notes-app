// const main = async (
//     title: string,
//     description: string
// ): Promise<void> => {
//     const res: Response = await fetch(
//         `/add?title=${title}&description=${description}`,
//         { method: "POST" }
//     );
//     if (!res.ok) {
//         throw new Error("Not ok!");
//     }
//     const data = res.json();
//     // console.log(data);
//     console.info(
//         "Object promise to string:",
//         JSON.stringify(data)
//     );
//     localStorage.setItem(
//         "Note",
//         JSON.stringify(data).replaceAll("{}", "")
//     );
// };
// main("Test", "testing");
