
function render({ model, el }) {
  let btn = document.createElement("button");
  el.appendChild(btn);
  btn.innerHTML = "Hello World!"

  btn.classList.add("anywidget_instructions-counter-button");
} 

export default { render };