$(document).ready(function () {
  var scrollTopButton = document.getElementById("scroll-to-top-button");

  window.onscroll = function () {
    scrollFunction();
  };

  function scrollFunction() {
    if (
      document.body.scrollTop > 20 ||
      document.documentElement.scrollTop > 20
    ) {
      scrollTopButton.style.display = "block";
    } else {
      scrollTopButton.style.display = "none";
    }
  }

  $("#scroll-to-top-button").click(function () {
    $("html ,body").animate({ scrollTop: 0 }, 800);
  });
});
