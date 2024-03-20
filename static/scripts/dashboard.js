$(() => {
  $.ajax({
    url: "https://yeab.tech/temarisync/api/v1/checkuser",
    method: "GET",
    success: function (response, status, xhr) {
      if (xhr.status === 200) {
        console.log(response);
      }
    },
    error: function (xhr, status, error) {
        console.error(error);
        if (xhr.status === 401)
        {
            localStorage.removeItem("user_id");
            window.location.href = "login";
        }
    },
  });

  const $assignments = $("#assignments");
  const $projects = $("#projects");
  const $materials = $("#materials");
  $assignments.attr("href", "docs?category=assignment");
  $projects.attr("href", "docs?category=project");
  $materials.attr("href", "docs?category=material");
  $('$logout').attr('href', 'login');

  $("#logout").click(() => {
    $.ajax({
      url: "https://yeab.tech/temarisync/api/v1/logout",
      method: "GET",
      success: function (response) {
        localStorage.removeItem("user_id");
        window.location.href = "login";
      },
      error: function (xhr, status, error) {
        console.error(error);
      },
    });
  });
});
