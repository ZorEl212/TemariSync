$(document).ready(function () {
  const $email = $("#email");
  const $password = $("#password");
  const schoolId = $("#schoolId");
  const departments = $("#departments");
  const $name = $("#name");
  const toast = document.getElementById("toast");

  $.ajax({
    url: "https://yeab.tech/temarisync/api/v1/departments",
    method: "GET",
    success: function (response) {
      $.each(response, function (i, department) {
        departments.append(
          `<option value="${department.id}">${department.dept_name}</option>`
        );
      });
    },
  });
  $("#registerationForm").submit(function (event) {
    event.preventDefault();
    if (
      departments.val() === "Select Department" ||
      departments.val() === null
    ) {
      $("#alertMsg").append("Please select a department");
      toast.style.display = "block";
      window.location.href = "#" + "toast";

      // Hide toast after 3 seconds (3000 milliseconds)
      setTimeout(function () {
        toast.style.display = "none";
        $("#alertMsg").empty();
      }, 3000);
      return;
    }

    $.ajax({
      url: "https://yeab.tech/temarisync/api/v1/students/register",
      method: "POST",
      data: JSON.stringify({
        email: $email.val(),
        password: $password.val(),
        school_id: schoolId.val(),
        dept_id: departments.val(),
        name: $name.val(),
      }),
      contentType: "application/json",
      success: function (response) {
        window.location.href = "login";
      },
      error: function (response, status, error) {
        console.error(error);
        if (response.status === 400) {
          $("#alertMsg").append(
            "The email address is already in use. Please enter a different email."
          );
          toast.style.display = "block";
          window.location.href = "#" + "toast";

          // Hide toast after 3 seconds (3000 milliseconds)
          setTimeout(function () {
            toast.style.display = "none";
            $("#alertMsg").empty();
          }, 3000);
        }
      },
    });
  });
});
