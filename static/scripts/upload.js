$(document).ready(function () {
    $('#uploadForm').submit(function (event) {
        event.preventDefault();
        var form = document.getElementById('myForm');
        var formData = new FormData(this);
        const title = $('#title').val();
        const discription = $('#description').val();
        const tags = $('#tags').val();
        let course = $('#course').val();
        const coAuthor = $('#coAuthor').val();
        let category;
        const docfile = $('#docfile');
        const caancel = $('#cancel');
        const user_id = localStorage.getItem('user_id');
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

        if (!category) {
            alert('Please select a category.');
            return;
        }
        if (discription.trim() === '') {
            alert('Please enter a description.');
            return;
        }
        if ($('#authorsNote').val().trim() === '') {
            alert(`Please enter Author's note.`);
            return;
        }

        if (docfile[0].files.length === 0) {
            alert('Please select a file to upload.');
            return;
        }
        if (localStorage.getItem('user_id') === null || localStorage.getItem('user_id') === 'null') {
            alert('Please login to upload a document.');
            return;
        }
        $.ajax({
            url: 'http://34.207.190.195/temarisync/api/v1/courses/',
            method: 'GET',
            success: function (response) {
                var validCourse = false;
                $.each(response, function (i, crs) {
                    if (crs.name.toLowerCase() === course.toLowerCase()) {
                        course = crs.id;
                        validCourse = true;
                        return false; // Exit the loop early since a match is found
                    }
                });
                if (!validCourse) {
                    alert('Please enter a valid course.');
                    console.error(crs.name);
                    return;
                }
        
                formData.append('title', title);
                formData.append('description', discription);
                formData.append('tags', tags);
                formData.append('course_id', course);
                formData.append('coAuthor', coAuthor);
                formData.append('category', category);
                formData.append('author_comment', $('#author_comment').val());
                formData.append('stud_id', localStorage.getItem('user_id'));
                formData.append('file', docfile[0].files[0]);
        
                $.ajax({
                    url: 'http://34.207.190.195/temarisync/api/v1/documents/upload/' + user_id,
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
            },
            error: function (xhr, status, error) {
                console.error(error);
                exit()
            }
        });
        
    });
});