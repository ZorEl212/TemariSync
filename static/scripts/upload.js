$(document).ready(function () {
    $('#uploadForm').submit(function (event) {
        event.preventDefault();
        var form = document.getElementById('myForm');
        var formData = new FormData(this);
        const title = $('#title').val();
        const discription = $('#description').val();
        const tags = $('#tags').val();
        const course = $('#course').val();
        const coAuthor = $('#coAuthor').val();
        let category;
        const docfile = $('#docfile');

        $('input[type="radio"][name="option"]').each(function () {
            if ($(this).is(':checked')) {
                category = $(this).val();
            }
        });
        // Validity checks for all fields
        if (title.trim() === '') {
            alert('Please enter a title.');
            return;
        }

        if (course.trim() === '') {
            alert('Please enter a course.');
            return;
        }

        if (tags.trim() === '') {
            alert('Please enter tags.');
            return;
        }

        if (coAuthor.trim() === '') {
            alert('Please enter a co-author.');
            return;
        }

        if (!category) {
            alert('Please select a category.');
            return;
        }
        if (discription.trim() === '') {
            alert('Please enter a description.');
            return;
        }
        formData.append('title', title);
        formData.append('description', discription);
        formData.append('tags', tags);
        formData.append('course', course);
        formData.append('coAuthor', coAuthor);
        formData.append('category', category);
        formData.append('file', docfile[0].files[0]);

        $.ajax({
            url: 'http://34.207.190.195/temarisync/api/v1/documents/upload/bd4d3614-f2b0-4f34-b6a6-c6cff2af127e',
            method: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function (response) {
                alert('Your form has been sent successfully.');
            },
            error: function (xhr, status, error) {
                alert('Your form was not sent successfully.');
                console.error(error);
            }
        });
    });
});