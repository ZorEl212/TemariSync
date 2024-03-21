$(document).ready(function () {
  $.ajax({
    url: "https://yeab.tech/temarisync/api/v1/courses/",
    method: "GET",
    success: function (response) {
      var validCourse = false;
      $.each(response, function (i, crs) {
        $course.append(`<option value="${crs.id}">${crs.name}</option>`);
      });
      if ($course.val() !== "Select Course") {
        validCourse = true;
      }
      if (!validCourse) {
        alert("Please enter a valid course.");
        console.error(crs.name);
        return;
      }
    },
    error: function (xhr, status, error) {
      alert("Error occured please try again later.");
      console.error(error);
    }
  });

  const $title = $("#title")
  const $discription = $("#description")
  const $tags = $("#tags")
  let $course = $("#course");
  const $coAuthor = $("#coAuthor")
  let category;
  const $docfile = $("#docfile");
  const user_id = sessionStorage.getItem("user_id");

  $("#uploadForm").submit(function (event) {
    event.preventDefault();
    var formData = new FormData(this);
    $('input[type="radio"][name="option"]').each(function () {
      if ($(this).is(":checked")) {
        category = $(this).val();
      }
    });
    // Validity checks for all fields
    if ($title.val().trim() === "") {
      alert("Please enter a title.");
      return;
    }

    if ($tags.val().trim() === "") {
      alert("Please enter tags.");
      return;
    }

    if (!category) {
      alert("Please select a category.");
      return;
    }
    if ($discription.val().trim() === "") {
      alert("Please enter a description.");
      return;
    }
    if ($("#authorsNote").val().trim() === "") {
      alert(`Please enter Author's note.`);
      return;
    }

    if ($docfile[0].files.length === 0) {
      alert("Please select a file to upload.");
      return;
    }
    if (
      sessionStorage.getItem("user_id") === null ||
      sessionStorage.getItem("user_id") === "null"
    ) {
      alert("Please login to upload a document.");
      return;
    }

    formData.append("title", $title.val());
    formData.append("description", $discription.val());
    formData.append("tags", $tags.val());
    formData.append("course_id", $course.val());
    formData.append("coAuthor", $coAuthor.val());
    formData.append("category", category);
    formData.append("author_comment", $("#authorsNote").val());
    formData.append("stud_id", sessionStorage.getItem("user_id"));
    formData.append("file", $docfile[0].files[0]);

    $.ajax({
      url: "https://yeab.tech/temarisync/api/v1/documents/upload/" + user_id,
      method: "POST",
      data: formData,
      processData: false,
      contentType: false,
      success: function (response) {
        $("#successModal").css("display", "");
        $("#gotIt").click(function () {
          window.location.href = "home";
        });
      },
      error: function (xhr, status, error) {
        alert("Error occured please try again later.");
        console.error(error);
      },
    });
  });
  $("#cancel").click(function () {
    window.location.href = "home";
  });
});
