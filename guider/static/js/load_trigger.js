const spinner = document.getElementById("spinner");
const wrapper = document.getElementById("spinner-wrapper");
const map = document.getElementById("gmap_canvas");

function loadData() {
  spinner.removeAttribute('hidden');
  wrapper.removeAttribute('hidden');
  fetch('/handle_route')
    .then(response => response.json())
    .then(data => {
      spinner.setAttribute('hidden', '');
      wrapper.setAttribute('hidden', '');
      console.log(data);

      var event = new CustomEvent('load_trigger', {detail: data});
      console.log('This is the event');
      console.log(event)
      map.dispatchEvent(event);
    });
}

console.log("Initializing");
loadData();
console.log("Done");