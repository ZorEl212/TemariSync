$(document).ready(function () {
    const title = $('#title');
    const description = $('#description');
    const tags = $('#tags');
    const course = $('#course');
    const coAuthor = $('#coAuthor');
    let category;
    const cancel = $('#cancel');
    const user_id = sessionStorage.getItem('user_id');
    const doc_id = new URLSearchParams(window.location.search).get('doc_id');
    let course_id;
    $.ajax({
        url: 'https://yeab.tech/temarisync/api/v1/documents/details/' + doc_id,
        method: 'GET',
        success: function (response) {
            if (title.val().trim() === '') {
                title.val(response.title);
            }
            if (course.val().trim() === '') {
                $.ajax({
                    url: 'https://yeab.tech/temarisync/api/v1/courses/' + response.course_id,
                    method: 'GET',
                    success: function (crs) {
                        course.val(crs.name);
                        course_id = crs.id;
                    }
                });
            }
            if (tags.val().trim() === '') {
                let tagconcat;
                $.each(response.tags, function (i, tag) {
                    tagconcat += tag + " ";
                })
                tagconcat = tagconcat.trim();
                tagconcat =tagconcat.replaceAll('undefined', '');
                tagconcat = '#' + tagconcat.replaceAll(' ', '#');
                tags.val(tagconcat);
            }

            if (!category) {
                $('input[type="radio"][name="option"]').each(function () {
                    if ($(this).val().toLowerCase() === response.category.toLowerCase()) {
                        $(this).prop('checked', true);
                    }
                })
            }
            if (description.val().trim() === '') {
                description.val(response.description);
                } 
            if ($('#authorsNote').val().trim() === '') {
                $('#authorsNote').val(response.author_comment);
            } 
        },
        error: function (response, status, error) {
            console.error(error);
        }
    });

    $('#editForm').submit(function (event) {
        event.preventDefault();
        var formData = new FormData(this);
        $.ajax({
            url: 'https://yeab.tech/temarisync/api/v1/courses/',
            method: 'GET',
            success: function (response) {
                var validCourse = false;
                $.each(response, function (i, crs) {
                    if (crs.name.toLowerCase() === $('#course').val().toLowerCase()) {
                        course_id = crs.id;
                        console.log(course.val());
                        validCourse = true;
                        return false; 
                    }
                });
                if (!validCourse) {
                    alert('Please enter a valid course.');
                    console.error(crs.name);
                    return;
                }
                formData.append('course_id', course_id);
                formData.append('title', title.val());
                formData.append('description', description.val());
                formData.append('tags', tags.val());
                $('input[type="radio"][name="option"]').each(function () {
                    if ($(this).is(':checked')) {
                        category = $(this).val();
                    }
                });
                formData.append('category', category);
                formData.append('author_comment', $('#authorsNote').val());
                formData.append('co_author', coAuthor.val());
                formData.append('user_id', user_id);
            
                $.ajax({
                    url: 'https://yeab.tech/temarisync/api/v1/documents/' + user_id + '/' + doc_id,
                    method: 'PUT',
                    contentType: 'application/json',
                    data: JSON.stringify(Object.fromEntries(formData)),
                    processData: false,
                    success: function (response) {
                        alert('Document successfully updated.');
                        window.location.href = '/temarisync/docfile?doc_id=' + doc_id + '&user_id=' + user_id;
                    },
                    error: function (response, status, error) {
                        if (response.status === 401 || response.status === 403) {
                            alert('You are not authorized to edit this document.');
                        }
                    }
                });
            }
            
        })
        
    });
    cancel.click(function () {
        window.location.href = '/temarisync/docfile?doc_id=' + doc_id + '&user_id=' + user_id;
    });
});