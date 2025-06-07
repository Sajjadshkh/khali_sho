/*=============== SHOW MENU ===============*/
const navMenu = document.getElementById('nav-menu'),
      navToggle = document.getElementById('nav-toggle'),
      navClose = document.getElementById('nav-close')

/* Menu show */
navToggle.addEventListener('click', () =>{
   navMenu.classList.add('show-menu')
})

/* Menu hidden */
navClose.addEventListener('click', () =>{
   navMenu.classList.remove('show-menu')
})

/*=============== SEARCH ===============*/
// const search = document.getElementById('search'),
//       searchBtn = document.getElementById('search-btn'),
//       searchClose = document.getElementById('search-close')

// /* Search show */
// searchBtn.addEventListener('click', () =>{
//    search.classList.add('show-search')
// })

// /* Search hidden */
// searchClose.addEventListener('click', () =>{
//    search.classList.remove('show-search')
// })

/*=============== LOGIN ===============*/
const login = document.getElementById('login'),
      loginBtn = document.getElementById('login-btn'),
      loginClose = document.getElementById('login-close')

/* Login show */
loginBtn.addEventListener('click', () =>{
   login.classList.add('show-login')
})

/* Login hidden */
loginClose.addEventListener('click', () =>{
   login.classList.remove('show-login')
})
// Testimonial Slider (safe version)
document.addEventListener("DOMContentLoaded", function () {
  const slider = document.getElementById('testimonial-slider');
  const prevBtn = document.getElementById('prev-testimonial');
  const nextBtn = document.getElementById('next-testimonial');
  const testimonialCard = document.querySelector('.testimonial-card');

  if (slider && prevBtn && nextBtn && testimonialCard) {
    let currentSlide = 0;
    const slideWidth = testimonialCard.offsetWidth + 32; // 32 is for margin

    nextBtn.addEventListener('click', () => {
      currentSlide = (currentSlide + 1) % 3;
      slider.style.transform = `translateX(-${currentSlide * slideWidth}px)`;
    });

    prevBtn.addEventListener('click', () => {
      currentSlide = (currentSlide - 1 + 3) % 3;
      slider.style.transform = `translateX(-${currentSlide * slideWidth}px)`;
    });
  }
});
 
 // Chat Button
 const chatBtn = document.getElementById('chat-btn');
 
 chatBtn.addEventListener('click', () => {
     alert('پشتیبانی آنلاین در حال حاضر در دسترس نیست. لطفاً در ساعات کاری تماس بگیرید.');
 });

  // Simple animation for scroll
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                
                document.querySelector(this.getAttribute('href')).scrollIntoView({
                    behavior: 'smooth'
                });
            });
        });
        
        // Donate button effect
        const donateBtn = document.querySelector('.donate-btn');
        if(donateBtn) {
            donateBtn.addEventListener('mouseenter', () => {
                donateBtn.innerHTML = 'حمایت مالی <i class="fas fa-hand-holding-heart ml-2"></i>';
            });
            
            donateBtn.addEventListener('mouseleave', () => {
                donateBtn.innerHTML = 'حمایت مالی <i class="fas fa-heart ml-2"></i>';
            });
        }

// loding screen

document.addEventListener("DOMContentLoaded", function () {
  // Simulate the delay in loading your content (remove this in production)
  setTimeout(function () {
    document.querySelector(".loading-screen").style.display = "none"; // Hide loading screen
    document.querySelector("header").style.display = "block"; // Show the navigation bar
  }, 2000); // Change the duration as needed
});

// podcasts
        // Simple animation for upload button
        const uploadBtn = document.querySelector('.upload-btn');
        if(uploadBtn) {
            uploadBtn.addEventListener('mouseenter', () => {
                uploadBtn.innerHTML = '<i class="fas fa-share-square ml-2"></i> انتشار پادکست';
            });
            
            uploadBtn.addEventListener('mouseleave', () => {
                uploadBtn.innerHTML = '<i class="fas fa-podcast ml-2"></i> انتشار پادکست';
            });
        }
        
        // Simulate podcast play count
        document.querySelectorAll('audio').forEach(audio => {
            audio.addEventListener('play', function() {
                const card = this.closest('.podcast-card');
                if(card) {
                    card.classList.add('ring-2', 'ring-blue-500');
                }
            });
            
            audio.addEventListener('pause', function() {
                const card = this.closest('.podcast-card');
                if(card) {
                    card.classList.remove('ring-2', 'ring-blue-500');
                }
            });
        });

fetch('/home/login/')
  .then(res => res.text())
  .then(html => {
    document.getElementById("popup-container").innerHTML = html;
    document.getElementById("login").classList.add("show");
  });