function autoSubmitFilter() {
    const filterForm = document.querySelector('#filter-form');
    const filterInputs = filterForm.querySelectorAll('input, select');

    filterInputs.forEach(input => {
        input.addEventListener('change', () => {
            filterForm.submit();
        });
    });
}

autoSubmitFilter();