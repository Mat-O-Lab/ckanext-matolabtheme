$(document).ready(function () {
  // Attach keypress listener to all forms
  $(document).on('keydown', function (event) {
    if (event.shiftKey && event.key === 'Enter') {
      event.preventDefault(); // Prevent any default behavior
      // Find the submit button across the entire page or near the current active element
      const button = $(event.target).closest('form').find('.form-actions button[type="submit"]').first();
      if (button.length) {
          button.click(); // Trigger the button's click event
      } 
    }
  });  
});
