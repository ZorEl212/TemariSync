$(document).ready(function () {
  const email = $("#email");
  const password = $("#password");
  const toast = document.getElementById("toast");
  $("#loginForm").submit(function (event) {
    if (email.val().includes("example.com")) {
      // Show toast message
    }
    event.preventDefault();
    $.ajax({
      url: "https://yeab.tech/temarisync/api/v1/login",
      method: "POST",
      data: JSON.stringify({
        email: email.val(),
        password: password.val(),
      }),
      contentType: "application/json",
      success: function (response) {
        sessionStorage.setItem("user_id", response.id);
        window.location = "home";
      },
      error: function (response, status, error) {
        console.error(error);
        $("#alertMsg").append("Invalid email or password");
        toast.style.display = "block";
        window.location.href = "#toast";

        // Hide toast after 3 seconds (3000 milliseconds)
        setTimeout(function () {
          toast.style.display = "none";
          $("#alertMsg").empty();
        }, 3000);
      },
    });
  });
});
