document.addEventListener("DOMContentLoaded", function() {
    // Mostrar mensajes de éxito o error si los hay
    if (messages.length > 0) {
        for (let message of messages) {
            if (message.tags.includes('success')) {
                $('#updateSuccessModal').modal('show');
                const updateModalAcceptButton = document.getElementById('updateModalAcceptButton');
                if (updateModalAcceptButton) {
                    updateModalAcceptButton.addEventListener('click', updateLogoutAndRedirect, { once: true });
                }
            } else {
                $('#updateErrorModal').modal('show');
            }
        }
    }

    // Manejar la eliminación del usuario
    const confirmDeleteButton = document.getElementById('confirmDeleteButton');
    if (confirmDeleteButton) {
        confirmDeleteButton.addEventListener('click', handleDeleteUser, { once: true });
    }
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

function handleDeleteUser() {
    fetch(deleteUrl, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        }
    }).then(response => {
        if (response.ok) {
            $('#deleteSuccessModal').modal('show');
            const deleteModalSuccessAcceptButton = document.getElementById('deleteModalSuccessAcceptButton');
            if (deleteModalSuccessAcceptButton) {
                deleteModalSuccessAcceptButton.addEventListener('click', updateLogoutAndRedirect, { once: true });
            }
        } else {
            $('#deleteErrorModal').modal('show');
        }
    }).catch(error => {
        $('#deleteErrorModal').modal('show');
    });
}
