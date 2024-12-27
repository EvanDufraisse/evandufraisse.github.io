document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll('table').forEach(table => {
        table.classList.add('display');
    });
    $('table').DataTable({
        paging: false,
        searching: false,
        scrollX: true,
    });
});

