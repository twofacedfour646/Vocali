$(document).ready(function() {
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

    // Get the creator's bio
    const bio = $(".creator-bio").text();
    // Check if bio is longer than 500 characters
    if (bio.length > 500) {
      // Substring the bio
      $(".creator-bio").text(bio.substring(0, 500) + "...");

      // Create show more/less element
      const showElement = $("<span class='fw-bold text-primary bio-btn'>Show more</span>")

      // Move show more/less elements after bio
      $(".creator-bio").after(showElement);
    }

    // Bio visiblitiy flag
    let fullBio = false;

    // Check if show more/less has been clicked
    $(".bio-btn").on("click", function() {
      // Switch fullBio flag
      fullBio = !fullBio;
      $(".creator-bio").text(fullBio ? bio : bio.substring(0, 500) + "...");
      $(".bio-btn").text(fullBio ? "Show less" : "Show more");
    });

});