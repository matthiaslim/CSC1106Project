document.addEventListener('DOMContentLoaded', function () {

    // Select all elements with data-bs-toggle attribute
    const collapsibleElements = document.querySelectorAll('[data-bs-toggle="collapse"]');

    collapsibleElements.forEach(element => {
        const collapseId = element.getAttribute('href');
        const caretElement = element.querySelector('.collapse-head');

        if (collapseId && caretElement) {
            const collapseElement = document.querySelector(collapseId);
            if (collapseElement) {

                // Toggle caret icon classes based on collapse state
                collapseElement.addEventListener('show.bs.collapse', function () {
                    caretElement.classList.remove('bi-chevron-right');
                    caretElement.classList.add('bi-chevron-down');
                });

                collapseElement.addEventListener('hide.bs.collapse', function () {
                    caretElement.classList.remove('bi-chevron-down');
                    caretElement.classList.add('bi-chevron-right');
                });

                // Prevent collapse from closing when clicking on an item within the dropdown
                const collapseItems = collapseElement.querySelectorAll('.collapse-item');
                collapseItems.forEach(item => {
                    item.addEventListener('click', function (e) {
                        e.stopPropagation();
                    });
                });
            }
        }
    });

    // Ensure the active sidebar link and caret state
    const activeCollapse = document.querySelector('.sidenav-items .active[data-bs-toggle="collapse"]');
    if (activeCollapse) {
        const caretElement = activeCollapse.querySelector('.collapse-head');
        const collapseElement = document.querySelector(activeCollapse.getAttribute('href'));
        if (caretElement && collapseElement) {
            caretElement.classList.remove('bi-chevron-right');
            caretElement.classList.add('bi-chevron-down');
            collapseElement.classList.add('show');
        }
    }

    // Prevent dropdown closing on checkbox click
    const checkboxes = document.querySelectorAll('.filter-item');
    checkboxes.forEach(checkbox =>
        checkbox.addEventListener('click', (event) => event.stopPropagation()));


    // Map category checkboxes to their collapse containers
    const filterMap = {
        categoryCheck: document.getElementById('categoryFilter'),
        sizeCheck: document.getElementById('sizeFilter'),
        priceCheck: document.getElementById('priceFilter'),
    };

    checkboxes.forEach(checkbox => {
        const filterId = checkbox.querySelector('input').id;  // Get checkbox ID
        const filterContainer = filterMap[filterId];          // Find mapped container

        checkbox.addEventListener('click', () => {
            const isChecked = checkbox.querySelector('input').checked;

            if (isChecked) {
                // Show the clicked filter's container
                filterContainer.classList.add('show');
            } else {
                // Hide the clicked filter's container
                filterContainer.classList.remove('show');
            }
        });
    });
});
