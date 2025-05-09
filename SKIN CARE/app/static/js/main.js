let menu = document.querySelector('#menu-bar');
let nav = document.querySelector('.nav');

menu.onclick = () =>{
    menu.classList.toggle('fa-times');
    nav.classList.toggle('active');
}

let section = document.querySelectorAll('section');
let navLinks = document.querySelectorAll('header .nav a');

window.onscroll = () =>{

    menu.classList.remove('fa-times');
    nav.classList.remove('active');

    section.forEach(sec =>{

        let top = window.scrollY;
        let height = sec.offsetHeight;
        let offset = sec.offsetTop - 150;
        let id = sec.getAttribute('id');

        if(top >= offset && top < offset + height){
            navLinks.forEach(links =>{
                links.classList.remove('active');
                document.querySelector('header .nav a[href*='+id+']').classList.add('active');
            });
        };
    });

}

const realFileBtn = document.getElementById("real-file");
const customBtn = document.getElementById("custom-button");
const customTxt = document.getElementById("custom-text");

customBtn.addEventListener("click", function() {
  realFileBtn.click();
});

realFileBtn.addEventListener("change", function() {
  if (realFileBtn.value) {
    customTxt.innerHTML = realFileBtn.value.match(
      /[\/\\]([\w\d\s\.\-\(\)]+)$/
    )[1];
  } else {
    customTxt.innerHTML = "No file chosen, yet.";
  }
});

// --- AJAX upload logic for dynamic/live results ---
const form = document.querySelector('form');
const statusDiv = document.getElementById('upload-status');
const resultDiv = document.getElementById('result-area');

form.addEventListener('submit', function(e) {
  e.preventDefault();
  statusDiv.innerHTML = '<span style="color:#926AD4">Uploading and analyzing...</span>';
  resultDiv.innerHTML = '';
  const formData = new FormData(form);
  fetch('/np', {
    method: 'POST',
    body: formData,
    headers: {
      'X-Requested-With': 'XMLHttpRequest'
    }
  })
    .then(res => {
      if (!res.ok) {
        throw new Error('Network response was not ok');
      }
      return res.json();
    })
    .then(data => {
      statusDiv.innerHTML = '';
      if (data.res) {
        resultDiv.innerHTML = `<h4 style='color:#926AD4; font-size:2vw;'><b>Your Result is here:</b></h4><h4 style='color:#926AD4; font-size:2vw;'><b>${data.res}</b></h4>`;
      } else {
        resultDiv.innerHTML = `<span style='color:red;'>No result returned.</span>`;
      }
    })
    .catch(err => {
      statusDiv.innerHTML = '';
      resultDiv.innerHTML = `<span style='color:red;'>Error: ${err}</span>`;
    });
});
