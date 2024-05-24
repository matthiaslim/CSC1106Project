document.querySelector('#collapse-crm').addEventListener('show.bs.collapse', function () {
    document.querySelector('#caret-crm').classList.remove('bi-chevron-right');
    document.querySelector('#caret-crm').classList.add('bi-chevron-down');
});

document.querySelector('#collapse-crm').addEventListener('hide.bs.collapse', function () {
    document.querySelector('#caret-crm').classList.remove('bi-chevron-down');
    document.querySelector('#caret-crm').classList.add('bi-chevron-right');
});

document.querySelector('#collapse-finance').addEventListener('show.bs.collapse', function () {
    document.querySelector('#caret-finance').classList.remove('bi-chevron-right');
    document.querySelector('#caret-finance').classList.add('bi-chevron-down');
});

document.querySelector('#collapse-finance').addEventListener('hide.bs.collapse', function () {
    document.querySelector('#caret-finance').classList.remove('bi-chevron-down');
    document.querySelector('#caret-finance').classList.add('bi-chevron-right');
});