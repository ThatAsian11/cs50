$(function () {
  $('[data-toggle="popover"]').popover()
})

$(function () {
  $('[data-toggle="tooltip"]').tooltip()
})

document.addEventListener('DOMContentLoaded', () => {
  window.onload = function(){
  const display = () => {
  document.getElementById('trending_container').style.visibility = "visible";
}
setTimeout(display(), 3000);

  };
});
