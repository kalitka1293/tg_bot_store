document.addEventListener('DOMContentLoaded', () => {
    // Обработчики кликов
    const buttons = {
        channelBtn: document.querySelector('.channel-btn'),
        callbackBtn: document.querySelector('.callback-btn'),
        cartBtn: document.querySelector('.cart-btn')
    };

    // Переход на канал
    buttons.channelBtn.addEventListener('click', () => {
        window.open('https://t.me/shovik_channel', '_blank');
    });

    // Заказ звонка
    buttons.callbackBtn.addEventListener('click', () => {
        alert('Мы перезвоним вам в течение 10 минут!');
    });

    // Корзина
    let cartCount = 0;
    buttons.cartBtn.addEventListener('click', () => {
        window.location.href = '/cart';
    });

    // Обновление счетчика корзины
    function updateCartCounter() {
        buttons.cartBtn.textContent = `Корзина (${cartCount})`;
    }
});