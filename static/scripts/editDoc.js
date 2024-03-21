$(document).ready(function () {
  const title = $("#title");
  const description = $("#description");
  const tags = $("#tags");
  const course = $("#course");
  const coAuthor = $("#coAuthor");
  let category;
  const cancel = $("#cancel");
  const user_id = sessionStorage.getItem("user_id");
  const doc_id = new URLSearchParams(window.location.search).get("doc_id");

  $.ajax({
    url: "https://yeab.tech/temarisync/api/v1/courses/",
    method: "GET",
    success: function (response) {
      $.each(response, function (i, crs) {
        course.append(`<option value="${crs.id}">${crs.name}</option>`);
      });
    },
  });
  $.ajax({
    url: "https://yeab.tech/temarisync/api/v1/documents/details/" + doc_id,
    method: "GET",
    success: function (response) {
      if (title.val().trim() === "") {
        title.val(response.title);
      }
      if (course.val() === "Select Course" || course.val() === null) {
        course.val(response.course_id);
      }
      if (tags.val().trim() === "") {
        let tagconcat;
        $.each(response.tags, function (i, tag) {
          tagconcat += tag + " ";
        });
        tagconcat = tagconcat.trim();
        tagconcat = tagconcat.replaceAll("undefined", "");
        tagconcat = "#" + tagconcat.replaceAll(" ", "#");
        tags.val(tagconcat);
      }

      if (!category) {
        $('input[type="radio"][name="option"]').each(function () {
          if ($(this).val().toLowerCase() === response.category.toLowerCase()) {
            $(this).prop("checked", true);
          }
        });
      }
      if (description.val().trim() === "") {
        description.val(response.description);
      }
      if ($("#authorsNote").val().trim() === "") {
        $("#authorsNote").val(response.author_comment);
      }
    },
    error: function (response, status, error) {
      console.error(error);
    },
  });

  $("#editForm").submit(function (event) {
    event.preventDefault();
    let validCourse = false;
    var formData = new FormData(this);
    if (course.val() !== "Select Course") {
      validCourse = true;
    }
    if (!validCourse) {
      alert("Please enter a valid course.");
      console.error(crs.name);
      return;
    }
    if (validCourse) {
      formData.append("course_id", course.val());
      formData.append("title", title.val());
      formData.append("description", description.val());
      formData.append("tags", tags.val());
      $('input[type="radio"][name="option"]').each(function () {
        if ($(this).is(":checked")) {
          category = $(this).val();
        }
      });
      formData.append("category", category);
      formData.append("author_comment", $("#authorsNote").val());
      formData.append("co_author", coAuthor.val());
      formData.append("user_id", user_id);

      $.ajax({
        url:
          "https://yeab.tech/temarisync/api/v1/documents/" +
          user_id +
          "/" +
          doc_id,
        method: "PUT",
        contentType: "application/json",
        data: JSON.stringify(Object.fromEntries(formData)),
        processData: false,
        success: function (response) {
          $("#successModal").css("display", "");
          $("#gotIt").click(function () {
            window.location.href =
              "/temarisync/docfile?doc_id=" + doc_id + "&user_id=" + user_id;
          });
        },
        error: function (response, status, error) {
          if (response.status === 401 || response.status === 403) {
            alert("You are not authorized to edit this document.");
          }
        },
      });
    }
  });
  cancel.click(function () {
    window.location.href =
      "/temarisync/docfile?doc_id=" + doc_id + "&user_id=" + user_id;
  });
});
