document.addEventListener("DOMContentLoaded", function () {
    var highlight1 = document.querySelector('.sidenav > div > a[href="' + window.location.pathname + '"]');
    var highlight2 = document.querySelector('.sidenav > div > a[href="' + window.location.pathname + window.location.search + '"]');
    if (highlight1) highlight1.classList.add('active');
    if (highlight2) highlight2.classList.add('active');

    var toastList = document.querySelectorAll(".toast");
    if (toastList) {
        toastList.forEach(element => {
            new bootstrap.Toast(element, { delay: 7500 }).show();
        });
    }
});

function toggleSidebar() {
    document.querySelector('.sidenav').classList.toggle("sidenav-show");
    document.querySelector('.main').classList.toggle("main-below");
    document.querySelector('body').classList.toggle("body-below");
    document.querySelector('.sidenav-button').classList.toggle("sidenav-button-show");
}

document.addEventListener('htmx:afterSwap', function (e) {
    var mainModal = document.getElementById('mainModal');
    var bootstrapModal = new bootstrap.Modal(mainModal);
    bootstrapModal.show();

    if (e.detail.requestConfig.triggeringEvent.type == "submit") {
        var submitter = e.detail.requestConfig.triggeringEvent.submitter;
        submitter.disabled = false;
        submitter.querySelector('i').classList.remove('d-none');
        var submitterDiv = submitter.querySelector('div');
        if (submitterDiv) {
            submitterDiv.remove();
        }
    } else {
        var elt = e.detail.requestConfig.elt;
        elt.disabled = false;
        var eltDiv = elt.querySelector('div');
        if (eltDiv) {
            eltDiv.remove();
        }
    }
});

document.addEventListener('htmx:beforeRequest', function(evt) {
    const existingBackdrops = document.querySelectorAll('.modal-backdrop');
    existingBackdrops.forEach(backdrop => backdrop.remove());
});

jQuery(document).ready(function($) {
    if ($('#jsTable').length) {
        $('#jsTable').DataTable({
          responsive: true,
          dom: '<"d-flex flex-nowrap"<"flex-grow-1"f><"flex-shrink-0 ms-1"l>>t<"row"<"col-12 col-md-6"i><"col-12 col-md-6 mt-2 mt-md-0"p>>',
          stateSave: true,
          lengthMenu: [5, 10, 25, 50, 100],
          pagingType: "numbers",
          pageLength: 10,
          language: {
            lengthMenu: "_MENU_",
            search: "_INPUT_",
            searchPlaceholder: "Search"
          },
          columnDefs: [{
            targets: [-1],
            orderable: false
          },
          {
            targets: [0, -1],
            responsivePriority: 1
          }],
          "initComplete": function () {
            $("#jsTable").show();
          }
        });
    
        $('#jsTable_length').removeClass('dataTables_length');
        $('#jsTable_filter').removeClass('dataTables_filter');
        $('#jsTable_filter > label').contents().unwrap();
        $('#jsTable_length > label').contents().unwrap();
        $('#jsTable_filter > input').removeClass("form-control-sm");
        $('#jsTable_length > select').removeClass("form-select-sm");
      }

    const list = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'))
    list.map((el) => {
    let opts = {
        animation: false,
    }
    if (el.hasAttribute('data-bs-content-id')) {
        opts.content = document.getElementById(el.getAttribute('data-bs-content-id')).innerHTML;
        opts.html = true;
        opts.delay = 100;
    }
    new bootstrap.Popover(el, opts);
    })
});   