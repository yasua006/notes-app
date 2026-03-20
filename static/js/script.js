const { createApp, ref } = Vue;
const app = createApp({
    setup() {
        const notes = ref("notes");
        notes.value.replaceAll("[]", "");
        return {
            notes
        };
    }
});
app.mount("#app");
