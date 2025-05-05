// Tum section ve nav linklerini sec
let sections = document.querySelectorAll('section');
let navlinks = document.querySelectorAll('header nav a');

// Sayfa kaydirildiginda navbar linklerinin aktifligini degistir
window.onscroll = () => {
    sections.forEach(sec => {
        let top = window.scrollY; // Sayfa ne kadar asagi kaydirildi
        let offset = sec.offsetTop - 150; // Her section'un ustten uzakligi -150 (erken tetiklenmesi icin)
        let height = sec.offsetHeight; // Section yuksekligi
        let id = sec.getAttribute('id'); // Section'un id'si ("home", "about" gibi)

        // Eger bu section gorunurdeyse, nav linkini aktif yap
        if (top >= offset && top < offset + height) {
            navlinks.forEach(links => {
                links.classList.remove('active'); // Tum linklerden "active" class'ini kaldir
                document.querySelector('header nav a[href*=' + id + ']').classList.add('active'); // Uyan linke "active" class'ini ekle
            });
        }
    });

    // Header'a sticky class'i ekle/kaldir (scroll 100'den fazlaysa)
    let header = document.querySelector('header');
    header.classList.toggle('sticky', window.scrollY > 100);

    // Linke tiklayinca menu otomatik kapansin
    menuIcon.classList.remove('bx-x');
    navbar.classList.remove('active');
};

// Navbar menu ac/kapat
let menuIcon = document.querySelector('#menu-icon');
let navbar = document.querySelector('.navbar');

menuIcon.onclick = () => {
    menuIcon.classList.toggle('bx-x'); // Ikonu degistir
    navbar.classList.toggle('active'); // Menuyu goster/gizle
};

// Scroll Reveal: Kaydirinca animasyonlar
ScrollReveal({
    reset: true, // Her kaydirmada yeniden animasyon yap
    distance: '80px', // Ne kadar uzakliktan gelsin
    duration: 2000, // Animasyon suresi
    delay: 200 // Baslamadan once bekleme suresi
});

// Hangi bolumler hangi yonden gelsin
ScrollReveal().reveal('.home-content, .heading', { origin: 'top' });
ScrollReveal().reveal('.home-img, .services-container, .portfolio-box, .contact form', { origin: 'bottom' });
ScrollReveal().reveal('.home-content h1, .about-img', { origin: 'left' });
ScrollReveal().reveal('.home-content p, .about-content', { origin: 'right' });

// Assistant fonksiyonu: kullanici yazisini al, backend'e gonder, sonucu goster
function startAssistant() {
    const userInput = document.getElementById("userInput").value; // Input degerini al

    fetch("http://localhost:5000/process", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ input: userInput }) // JSON formatinda gonder
    })
    .then(response => response.json())
    .then(data => {
        const cevapDiv = document.getElementById("cevapDiv");

        // Kategori ve Alt kategori bilgileri goster
        cevapDiv.innerHTML = `
            <div class="kategori-bilgi">
                <span>
                <h3 class="kategori">En iyi kategori: <strong>${data.category}</strong></h3>
                </span>
                <span>
                <h3 class="alt-kategori">Alt kategori: <strong>${data.subcategory}</strong></h3>
                </span>
            </div>
        `;

        // Urun onerileri varsa kart olarak goster
        if (data.products.length > 0) {
            cevapDiv.innerHTML += `
                <div class="recommendation-container">
                    ${data.products.map(product => `
                        <div class="product-card">
                            <h4>${product}</h4>
                        </div>
                    `).join('')}
                </div>
            `;
        } else {
            // Oneri yoksa sadece mesaj goster
            cevapDiv.innerHTML += `<h3 class="output-title">${data.message}</h3>`;
        }

        // Sonucu gosterilen bolume kaydir
        document.getElementById("home").scrollIntoView({ behavior: "smooth" });
    })
    .catch(error => {
        console.error("Error:", error); // Hata varsa konsola yazdir
    });
}
