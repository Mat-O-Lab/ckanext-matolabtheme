'use strict';

ckan.module('matolabtheme-module', function ($) {
    return {
        initialize: function () {
            console.log('matolabtheme-module initialized!');
            console.log('Element:', this.el);

            const updateCounter = (counter, targetValue) => {
                counter.innerText = '0'; // Start the counter from 0
                counter.setAttribute('data-target', targetValue); // Update data-target attribute

                const duration = +counter.getAttribute('data-duration') * 1000;
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
                const apiUrl = this.el.get(0).getAttribute('data-api-url');
                if (!apiUrl) {
                    console.error('No API URL specified for counter:', this.el);
                    return;
                }

                try {
                    const response = await $.getJSON(apiUrl);
                    let datasetCount = 0;
                    let totalResources = 0;
                    let orgCount = 0;

                    if (response && response.success && response.result) {
                      const result = response.result;
                      // Count datasets, resources, and organizations
                      datasetCount = result.pkg_count || 0; // `pkg_count` for datasets
                      totalResources = result.res_count || 0; // `res_count` for resources
                      orgCount = result.org_count || 0; // `org_count` for organizations
                    } else {
                        console.error('Invalid API response structure:', response);
                    }

                    updateCounter(document.getElementById('dataset_counter'), datasetCount);
                    updateCounter(document.getElementById('resource_counter'), totalResources);
                    updateCounter(document.getElementById('orgs_counter'), orgCount);
                } catch (error) {
                    console.error(`API request to ${apiUrl} failed:`, error);
                }
            };

            fetchAndAnimateCounter();
        },
    };
});
