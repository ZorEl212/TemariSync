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
        toast.style.display = "block";

        // Hide toast after 3 seconds (3000 milliseconds)
        setTimeout(function () {
          toast.style.display = "none";
        }, 3000);
      },
    });
  });
});
