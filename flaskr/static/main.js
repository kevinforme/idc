window.onload = function () {
    var events = document.getElementsByClassName('event');
    var pagination=document.getElementById('event_page');
    window.location.search.substring(1)
    if (events.length < 10 && (window.location.search.substring(1).split('=')[1] == 1 || window.location.search=='')) {
        pagination.style.display='none';
    }
}