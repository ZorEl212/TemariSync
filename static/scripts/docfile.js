$(() => {
  const $title = $("#docTitle");
  const $disc = $("#discription");
  const $tags = $("#tags");
  const $dtitle = $("#title");
  const $course = $("#courseName");
  const $category = $("#category");
  const $fileType = $("#fileType");
  const $author = $("#author");
  const $aNote = $("#note");
  const $download = $("#download");
  const $editDocInfo = $("#editDocInfo");
  const $deleteDoc = $("#deleteDoc");
  const $container = $("#container");

  const doc_id = new URLSearchParams(window.location.search).get("doc_id");
  const user_id = sessionStorage.getItem("user_id");
  let $doc;

  $.ajax({
    type: "GET",
    url: "https://yeab.tech/temarisync/api/v1/documents/details/" + doc_id,
    data: "{}",
    dataType: "json",
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
        if (document.stud_id === user_id) {
          $editDocInfo.css("display", "");
          $deleteDoc.css("display", "");
        }
      });
      $.ajax({
        type: "GET",
        url:
          "https://yeab.tech/temarisync/api/v1/courses/" + document.course_id,
        data: "{}",
        dataType: "json",
        success: function (course) {
          $course.text(course.name);
        },
      });
      $.ajax({
        type: "GET",
        url: "https://yeab.tech/temarisync/api/v1/students/" + document.stud_id,
        data: "{}",
        dataType: "json",
        success: function (student) {
          $author.text(student.name);
        },
      });
      $download.attr(
        "href",
        "https://yeab.tech/temarisync/api/v1/documents/download/" +
          document.stud_id +
          "/" +
          doc_id
      );
    },
  });
  $deleteDoc.click(function () {
    $("#confirmDelete").css("display", "");
    $("#cancel").off("click");
    $("#confirm").off("click");
    $("#cancel").click(function () {
      $container.find("#confirmDelete").css("display", "none");
    });
    $("#confirm").click(function () {
      $.ajax({
        type: "DELETE",
        url:
          "https://yeab.tech/temarisync/api/v1/documents/" +
          user_id +
          "/" +
          doc_id,
        success: function (response) {
          window.location.href = "docs?filter=all";
        },
        error: function (response, status, error) {
          if (response.status === 401 || response.status === 403) {
            alert("You are not authorized to delete this document.");
          }
        },
      });
    });
  });
  $editDocInfo.click(function () {
    window.location.href = "editdoc?doc_id=" + doc_id;
  });
});
