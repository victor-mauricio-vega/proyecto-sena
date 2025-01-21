const btneliminar = document.querySelectorAll(".btneliminar");

(function(){

    btneliminar.forEach((btn)=>{
        btn.addEventListener('click', function(e){
            e.preventDefault();
            Swal.fire({
                title: "¿Desea eliminar?",
                icon:"warning",
                iconColor:"#dc3545",
                cancelButtonText:"Cancelar",
                cancelButtonColor:"#0d6efd",
                showCancelButton: true,
                confirmButtonText: "Eliminar",
                confirmButtonColor: "#dc3545",
                backdrop: true,
                showLoaderOnConfirm: true,
                preConfirm: () => {
                    location.href = e.target.href;
                },
                allowOutsideClick: () => false,
                allowEscapeKey: () => false
            });
        }); 
    });
})();

