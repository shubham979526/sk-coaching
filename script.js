const navToggle = document.querySelector('.nav-toggle');
const navMenu = document.querySelector('.nav-menu');
const year = document.getElementById('year');
const enquiryForm = document.getElementById('enquiryForm');

if (year) {
  year.textContent = new Date().getFullYear();
}

if (navToggle && navMenu) {
  navToggle.addEventListener('click', () => {
    const isOpen = navMenu.classList.toggle('open');
    navToggle.setAttribute('aria-expanded', String(isOpen));
  });

  navMenu.querySelectorAll('a').forEach((link) => {
    link.addEventListener('click', () => {
      navMenu.classList.remove('open');
      navToggle.setAttribute('aria-expanded', 'false');
    });
  });
}

if (enquiryForm) {
  enquiryForm.addEventListener('submit', async (event) => {
    event.preventDefault();

    const button = enquiryForm.querySelector('button');
    const originalText = button.textContent;
    const formData = new FormData(enquiryForm);
    const payload = {
      name: formData.get('name')?.toString().trim(),
      class_name: formData.get('class_name')?.toString().trim(),
      phone: formData.get('phone')?.toString().trim(),
      course: formData.get('course')?.toString().trim(),
    };

    button.textContent = 'Submitting...';
    button.disabled = true;

    try {
      const response = await fetch('/api/enquiry', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });

      const result = await response.json();

      if (!response.ok) {
        throw new Error(result.error || 'Unable to submit enquiry.');
      }

      button.textContent = 'Submitted';
      enquiryForm.reset();
      alert('Your enquiry has been submitted successfully. We will contact you soon.');
    } catch (error) {
      alert(error.message || 'Something went wrong. Please try again.');
      button.textContent = originalText;
    } finally {
      button.disabled = false;
      setTimeout(() => {
        button.textContent = originalText;
      }, 1200);
    }
  });
}
