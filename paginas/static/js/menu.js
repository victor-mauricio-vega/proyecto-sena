document.addEventListener('DOMContentLoaded', function() {
    const toggleButton = document.querySelector('.navbar-toggler');
    const sidebar = document.querySelector('.sidebar');

    toggleButton.addEventListener('click', function() {
        sidebar.classList.toggle('active');
    });

    // Cerrar el menú al hacer clic fuera de él
    document.addEventListener('click', function(event) {
        const isClickInside = sidebar.contains(event.target);
        const isToggleButton = toggleButton.contains(event.target);
        if (!isClickInside && !isToggleButton) {
            sidebar.classList.remove('active');
        }
    });

    // Ocultar el menú al cargar la página
    sidebar.classList.remove('active');
});
$(document).ready(function() {
    $(".navbar-toggler").click(function() {
        $(".sidebar").toggleClass("active");
    });
});