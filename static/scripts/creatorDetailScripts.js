$(document).ready(function() {
  $('.toast').toast();
    const stars = $(".star");
    const ratingInput = $("#id_rating");

    stars.on("click", function() {
      const selectedRating = $(this).data("value");
      ratingInput.val(selectedRating);

      // Reset all stars to grey
      stars.removeClass("star-selected");

      // Highlight selected stars
      for (let i = 1; i <= selectedRating; i++) {
        $(`.star[data-value="${i}"]`).addClass("star-selected");
      }
    });

});