$(document).ready(function () {
    const $email = $('#email');
    const $password = $('#password');
    const schoolId = $('#schoolId');
    const departments = $('#departments');
    const $name = $('#name');

    $.ajax({
        url : 'http://localhost:5001/api/v1/departments',
        method: 'GET',
        success: function (response) {
            $.each(response, function (i, department) {
                departments.append(`<option value="${department.id}">${department.dept_name}</option>`);
            });
        }
    });
    $('#registerationForm').submit(function (event) {
        event.preventDefault();
        $.ajax({
            url: 'http://localhost:5001/api/v1/students/register',
            method: 'POST',
            data: JSON.stringify({
                'email': $email.val(),
                'password': $password.val(),
                'school_id': schoolId.val(),
                'dept_id': departments.val(),
                'name': $name.val()
            }),
            contentType: 'application/json',
            success: function (response) {
                localStorage.setItem('user_id', response.id);
                window.location.href = 'login';
            },
            error: function (response, status, error) {
                console.error(error);
            }
        });
    });
});