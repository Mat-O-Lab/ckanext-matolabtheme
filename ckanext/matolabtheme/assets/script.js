ckan.module("matolabtheme-module", function ($, _) {
  "use strict";
  return {
    options: {
      debug: false,
    },
    initialize: function () {
      console.log("Initialized Counter Animation for element: ", this.el);
      const counters = this.el.get(0).querySelectorAll('.theme-counter')
      // this.el.querySelectorAll(".theme-counter");
      counters.forEach((counter) => {
        console.log("counter element: ", counter);
        counter.innerText = "0";
        const updateCounter = () => {
          const target = +counter.getAttribute("data-target");
          const duration = +counter.getAttribute("data-duration") * 1000;
          const count = +counter.innerText;
          const increment = (target - count) / duration * 10;
          const currentTime = Date.now();
          const endTime = currentTime + duration;
          const animate = () => {
            const remaining = Math.max((endTime - Date.now()) / duration, 0);
            const currentCount = Math.round(target - (target - count) * remaining);
            counter.innerText = currentCount;
            if (remaining > 0) {
              requestAnimationFrame(animate);
            }
          };
          requestAnimationFrame(animate);
        };
        updateCounter();
      });
    },
  };
});
