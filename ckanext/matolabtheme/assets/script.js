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

      const fetchAndAnimateCounter = async (counter) => {
        const apiUrl = counter.getAttribute("data-api-url");
        if (!apiUrl) {
          console.error("No API URL specified for counter:", counter);
          return;
        }

        try {
          const response = await $.getJSON(apiUrl);
          let targetValue = 0;

          // Parse the count based on the API's response structure
          if (apiUrl.includes("package_search")) {
            // For datasets
            targetValue = response.success && response.result.count !== undefined ? response.result.count : 0;
          } else if (apiUrl.includes("resource_search")) {
            // For resources
            targetValue = response.success && response.result.count !== undefined ? response.result.count : 0;
          } else if (apiUrl.includes("organization_list")) {
            // For organizations
            targetValue = response.success && Array.isArray(response.result) ? response.result.length : 0;
          } else {
            console.error("Unknown API response structure for URL:", apiUrl);
          }

          // Update and animate the counter independently
          updateCounter(counter, targetValue);
        } catch (error) {
          console.error(`API request to ${apiUrl} failed:`, error);
        }
      };

      // Fetch and animate all counters independently
      const counters = this.el.get(0).querySelectorAll(".theme-counter");
      counters.forEach(fetchAndAnimateCounter);
    },
  };
});
