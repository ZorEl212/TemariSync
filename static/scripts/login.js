$(document).ready(function () {
    const email = $('#email');
    const password = $('#password');
    $('#loginForm').submit(function (event) {
        event.preventDefault();
        $.ajax({
            url: 'https://yeab.tech/temarisync/api/v1/login',
            method: 'POST',
            data: JSON.stringify({
                'email': email.val(),
                'password': password.val()
            }),
            contentType: 'application/json',
            success: function (response) {
                localStorage.setItem('user_id', response.id);
                window.location = 'home'
            },
            error: function (response, status, error) {
                console.error(error);
            }
        });
    });
});
