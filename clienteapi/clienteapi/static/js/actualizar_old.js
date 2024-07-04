document.addEventListener("DOMContentLoaded", function() {
    // Mostrar mensajes de éxito o error si los hay
    if (messages.length > 0) {
        messages.forEach(message => {
            if (message.tags.includes('success')) {
                $('#updateSuccessModal').modal('show');
                let updateModalAcceptButton = document.getElementById('updateModalAcceptButton');
                updateModalAcceptButton.replaceWith(updateModalAcceptButton.cloneNode(true));
                document.getElementById('updateModalAcceptButton').addEventListener('click', updateLogoutAndRedirect);
            } else {
                $('#updateErrorModal').modal('show');
            }
        });
    }

    // Manejar la eliminación del usuario
    let confirmDeleteButton = document.getElementById('confirmDeleteButton');
    confirmDeleteButton.replaceWith(confirmDeleteButton.cloneNode(true));
    document.getElementById('confirmDeleteButton').addEventListener('click', function() {
        fetch(deleteUrl, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            }
        }).then(response => {
            if (response.ok) {
                $('#deleteSuccessModal').modal('show');
                let deleteModalSuccessAcceptButton = document.getElementById('deleteModalSuccessAcceptButton');
                deleteModalSuccessAcceptButton.replaceWith(deleteModalSuccessAcceptButton.cloneNode(true));
                document.getElementById('deleteModalSuccessAcceptButton').addEventListener('click', updateLogoutAndRedirect);
            } else {
                $('#deleteErrorModal').modal('show');
            }
        }).catch(error => {
            $('#deleteErrorModal').modal('show');
        });
    });
});

function updateLogoutAndRedirect() {
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
}

