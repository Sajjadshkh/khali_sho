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

document.addEventListener('DOMContentLoaded', () => {
  const login = document.getElementById('login'),
        loginBtn = document.getElementById('login-btn'),
        loginClose = document.getElementById('login-close');

  if (loginBtn) {  // فقط اگر loginBtn وجود داشت
    loginBtn.addEventListener('click', () => {
      login.classList.add('show-login');
    });
  }

  if (loginClose) {
    loginClose.addEventListener('click', () => {
      login.classList.remove('show-login');
    });
  }
});
// Testimonial Slider (Enhanced version)
document.addEventListener("DOMContentLoaded", function () {
  const track = document.getElementById('testimonial-track');
  const prevBtn = document.getElementById('prev-testimonial');
  const nextBtn = document.getElementById('next-testimonial');
  const slides = document.querySelectorAll('.testimonial-slide');

  if (track && prevBtn && nextBtn && slides.length > 0) {
    let currentSlide = 0;
    const totalSlides = slides.length;
    
    // Calculate slides per view based on screen size
    function getSlidesPerView() {
      if (window.innerWidth >= 1400) return 4; // xl
      if (window.innerWidth >= 1024) return 3; // lg
      if (window.innerWidth >= 768) return 2;  // md
      return 1; // mobile
    }
    
    let slidesPerView = getSlidesPerView();
    let maxSlide = Math.max(0, totalSlides - slidesPerView);
    
    
    // Go to specific slide
    function goToSlide(slideIndex) {
      currentSlide = Math.max(0, Math.min(slideIndex, maxSlide));
      const translateX = (currentSlide * (100 / slidesPerView));
      track.style.transform = `translateX(${translateX}%)`;
      updateDots();
      updateButtons();
    }
    
    // Update button states
    function updateButtons() {
      prevBtn.disabled = currentSlide === 0; 
      nextBtn.disabled = currentSlide >= maxSlide;
      
      prevBtn.style.opacity = currentSlide === 0 ? '0.5' : '1';
      nextBtn.style.opacity = currentSlide >= maxSlide ? '0.5' : '1';
    }
    
    // Next slide
    function nextSlide() {
      if (currentSlide < maxSlide) {
        goToSlide(currentSlide + 1);
      }
    }
    
    // Previous slide
    function prevSlide() {
      if (currentSlide > 0) {
        goToSlide(currentSlide - 1);
      }
    }
    
    // Event listeners
    nextBtn.addEventListener('click', nextSlide);
    prevBtn.addEventListener('click', prevSlide);
    
    // Handle window resize
    window.addEventListener('resize', () => {
      const newSlidesPerView = getSlidesPerView();
      if (newSlidesPerView !== slidesPerView) {
        slidesPerView = newSlidesPerView;
        maxSlide = Math.max(0, totalSlides - slidesPerView);
        currentSlide = Math.min(currentSlide, maxSlide);
        createDots();
        goToSlide(currentSlide);
      }
    });
    
    // Auto-play functionality
    let autoPlayInterval;
    
    function startAutoPlay() {
      autoPlayInterval = setInterval(() => {
        if (currentSlide >= maxSlide) {
          goToSlide(0);
        } else {
          nextSlide(); // This will handle looping automatically
        }
      }, 5000); // Change slide every 5 seconds
    }
    
    function stopAutoPlay() {
      clearInterval(autoPlayInterval);
    }
    
    // Pause auto-play on hover
    track.addEventListener('mouseenter', stopAutoPlay);
    track.addEventListener('mouseleave', startAutoPlay);
    
    // Initialize
    createDots();
    updateButtons();
    startAutoPlay();
    
    // Touch/swipe support for mobile
    let startX = 0;
    let endX = 0;
    
    track.addEventListener('touchstart', (e) => {
      startX = e.touches[0].clientX;
    });
    
    track.addEventListener('touchend', (e) => {
      endX = e.changedTouches[0].clientX;
      const diff = startX - endX;
      
      if (Math.abs(diff) > 50) { // Minimum swipe distance
        if (diff > 0) {
          prevSlide(); // Swipe left
        } else {
          nextSlide(); // Swipe right
        }
      }
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


    // adviser

         // Simple animation for upload button
        // Tab switching for education levels
        const tabs = document.querySelectorAll('[data-tab]');
        tabs.forEach(tab => {
            tab.addEventListener('click', () => {
                // Remove active class from all tabs
                tabs.forEach(t => t.classList.remove('active'));
                // Add active class to clicked tab
                tab.classList.add('active');
                
                // Hide all tab contents
                document.querySelectorAll('.tab-content').forEach(content => {
                    content.classList.add('hidden');
                });
                
                // Show the selected tab content
                const tabId = tab.getAttribute('data-tab');
                document.getElementById(`${tabId}-tab`).classList.remove('hidden');
            });
        });
        
        // Specialty selection
        const specialtyTags = document.querySelectorAll('.specialty-tag');
        let selectedSpecialties = [];
        
        specialtyTags.forEach(tag => {
            tag.addEventListener('click', () => {
                const specialty = tag.getAttribute('data-specialty');
                
                if (tag.classList.contains('selected')) {
                    // Remove from selected
                    tag.classList.remove('selected');
                    selectedSpecialties = selectedSpecialties.filter(item => item !== specialty);
                } else {
                    // Add to selected
                    tag.classList.add('selected');
                    selectedSpecialties.push(specialty);
                }
                
                // Update hidden input
                // if (selectedSpecialtiesInput) { // This line is removed
                //     selectedSpecialtiesInput.value = selectedSpecialties.join(',');
                // }
            });
        });
        
        // Form validation
        document.querySelector('form').addEventListener('submit', function(e) {
            const requiredFields = document.querySelectorAll('input[required], select[required], textarea[required]');
            let isValid = true;
            
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    field.classList.add('border-red-500');
                    isValid = false;
                } else {
                    field.classList.remove('border-red-500');
                }
            });
            
            if (!document.getElementById('terms').checked) {
                document.getElementById('terms').nextElementSibling.classList.add('text-red-500');
                isValid = false;
            } else {
                document.getElementById('terms').nextElementSibling.classList.remove('text-red-500');
            }
            
            if (selectedSpecialties.length === 0) {
                alert('لطفا حداقل یک زمینه تخصصی را انتخاب کنید.');
                isValid = false;
            }
            
            if (!isValid) {
                e.preventDefault();
                alert('لطفا تمامی فیلدهای الزامی را پر کنید.');
            } else {
                // In a real app, you would submit the form here
                alert('فرم با موفقیت ارسال شد! اطلاعات شما در حال بررسی است.');
            }
        });
        
        // Add red border to required fields when they lose focus and are empty
        document.querySelectorAll('input[required], select[required], textarea[required]').forEach(field => {
            field.addEventListener('blur', function() {
                if (!this.value.trim()) {
                    this.classList.add('border-red-500');
                } else {
                    this.classList.remove('border-red-500');
                }
            });
        });