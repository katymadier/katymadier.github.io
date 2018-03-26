

function toggleAside() {
  var x = document.getElementById('mobile-nav');
    if (x.style.display === "none") {
      x.style.display = "block";
    } else {
      x.style.display = "none";
    }
  }

window.onscroll=function() {shadow()};

function shadow() {
  if (document.body.scrollTop > 50 || document.documentElement.scrollTop > 50) {
    document.getElementById('top-menu').className= "shadow";
} else {
      document.getElementById("top-menu").className="noshadow";
  }
}






// mdc material design script by google
function closeAside() {
  var x = document.getElementById('mobile-nav');
    x.style.display = "none";
  }

var buttons = document.querySelectorAll('.mdc-button, .mdc-fab');
for (var i = 0, button; button = buttons[i]; i++) {
  mdc.ripple.MDCRipple.attachTo(button);
}

var nodes = document.querySelectorAll('.mdc-icon-toggle');
for (var i = 0, node; node = nodes[i]; i++) {
  mdc.iconToggle.MDCIconToggle.attachTo(node);
}

var checkboxes = document.querySelectorAll('.mdc-checkbox');
for (var i = 0, checkbox; checkbox = checkboxes[i]; i++) {
  new mdc.checkbox.MDCCheckbox(checkbox);
}

var radios = document.querySelectorAll('.mdc-radio');
for (var i = 0, radio; radio = radios[i]; i++) {
  new mdc.radio.MDCRadio(radio);
}

var interactiveListItems = document.querySelectorAll('.mdc-list-item');
for (var i = 0, li; li = interactiveListItems[i]; i++) {
  mdc.ripple.MDCRipple.attachTo(li);
  // Prevent link clicks from jumping demo to the top of the page
  li.addEventListener('click', function(evt) {
    evt.preventDefault();
  });
}
