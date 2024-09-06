var onRequestOpenModal;

(function () {
    onRequestOpenModal = function (modal) {
        // Find the form in the modal
        const form = modal.body.querySelector('form');

        // Add the checkbox for "Open in new tab"
        const targetCheckboxHTML = `
            <div class="field">
                <input type="checkbox" name="target_blank" id="target_blank" value="_blank">
                <label for="target_blank">Open link in a new tab</label>
            </div>`;

        // Append it to the form
        form.insertAdjacentHTML('beforeend', targetCheckboxHTML);

        // When the form is submitted, append the `target_blank` field to the form data
        form.addEventListener('submit', function () {
            const targetBlank = form.querySelector('input[name="target_blank"]').checked ? '_blank' : '';
            form.querySelector('input[name="link_target"]').value = targetBlank;
        });
    };

    document.addEventListener('wagtail:modal-open', function (event) {
        const modal = event.detail.modal;
        if (modal.body.classList.contains('richtext-link-chooser')) {
            onRequestOpenModal(modal);
        }
    });
})();
