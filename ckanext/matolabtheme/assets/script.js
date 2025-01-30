$(document).ready(function () {
  let hoveredForm = null;

  // Track which form the mouse is currently over
  $(document).on('mouseenter', 'form', function () {
    hoveredForm = $(this);
  });

  $(document).on('mouseleave', 'form', function () {
    hoveredForm = null;
  });

  // Listen for Shift + Enter keypress
  $(document).on('keydown', function (event) {
    if (event.shiftKey && event.key === 'Enter') {
      event.preventDefault(); // Prevent default behavior

      // Find the submit button in the hovered form (or the focused form)
      const form = hoveredForm || $(event.target).closest('form');
      const button = form.find('.form-actions button[type="submit"]').last();

      if (button.length) {
        button.click(); // Trigger the button's click event
      }
    }
  });
});
