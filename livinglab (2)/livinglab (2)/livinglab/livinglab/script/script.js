////let sections= document.querySelectorAll('section');
////let navlinks = document.querySelectorAll('header nav a');
////
////window.onscroll = () => {
////    sections.forEach(sec => {
////        let top = window.scrollY;
////        let offset = sec.offsetTop - 150;
////        let height = sec.offsetHeight;
////        let id = sec.getAttribute('id');
////
////
////        if(top >= offset && top < offset + height){
////            navlinks.forEach(links => {
////                links.classList.remove('active');
////                document.querySelector('header nav a[href*=' + id + ']').classList.add('active');
////
////            });
////        };
////
////
////    });
////
////    //sticky navbar
////
////let header = document.querySelector('header');
////
////header.classList.toggle('sticky',window.scrollY >100);
////
////
////// remove toggle icon and navbar when click navbar link(scroll)
////
////menuIcon.classList.remove('bx-x');
////navbar.classList.remove('active');
////
////
////
////};
////
////
////
////
////
////
////
/////*  SCROLL REVEAL */
////
////ScrollReveal({
////    reset: true, //false
////    distance:'80px',
////    duration:2000,
////    delay:200
////
////
////
////});
////
////ScrollReveal().reveal('.home-content, .heading', { origin: 'top'});
////
////ScrollReveal().reveal('.home-img, .services-container, .portfolio-box, .contact from', { origin: 'bottom'});
////
////ScrollReveal().reveal('.home-content h1, .about-img', { origin: 'left'});
////
////ScrollReveal().reveal('.home-content p, .about-content', { origin: 'right'});
////
////
//////toggle icon navbar
////
////let menuIcon = document.querySelector('#menu-icon');
////let navbar = document.querySelector('.navbar');
////
////menuIcon.onclick = () =>{
////    menuIcon.classList.toggle('bx-x');
////    navbar.classList.toggle('active');
////};
////
////
////// function startAssistant() {
//////     const userInput = document.getElementById('userInput').value;
////
//////     // API'ye veri göndermek için fetch() kullanacağız
//////     fetch('http://127.0.0.1:5000/process', {
//////         method: 'POST',
//////         headers: {
//////             'Content-Type': 'application/json'
//////         },
//////         body: JSON.stringify({
//////             input: userInput
//////         })
//////     })
//////     .then(response => response.json())
//////     .then(data => {
//////         // API'den gelen cevabı al
//////         const cevapDiv = document.getElementById('cevapDiv');
//////         cevapDiv.textContent = data.message;  // Gelen cevabı bu div'in içine ekliyoruz
//////     })
//////     .catch(error => {
//////         console.error('Error:', error);
//////     });
////// }
////
////function startAssistant() {
////    const userInput = document.getElementById("userInput").value;
////
////    fetch("http://localhost:5000/process", {
////        method: "POST",
////        headers: {
////            "Content-Type": "application/json",
////        },
////        body: JSON.stringify({ input: userInput })
////    })
////    .then(response => response.json())
////    .then(data => {
////        document.getElementById("cevapDiv").innerText = data.message;
////    })
////    .catch(error => {
////        console.error("Error:", error);
////    });
////}
////
////
////
//
//let sections= document.querySelectorAll('section');
//let navlinks = document.querySelectorAll('header nav a');
//
//window.onscroll = () => {
//    sections.forEach(sec => {
//        let top = window.scrollY;
//        let offset = sec.offsetTop - 150;
//        let height = sec.offsetHeight;
//        let id = sec.getAttribute('id');
//
//        if(top >= offset && top < offset + height){
//            navlinks.forEach(links => {
//                links.classList.remove('active');
//                document.querySelector('header nav a[href*=' + id + ']').classList.add('active');
//            });
//        }
//    });
//
//    let header = document.querySelector('header');
//    header.classList.toggle('sticky',window.scrollY >100);
//
//    menuIcon.classList.remove('bx-x');
//    navbar.classList.remove('active');
//};
//
//let menuIcon = document.querySelector('#menu-icon');
//let navbar = document.querySelector('.navbar');
//
//menuIcon.onclick = () =>{
//    menuIcon.classList.toggle('bx-x');
//    navbar.classList.toggle('active');
//};
//
//function startAssistant() {
//    const userInput = document.getElementById("userInput").value;
//
//    fetch("http://localhost:5000/process", {
//        method: "POST",
//        headers: {
//            "Content-Type": "application/json",
//        },
//        body: JSON.stringify({ input: userInput })
//    })
//    .then(response => response.json())
//    .then(data => {
//        const cevapDiv = document.getElementById("cevapDiv");
//        cevapDiv.innerHTML = `
//            <h3 class="output-title">Recommended Products for You</h3>
//            <div class="recommendation-container">
//                ${data.products.map(product => `
//                    <div class="product-card">
//                        <h4>${product}</h4>
//                    </div>
//                `).join('')}
//            </div>
//        `;
//    })
//    .catch(error => {
//        console.error("Error:", error);
//    });
//}

let sections = document.querySelectorAll('section');
let navlinks = document.querySelectorAll('header nav a');

// Navbar link active on scroll
window.onscroll = () => {
    sections.forEach(sec => {
        let top = window.scrollY;
        let offset = sec.offsetTop - 150;
        let height = sec.offsetHeight;
        let id = sec.getAttribute('id');

        if (top >= offset && top < offset + height) {
            navlinks.forEach(links => {
                links.classList.remove('active');
                document.querySelector('header nav a[href*=' + id + ']').classList.add('active');
            });
        }
    });

    let header = document.querySelector('header');
    header.classList.toggle('sticky', window.scrollY > 100);

    // Close navbar after clicking link
    menuIcon.classList.remove('bx-x');
    navbar.classList.remove('active');
};

// Toggle Navbar Menu
let menuIcon = document.querySelector('#menu-icon');
let navbar = document.querySelector('.navbar');

menuIcon.onclick = () => {
    menuIcon.classList.toggle('bx-x');
    navbar.classList.toggle('active');
};

// Scroll Reveal Animations
ScrollReveal({
    reset: true,
    distance: '80px',
    duration: 2000,
    delay: 200
});

ScrollReveal().reveal('.home-content, .heading', { origin: 'top' });
ScrollReveal().reveal('.home-img, .services-container, .portfolio-box, .contact form', { origin: 'bottom' });
ScrollReveal().reveal('.home-content h1, .about-img', { origin: 'left' });
ScrollReveal().reveal('.home-content p, .about-content', { origin: 'right' });

// Assistant Product Recommendation Function
function startAssistant() {
    const userInput = document.getElementById("userInput").value;

    fetch("http://localhost:5000/process", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ input: userInput })
    })
        .then(response => response.json())
        .then(data => {
            const cevapDiv = document.getElementById("cevapDiv");
            const subcategoryHTML = data.subcategory ? `<h4 class="output-subtitle">${data.subcategory}</h4>` : '';
            // If there are products
            if (data.products.length > 0) {
                cevapDiv.innerHTML = `
                <h3 class="output-title">${data.message}</h3>
                <div class="recommendation-container">
                    ${data.products.map(product => `
                        <div class="product-card">
                            <h4>${product}</h4>
                        </div>
                    `).join('')}
                </div>
                `;
            } else {
                cevapDiv.innerHTML = `<h3 class="output-title">${data.message}</h3>`;
            }
        })
        .catch(error => {
            console.error("Error:", error);
        });
}

/*
let sections = document.querySelectorAll('section');
let navlinks = document.querySelectorAll('header nav a');
let menuIcon = document.querySelector('#menu-icon');
let navbar = document.querySelector('.navbar');

window.onscroll = () => {
    sections.forEach(sec => {
        let top = window.scrollY;
        let offset = sec.offsetTop - 150;
        let height = sec.offsetHeight;
        let id = sec.getAttribute('id');

        if (top >= offset && top < offset + height) {
            navlinks.forEach(links => {
                links.classList.remove('active');
                document.querySelector('header nav a[href*=' + id + ']').classList.add('active');
            });
        }
    });

    document.querySelector('header').classList.toggle('sticky', window.scrollY > 100);
    menuIcon.classList.remove('bx-x');
    navbar.classList.remove('active');
};

menuIcon.onclick = () => {
    menuIcon.classList.toggle('bx-x');
    navbar.classList.toggle('active');
};

function startAssistant() {
    const userInput = document.getElementById("userInput").value;

    fetch("http://localhost:5000/process", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ input: userInput })
    })
        .then(response => response.json())
        .then(data => {
            const cevapDiv = document.getElementById("cevapDiv");
            cevapDiv.innerHTML = `
                <h3 class="output-title">Önerilen Ürünler</h3>
                <div class="recommendation-container">
                    ${data.products.map(product => `
                        <div class="product-card">
                            <h4>${product}</h4>
                        </div>
                    `).join('')}
                </div>
            `;
        })
        .catch(error => {
            console.error("Error:", error);
        });
}
*/
