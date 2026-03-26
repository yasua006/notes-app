import { main_elem } from "./modules/main_elem_var";

/**
 * @param {NodeListOf<HTMLInputElement>} target_checkboxes
 */
const target_checkboxes: NodeListOf<HTMLInputElement> =
    main_elem.querySelectorAll(
        "input[value='1'][type='checkbox']"
    );

target_checkboxes.forEach((target_checkbox) => {
    const description_id: string =
        target_checkbox.parentElement.id.replaceAll(
            "task-done-",
            "todo-description-"
        );

    /**
     * @param {NodeListOf<HTMLHeadingElement>} target_descriptions
     */
    const target_descriptions: NodeListOf<HTMLLIElement> =
        main_elem.querySelectorAll(
            `li[id^=${description_id}]`
        );

    target_descriptions.forEach((target_desc) => {
        target_desc.style.fontWeight = "bold";
    });
});
