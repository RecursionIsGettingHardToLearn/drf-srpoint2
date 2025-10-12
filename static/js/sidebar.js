document.addEventListener("DOMContentLoaded", function () {
  const body = document.body;
  const sidebar = document.querySelector(".sidebar");
  const toggle = document.getElementById("sidebarToggle");

  if (toggle) {
    toggle.addEventListener("click", (e) => {
      e.preventDefault();
      body.classList.toggle("show-sidebar");
      toggle.classList.toggle("active");
    });
  }

  // Cierra el sidebar si haces click fuera de él
  document.addEventListener("click", (e) => {
    if (
      sidebar &&
      !sidebar.contains(e.target) &&
      !e.target.closest("#sidebarToggle") &&
      body.classList.contains("show-sidebar")
    ) {
      body.classList.remove("show-sidebar");
      toggle.classList.remove("active");
    }
  });
});
