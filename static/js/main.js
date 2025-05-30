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

 // Testimonial Slider
 const slider = document.getElementById('testimonial-slider');
 const prevBtn = document.getElementById('prev-testimonial');
 const nextBtn = document.getElementById('next-testimonial');
 let currentSlide = 0;
 const slideWidth = document.querySelector('.testimonial-card').offsetWidth + 32; // 32 is for margin
 
 nextBtn.addEventListener('click', () => {
     currentSlide = (currentSlide + 1) % 3;
     slider.style.transform = `translateX(-${currentSlide * slideWidth}px)`;
 });
 
 prevBtn.addEventListener('click', () => {
     currentSlide = (currentSlide - 1 + 3) % 3;
     slider.style.transform = `translateX(-${currentSlide * slideWidth}px)`;
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