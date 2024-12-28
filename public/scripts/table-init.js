function initializeTable() {
    if (typeof $ === 'undefined' || typeof $.fn.DataTable === 'undefined') {
        console.error('jQuery or DataTables is not loaded!');
        return;
    }

    document.querySelectorAll('table').forEach(table => {
        if (!table.classList.contains('display')) {
            table.classList.add('display'); // Add DataTables required class
        }
    });

    document.querySelectorAll('table.display').forEach(table => {
        if (!$.fn.dataTable.isDataTable(table)) {
            $(table).DataTable({
                paging: false,
                searching: false,
                scrollX: true,
            });
        }
    });
}



// $('table').DataTable({
//     paging: false,
//     searching: false,
//     scrollX: true,
// });

document.addEventListener('DOMContentLoaded', () => {
    initializeTable();
});

document.addEventListener('astro:after-swap', () => {
    initializeTable();
});

initializeTable();
