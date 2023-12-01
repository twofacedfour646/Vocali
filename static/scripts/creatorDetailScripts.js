$(document).ready(function() {
    const stars = $(".star");
    const ratingInput = $("#id_rating");

    stars.on("click", function() {
      const selectedRating = $(this).data("value");
      ratingInput.val(selectedRating);

      console.log(ratingInput[0].value);

      // Reset all stars to grey
      stars.removeClass("selected");

      // Highlight selected stars
      for (let i = 1; i <= selectedRating; i++) {
        $(`.star[data-value="${i}"]`).addClass("selected");
      }
    });
});