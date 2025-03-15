export function setupCounter(element) {
  let counter = 0;

  const setCounter = (count) => {
      counter = count;
      document.getElementById('counterDisplay').innerHTML = `Count is ${counter}`;
  };

  element.addEventListener('click', () => {
      setCounter(counter + 1);

      // Visual Feedback
      element.classList.add("pulse");
      setTimeout(() => element.classList.remove("pulse"), 300);
  });

  setCounter(0); // Initialize counter
}

// Initialize Counter
document.addEventListener('DOMContentLoaded', () => {
  const counterBtn = document.getElementById('counterBtn');
  setupCounter(counterBtn);
});
