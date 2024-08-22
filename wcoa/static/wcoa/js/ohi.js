class Accordion {
    static selector() {
        return "[data-accordion]";
    }

    constructor(node) {
        this.accordion = node;
        this.link = this.accordion.querySelector("[data-accordion-link]");
        this.content = this.accordion.querySelector("[data-accordion-content]");
        this.bindEvents();
    }

    bindEvents() {
        this.link.addEventListener("click", (e) => {
            e.preventDefault();
            let open = this.accordion.classList.contains("is-open");
            this.accordion.classList.toggle("is-open");

            if (open) {
                this.link.setAttribute("aria-expanded", "false");
                this.link.setAttribute("tab-index", 0);
                this.content.setAttribute("aria-hidden", "true");
                open = false;
            } else {
                this.link.setAttribute("aria-expanded", "true");
                this.link.setAttribute("tab-index", -1);
                this.content.setAttribute("aria-hidden", "false");
                open = true;
            }
        });

        this.link.addEventListener("focus", () => {
            this.link.setAttribute("aria-selected", "true");
        });

        this.link.addEventListener("blur", () => {
            this.link.setAttribute("aria-selected", "false");
        });
    }
}

document.addEventListener("DOMContentLoaded", function () {
    for (const accordion of document.querySelectorAll(Accordion.selector())) {
        new Accordion(accordion);
    }
});