import { main_elem } from "./main_elem_var";

export const get_matching_id = (id: string): string => {
    return main_elem.querySelector("span#" + id)
        .textContent;
};