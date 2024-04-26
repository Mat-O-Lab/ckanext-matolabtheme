ckan.module("matolabtheme-module", function ($, _) {
  "use strict";
  return {
    options: {
      debug: false,
    },
    initialize: function () {
      console.log("Initialized Counter Aniation for element: ", this.el);
      const counters = this.el.get(0).querySelectorAll('.theme-counter')
      // this.el.querySelectorAll(".theme-counter");
      counters.forEach((counter) => {
        console.log("counter element: ", counter);
        counter.innerText = "0";
        const updateCounter = () => {
          const target = +counter.getAttribute("data-target");
          const count = +counter.innerText;
          const increment = target / 200;
          if (count < target) {
            counter.innerText = `${Math.ceil(count + increment)}`;
            setTimeout(updateCounter, 1);
          } else counter.innerText = target;
        };
        updateCounter();
      });
    },
  };
});
