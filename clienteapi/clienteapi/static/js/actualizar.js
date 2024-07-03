// static/js/actualizar.js
document.addEventListener("DOMContentLoaded", function() {
    // Mostrar mensajes de éxito o error si los hay
    if (messages.length > 0) {
        for (let message of messages) {
            if (message.tags.includes('success')) {
                $('#successModal').modal('show');
                document.getElementById('modalAcceptButton').addEventListener('click', function() {
                    // Cerrar sesión y redirigir al login
                    fetch(logoutUrl, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': csrfToken
                        }
                    }).then(response => {
                        if (response.ok) {
                            window.location.href = loginUrl;
                        }
                    });
                });
            } else {
                $('#errorModal').modal('show');
            }
        }
    }

    // Manejar la eliminación del usuario
    document.getElementById('confirmDeleteButton').addEventListener('click', function() {
        fetch(deleteUrl, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            }
        }).then(response => {
            if (response.ok) {
                fetch(logoutUrl, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrfToken
                    }
                }).then(response => {
                    if (response.ok) {
                        window.location.href = loginUrl;
                    }
                });
            } else {
                alert('Error al eliminar el usuario');
            }
        }).catch(error => {
            alert('Error al eliminar el usuario');
        });
    });
});
