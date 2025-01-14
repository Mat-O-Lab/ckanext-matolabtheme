ckan.module("matolabtheme-module", function ($, _) {
  "use strict";
  return {
    options: {
      debug: false,
    },
    initialize: function () {
      console.log("Initialized Counter Animation for element: ", this.el);

      const updateCounter = (counter, targetValue) => {
        counter.innerText = "0"; // Start the counter from 0
        counter.setAttribute("data-target", targetValue); // Update data-target attribute

        const duration = +counter.getAttribute("data-duration") * 1000;
        const increment = targetValue / (duration / 10);
        let count = 0;

        const animate = () => {
          count += increment;

          if (count >= targetValue) {
            counter.innerText = targetValue; // Final value
          } else {
            counter.innerText = Math.ceil(count); // Animated value
            requestAnimationFrame(animate);
          }
        };

        requestAnimationFrame(animate);
      };

      const fetchAndAnimateCounter = (counter) => {
        const apiUrl = counter.getAttribute("data-api-url");
        if (!apiUrl) {
          console.error("No API URL specified for counter:", counter);
          return;
        }

        $.getJSON(apiUrl, function (data) {
          let targetValue = 0;

          // Parse the count based on the API's response structure
          if (apiUrl.includes("package_search")) {
            // For datasets
            targetValue = data.success && data.result.count !== undefined ? data.result.count : 0;
          } else if (apiUrl.includes("resource_search")) {
            // For resources
            targetValue = data.success && data.result.count !== undefined ? data.result.count : 0;
          } else if (apiUrl.includes("organization_list")) {
            // For organizations
            targetValue = data.success && Array.isArray(data.result) ? data.result.length : 0;
          } else {
            console.error("Unknown API response structure for URL:", apiUrl);
          }

          updateCounter(counter, targetValue);
        }).fail(function (xhr, status, error) {
          console.error(`API request to ${apiUrl} failed:`, status, error);
        });
      };

      // Fetch and animate all counters
      const counters = this.el.get(0).querySelectorAll(".theme-counter");
      counters.forEach(fetchAndAnimateCounter);
    },
  };
});