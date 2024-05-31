document.addEventListener('DOMContentLoaded', function() {
    // Function to toggle caret icon classes
    function toggleCaretIcon(collapseElement, caretElement) {
        collapseElement.addEventListener('show.bs.collapse', function() {
            caretElement.classList.remove('bi-chevron-right');
            caretElement.classList.add('bi-chevron-down');
        });

        collapseElement.addEventListener('hide.bs.collapse', function() {
            caretElement.classList.remove('bi-chevron-down');
            caretElement.classList.add('bi-chevron-right');
        });
    }

    // Select all elements with data-bs-toggle attribute
    const collapsibleElements = document.querySelectorAll('[data-bs-toggle="collapse"]');

    collapsibleElements.forEach(element => {
        const collapseId = element.getAttribute('href');
        const caretElement = element.querySelector('.collapse-head');

        if (collapseId && caretElement) {
            const collapseElement = document.querySelector(collapseId);
            if (collapseElement) {
                toggleCaretIcon(collapseElement, caretElement);

                // Prevent collapse from closing when clicking on an item within the dropdown
                const collapseItems = collapseElement.querySelectorAll('.collapse-item');
                collapseItems.forEach(item => {
                    item.addEventListener('click', function(e) {
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

    // Mark the clicked item as active and keep parent collapsible open
    const collapseItems = document.querySelectorAll('.collapse-item');
    collapseItems.forEach(item => {
        item.addEventListener('click', function() {
            collapseItems.forEach(i => i.classList.remove('active'));
            item.classList.add('active');

            const parentCollapse = item.closest('.collapse');
            if (parentCollapse) {
                const parentTrigger = document.querySelector(`[href="#${parentCollapse.id}"]`);
                if (parentTrigger) {
                    parentTrigger.classList.add('active');
                    parentCollapse.classList.add('show');
                }
            }
        });
    });
});
