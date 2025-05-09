function togglePaymentMethod(method) {
    const callbackField = document.getElementById('callback-field');
    const onlineMethods = document.getElementById('online-methods');
    const buttons = document.querySelectorAll('.method-btn');

    // Управление активными кнопками
    buttons.forEach(btn => {
        btn.classList.remove('active');
        if (btn.textContent.includes(method === 'callback' ? '☎️' : '💳')) {
            btn.classList.add('active');
        }
    });

    // Показ/скрытие соответствующих блоков
    callbackField.style.display = method === 'callback' ? 'block' : 'none';
    onlineMethods.style.display = method === 'online' ? 'block' : 'none';

    // Валидация полей
    document.getElementById('payment-phone').required = method === 'callback';

    // Сброс выбранного метода оплаты
    document.querySelectorAll('.payment-option').forEach(btn => {
        btn.classList.remove('active-method');
    });
}

// Обработчик выбора конкретного метода оплаты
document.querySelectorAll('.payment-option').forEach(btn => {
    btn.addEventListener('click', function() {
        document.querySelectorAll('.payment-option').forEach(b => b.classList.remove('active-method'));
        this.classList.add('active-method');
        // Здесь можно добавить логику для выбранного метода
        console.log('Выбран метод:', this.dataset.method);
    });
});