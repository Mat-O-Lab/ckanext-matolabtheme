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

      const fetchAndAnimateCounter = async () => {
        const apiUrl = this.el.get(0).getAttribute("data-api-url"); // Fetch the API URL from the parent element
        if (!apiUrl) {
          console.error("No API URL specified for counter:", this.el);
          return;
        }

        try {
          const response = await $.getJSON(apiUrl);
          let datasetCount = 0; // Count of datasets
          let totalResources = 0; // Sum of all resources
          const organizations = new Set(); // To store unique organizations

          // Check if the response is successful and contains results
          if (response.success && Array.isArray(response.result)) {
            datasetCount = response.result.length; // Count of datasets

            // Sum up all resources and collect unique organizations
            response.result.forEach(dataset => {
              if (Array.isArray(dataset.resources)) {
                totalResources += dataset.resources.length; // Count of resources
              }
              if (dataset.organization && dataset.organization.id) {
                organizations.add(dataset.organization.id); // Collect unique organization IDs
              }
            });
          } else {
            console.error("Invalid API response structure:", response);
          }

          // Update and animate the counters independently
          updateCounter(document.getElementById("dataset_counter"), datasetCount); // For datasets
          updateCounter(document.getElementById("resource_counter"), totalResources); // For resources
          updateCounter(document.getElementById("orgs_counter"), organizations.size); // For unique organizations
        } catch (error) {
          console.error(`API request to ${apiUrl} failed:`, error);
        }
      };

      // Fetch and animate the counters
      fetchAndAnimateCounter(); // Call the function to fetch and animate counters

      // Animate individual counters (if needed)
      const counters = this.el.get(0).querySelectorAll(".theme-counter");
      counters.forEach(counter => {
        updateCounter(counter, 0); // Initialize counters to 0
      });
    },
  };
});