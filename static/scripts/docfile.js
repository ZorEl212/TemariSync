$(() => {
    const $title = $('#docTitle');
    const $disc = $('#discription');
    const $tags = $('#tags');
    const $dtitle = $('#title');
    const $course = $('#courseName');
    const $category = $('#category');
    const $fileType = $('#fileType');
    const $author = $('#author');
    const $aNote = $('#note');
    const $download = $('#download');

    const doc_id = new URLSearchParams(window.location.search).get('doc_id');
    let $doc;

    $.ajax({
        type: 'GET',
        url: 'http://172.23.154.146:5001/api/v1/documents/details/' + doc_id,
        data: '{}',
        dataType: 'json',
        success: function (document) {
            $doc = document;
            $title.text(document.title);
            $disc.text(document.description);
            $.each(document.tags, function (i, tag) {
                if (i === 0) {
                    $tags.append(`<span class="text-gray-500">${tag}</span>`);
                } else {
                    $tags.append(`<span class="text-gray-500 ml-2">${tag}</span>`);
                }
                $fileType.text(document.file_type);
                $category.text(document.category);
                $dtitle.text(document.title);
                $aNote.text(document.author_comment);
            });
            $.ajax({
                type: 'GET',
                url: 'http://172.23.154.146:5001/api/v1/courses/' + document.course_id,
                data: '{}',
                dataType: 'json',
                success: function (course) {
                    $course.text(course.name);
                }
            });
            $.ajax({
                type: 'GET',
                url: 'http://172.23.154.146:5001/api/v1/students/' + document.stud_id,
                data: '{}',
                dataType: 'json',
                success: function (student) {
                    $author.text(student.name);
                }
            });
            $download.attr('href', 'http://172.23.154.146:5001/api/v1/documents/download/' + document.stud_id + "/" + doc_id);
        }

    })
});