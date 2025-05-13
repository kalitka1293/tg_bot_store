const scrollContainer = document.querySelector('.scroll-container-image');
const blocksWrapper = document.querySelector('.blocks-wrapper-image');
let isDragging = false;
let startX;
let scrollLeft;

// Touch events
scrollContainer.addEventListener('touchstart', (e) => {
    isDragging = true;
    startX = e.touches[0].pageX - scrollContainer.offsetLeft;
    scrollLeft = scrollContainer.scrollLeft;
});

scrollContainer.addEventListener('touchmove', (e) => {
    if (!isDragging) return;
    const x = e.touches[0].pageX - scrollContainer.offsetLeft;
    const walk = (x - startX) * 2;
    scrollContainer.scrollLeft = scrollLeft - walk;
});

scrollContainer.addEventListener('touchend', () => {
    isDragging = false;
});

// Mouse events
scrollContainer.addEventListener('mousedown', (e) => {
    isDragging = true;
    startX = e.pageX - scrollContainer.offsetLeft;
    scrollLeft = scrollContainer.scrollLeft;
    scrollContainer.style.cursor = 'grabbing';
});

scrollContainer.addEventListener('mousemove', (e) => {
    if (!isDragging) return;
    const x = e.pageX - scrollContainer.offsetLeft;
    const walk = (x - startX) * 3;
    scrollContainer.scrollLeft = scrollLeft - walk;
});

scrollContainer.addEventListener('mouseup', () => {
    isDragging = false;
    scrollContainer.style.cursor = 'grab';
});

scrollContainer.addEventListener('wheel', (e) => {
    e.preventDefault();
    scrollContainer.scrollLeft += e.deltaY * 2;
});

// Initial styles
scrollContainer.style.cursor = 'grab';


        // Добавляем обработчик свайпа
    let touchStartX = 0;
    const container = document.querySelector('.scroll-container');

    container.addEventListener('touchstart', e => {
        touchStartX = e.touches[0].clientX;
    }, false);

    container.addEventListener('touchend', e => {
        const touchEndX = e.changedTouches[0].clientX;
        const diffX = touchStartX - touchEndX;

        if(Math.abs(diffX) > 30) {
            container.scrollBy({
                left: diffX > 0 ? 200 : -200,
                behavior: 'smooth'
            });
        }
    }, false);

    // Инициализация слайдеров для всех карточек
    document.addEventListener('DOMContentLoaded', function() {
        const swipers = document.querySelectorAll('.product-swiper');
        swipers.forEach(swiperEl => {
            new Swiper(swiperEl, {
                loop: true,
                speed: 400,
                spaceBetween: 0,
                pagination: {
                    el: '.swiper-pagination',
                    clickable: true,
                },
                navigation: {
                    nextEl: '.swiper-button-next',
                    prevEl: '.swiper-button-prev',
                },
            });
        });
    });