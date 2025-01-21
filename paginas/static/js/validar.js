document.querySelector('form').addEventListener('submit', function(event) {
    var categoriaSelect = document.querySelector('select[name="id_categoria"]');
    if (categoriaSelect.value === '') {
        event.preventDefault(); 
        document.querySelector('.error').style.display = 'block'; 
    }
});
document.querySelector('form').addEventListener('submit', function(event) {
    var estadoSelect = document.querySelector('select[name="id_estado"]');
    if (estadoSelect.value === '') {
        event.preventDefault(); 
        document.querySelector('.error').style.display = 'block'; 
    }
});
document.querySelector('form').addEventListener('submit', function(event) {
    var identificacionSelect = document.querySelector('select[name="identificacion"]');
    if (identificacionSelect.value === '') {
        event.preventDefault(); 
        document.querySelector('.error').style.display = 'block'; 
    }
});
document.querySelector('form').addEventListener('submit', function(event) {
    var rolSelect = document.querySelector('select[name="id_rol"]');
    if (rolSelect.value === '') {
        event.preventDefault(); 
        document.querySelector('.error').style.display = 'block';
    }
});