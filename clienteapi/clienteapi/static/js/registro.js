document.addEventListener("DOMContentLoaded", function() {
    const passwordField = document.getElementById('id_password1');
    const passwordHelpBlock = document.getElementById('passwordHelpBlock');

    passwordField.addEventListener('input', function() {
        const password = passwordField.value;
        let message = '';

        if (password.length < 8) {
            message = 'La contraseña es demasiado corta. Debe contener al menos 8 caracteres.';
        } else if (/^\d+$/.test(password)) {
            message = 'La contraseña es completamente numérica.';
        } else if (['password', '12345678', 'qwerty'].includes(password)) {
            message = 'Esta contraseña es demasiado común.';
        } else {
            message = '';
        }

        passwordHelpBlock.textContent = message;
    });
});


