document.addEventListener("DOMContentLoaded", function() {
  /**
   * HomePage - Help section
   */
  class Help {
    constructor($el) {
      this.$el = $el;
      this.$buttonsContainer = $el.querySelector(".help--buttons");
      this.$slidesContainers = $el.querySelectorAll(".help--slides");
      this.currentSlide = this.$buttonsContainer.querySelector(".active").parentElement.dataset.id;
      this.init();
    }

    init() {
      this.events();
    }

    events() {
      /**
       * Slide buttons
       */
      this.$buttonsContainer.addEventListener("click", e => {
        if (e.target.classList.contains("btn")) {
          this.changeSlide(e);
        }
      });

      /**
       * Pagination buttons
       */
      this.$el.addEventListener("click", e => {
        if (e.target.classList.contains("btn") && e.target.parentElement.parentElement.classList.contains("help--slides-pagination")) {
          this.changePage(e);
        }
      });
    }

    changeSlide(e) {
      e.preventDefault();
      const $btn = e.target;

      // Buttons Active class change
      [...this.$buttonsContainer.children].forEach(btn => btn.firstElementChild.classList.remove("active"));
      $btn.classList.add("active");

      // Current slide
      this.currentSlide = $btn.parentElement.dataset.id;

      // Slides active class change
      this.$slidesContainers.forEach(el => {
        el.classList.remove("active");

        if (el.dataset.id === this.currentSlide) {
          el.classList.add("active");
        }
      });
    }

    /**
     * TODO: callback to page change event
     */
    changePage(e) {
      e.preventDefault();
      const $btn = e.target;
      const page = $btn.getAttribute("href").split("=")[1];

      console.log(page); // logowanie numeru strony

      // Pobranie danych za pomocą AJAX
      fetch(`${window.location.pathname}?page_${this.getSlideType()}=${page}`)
        .then(response => response.text())
        .then(html => {
          const parser = new DOMParser();
          const doc = parser.parseFromString(html, 'text/html');
          const newContent = doc.querySelector(`.help--slides[data-id="${this.currentSlide}"]`);
          const currentContent = this.$el.querySelector(`.help--slides[data-id="${this.currentSlide}"]`);
          currentContent.innerHTML = newContent.innerHTML;
        })
        .catch(error => console.error('Błąd:', error));
    }

    getSlideType() {
      if (this.currentSlide == "1") return "fundations";
      if (this.currentSlide == "2") return "organizations";
      if (this.currentSlide == "3") return "collections";
    }
  }

  const helpSection = document.querySelector(".help");
  if (helpSection !== null) {
    new Help(helpSection);
  }

  /**
   * Form Select
   */
  class FormSelect {
    constructor($el) {
      this.$el = $el;
      this.options = [...$el.children];
      this.init();
    }

    init() {
      this.createElements();
      this.addEvents();
      this.$el.parentElement.removeChild(this.$el);
    }

    createElements() {
      // Input for value
      this.valueInput = document.createElement("input");
      this.valueInput.type = "text";
      this.valueInput.name = this.$el.name;

      // Dropdown container
      this.dropdown = document.createElement("div");
      this.dropdown.classList.add("dropdown");

      // List container
      this.ul = document.createElement("ul");

      // All list options
      this.options.forEach((el, i) => {
        const li = document.createElement("li");
        li.dataset.value = el.value;
        li.innerText = el.innerText;

        if (i === 0) {
          // First clickable option
          this.current = document.createElement("div");
          this.current.innerText = el.innerText;
          this.dropdown.appendChild(this.current);
          this.valueInput.value = el.value;
          li.classList.add("selected");
        }

        this.ul.appendChild(li);
      });

      this.dropdown.appendChild(this.ul);
      this.dropdown.appendChild(this.valueInput);
      this.$el.parentElement.appendChild(this.dropdown);
    }

    addEvents() {
      this.dropdown.addEventListener("click", e => {
        const target = e.target;
        this.dropdown.classList.toggle("selecting");

        // Save new value only when clicked on li
        if (target.tagName === "LI") {
          this.valueInput.value = target.dataset.value;
          this.current.innerText = target.innerText;
        }
      });
    }
  }
  document.querySelectorAll(".form-group--dropdown select").forEach(el => {
    new FormSelect(el);
  });

  /**
   * Hide elements when clicked on document
   */
  document.addEventListener("click", function(e) {
    const target = e.target;
    const tagName = target.tagName;

    if (target.classList.contains("dropdown")) return false;

    if (tagName === "LI" && target.parentElement.parentElement.classList.contains("dropdown")) {
      return false;
    }

    if (tagName === "DIV" && target.parentElement.classList.contains("dropdown")) {
      return false;
    }

    document.querySelectorAll(".form-group--dropdown .dropdown").forEach(el => {
      el.classList.remove("selecting");
    });
  });

  /**
   * Switching between form steps
   */
  class FormSteps {
    constructor(form) {
      this.$form = form;
      this.$next = form.querySelectorAll(".next-step");
      this.$prev = form.querySelectorAll(".prev-step");
      this.$step = form.querySelector(".form--steps-counter span");
      this.currentStep = 1;

      this.$stepInstructions = form.querySelectorAll(".form--steps-instructions p");
      const $stepForms = form.querySelectorAll("form > div");
      this.slides = [...this.$stepInstructions, ...$stepForms];

      this.init();
    }

    /**
     * Init all methods
     */
    init() {
      this.events();
      this.updateForm();
    }

    /**
     * All events that are happening in form
     */
    events() {
      // Next step
      this.$next.forEach(btn => {
        btn.addEventListener("click", e => {
          e.preventDefault();
          this.currentStep++;
          if (this.currentStep === 5) {
            this.collectSummaryData();
          }
          this.updateForm();
        });
      });

      // Previous step
      this.$prev.forEach(btn => {
        btn.addEventListener("click", e => {
          e.preventDefault();
          this.currentStep--;
          this.updateForm();
        });
      });

      // Form submit
      this.$form.querySelector("form").addEventListener("submit", e => this.submit(e));
    }

    /**
     * Update form front-end
     * Show next or previous section etc.
     */
    updateForm() {
      this.$step.innerText = this.currentStep;

      // TODO: Validation

      this.slides.forEach(slide => {
        slide.classList.remove("active");

        if (slide.dataset.step == this.currentStep) {
          slide.classList.add("active");
        }
      });

      this.$stepInstructions[0].parentElement.parentElement.hidden = this.currentStep >= 6;
      this.$step.parentElement.hidden = this.currentStep >= 6;

      // Filter institutions based on selected categories
      if (this.currentStep == 3) {
        const selectedCategories = [...this.$form.querySelectorAll('[data-step="1"] input[type="checkbox"]:checked')]
          .map(input => input.value);

        console.log('Selected Categories:', selectedCategories);

        this.$form.querySelectorAll('.institution').forEach(institution => {
          const institutionCategories = institution.dataset.categories.split(',');
          console.log('Institution Categories:', institutionCategories);
          const isVisible = selectedCategories.some(category => institutionCategories.includes(category));
          institution.style.display = isVisible ? 'block' : 'none';
        });
      }

      // TODO: get data from inputs and show them in summary
    }

    /**
     * Collect data from the form and show them in summary
     */
    collectSummaryData() {
      const summary = {
        categories: [],
        bags: this.$form.querySelector('input[name="bags"]').value,
        organization: '',
        address: {
          street: '',
          city: '',
          postcode: '',
          phone: '',
        },
        pickup: {
          date: '',
          time: '',
          more_info: '',
        },
      };

      // Pobierz wybrane organizacje
      const organizationInput = this.$form.querySelector('input[name="organization"]:checked');
      if (organizationInput) {
        console.log('organizationInput:', organizationInput);
        const organizationDescription = organizationInput.nextElementSibling.nextElementSibling;
        console.log('organizationDescription:', organizationDescription);
        const organizationTitle = organizationDescription ? organizationDescription.querySelector('.title') : null;
        console.log('organizationTitle:', organizationTitle);
        if (organizationTitle) {
          summary.organization = organizationTitle.innerText.trim();
        }
      }

      summary.address.street = this.$form.querySelector('input[name="address"]').value;
      summary.address.city = this.$form.querySelector('input[name="city"]').value;
      summary.address.postcode = this.$form.querySelector('input[name="postcode"]').value;
      summary.address.phone = this.$form.querySelector('input[name="phone"]').value;
      summary.pickup.date = this.$form.querySelector('input[name="data"]').value;
      summary.pickup.time = this.$form.querySelector('input[name="time"]').value;
      summary.pickup.more_info = this.$form.querySelector('textarea[name="more_info"]').value;

      this.$form.querySelectorAll('[data-step="1"] input[type="checkbox"]:checked').forEach(input => {
        summary.categories.push(input.nextElementSibling.nextElementSibling.innerText.trim());
      });

      console.log('Summary:', summary);

      // Update the summary view
      const summaryContainer = this.$form.querySelector('.summary');
      summaryContainer.innerHTML = `
        <div class="form-section">
          <h4>Oddajesz:</h4>
          <ul>
            <li>
              <span class="icon icon-bag"></span>
              <span class="summary--text">${summary.bags} worki ${summary.categories.join(', ')}</span>
            </li>
            <li>
              <span class="icon icon-hand"></span>
              <span class="summary--text">Dla fundacji ${summary.organization}</span>
            </li>
          </ul>
        </div>
        <div class="form-section form-section--columns">
          <div class="form-section--column">
            <h4>Adres odbioru:</h4>
            <ul>
              <li>${summary.address.street}</li>
              <li>${summary.address.city}</li>
              <li>${summary.address.postcode}</li>
              <li>${summary.address.phone}</li>
            </ul>
          </div>
          <div class="form-section--column">
            <h4>Termin odbioru:</h4>
            <ul>
              <li>${summary.pickup.date}</li>
              <li>${summary.pickup.time}</li>
              <li>${summary.pickup.more_info}</li>
            </ul>
          </div>
        </div>
      `;
    }

    /**
     * Submit form
     *
     * TODO: validation, send data to server
     */
    submit(e) {
      e.preventDefault();
      this.currentStep++;
      this.updateForm();
    }
  }
  const form = document.querySelector(".form--steps");
  if (form !== null) {
    new FormSteps(form);
  }
});
