function decreaseValue() {
    var input = document.getElementById('number');
    var value = parseInt(input.value);
  
    if (value > 1) {
      value--;
      input.value = value;
    }
  }
  
function increaseValue() {
    var input = document.getElementById('number');
    var value = parseInt(input.value);

    value++;
    input.value = value;
}

function updateRating(rating) {
    const stars = document.querySelectorAll('.rating .star');
    const numericRating = parseFloat(rating);
  
    stars.forEach((star, index) => {
      const starValue = index + 1;
  
      if (starValue <= Math.floor(numericRating)) {
        star.classList.add('filled');
        star.classList.remove('half-filled');
      } else if (starValue === Math.ceil(numericRating)) {
        star.classList.add('half-filled');
        star.classList.remove('filled');
      } else {
        star.classList.remove('filled');
        star.classList.remove('half-filled');
      }
    });
}
  
  
  
  