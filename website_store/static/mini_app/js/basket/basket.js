document.addEventListener('click', async (e) => {
  const target = e.target;

// Удаление товара
if(target.classList.contains('delete-btn')) {
    const itemId = target.dataset.id;
    send_basket(itemId, 'delete', 1);

    // Удаляем элемент из HTML
    const cartItem = target.closest('.cart-item');
    cartItem.remove();

    // Обновляем общую сумму
    let total = 0;
    document.querySelectorAll('.item-price').forEach(element => {
        total += parseFloat(element.textContent.replace(' ₽', ''));
    });
    document.querySelector('.total-price').textContent = total.toFixed(2) + ' ₽';

    // Показываем сообщение если корзина пуста
    if(document.querySelectorAll('.cart-item').length === 0) {
        document.getElementById('empty-cart-message').style.display = 'block';

        const checkoutLink = document.querySelector('.a-checkout-btn')
        const checkoutButton = document.querySelector('.checkout-btn')
        checkoutLink.href = "http://127.0.0.1:8080/mini_app/menu"
        checkoutButton.textContent = "Перейти к каталогу товаров"

    }
}

  // Изменение количества
  if(target.classList.contains('quantity-btn')) {
    const itemId = target.dataset.id;
    const isPlus = target.classList.contains('plus');
    const quantityElement = target.parentElement.querySelector('.quantity');
    let newQuantity = parseInt(quantityElement.textContent);

    if(isPlus) {
        newQuantity++;
        send_basket(itemId, 'put', 1);
    } else if(newQuantity > 1) {
      newQuantity--;
        send_basket(itemId, 'put', -1);
    }

    // После успешного ответа сервера обновить:
    quantityElement.textContent = newQuantity;

    // Новый код для обновления сумм
    const itemInfo = target.closest('.item-info');
    const price = parseFloat(itemInfo.querySelector('.price_product').value);
    const itemPriceElement = itemInfo.querySelector('.item-price');
    itemPriceElement.textContent = (price * newQuantity).toFixed(2) + ' ₽';

    let total = 0;
    document.querySelectorAll('.item-price').forEach(element => {
        total += parseFloat(element.textContent.replace(' ₽', ''));
    });
    document.querySelector('.total-price').textContent = total.toFixed(2) + ' ₽';
    // Конец нового кода
  }
});

const send_basket = (productID, method, quantity) => {
    axios({
        method: method,
        url: "https://aa64f2542c2ab1.lhr.life/basket/",
        data: {
            product_id: productID,
            user: 3434,
            quantity: quantity 
        },
        withCredentials: true,
        headers: {
            "Content-Type": "application/json",
        }
    }).then(function (response) {
        console.log('Ответ сервера:', response.data);
    })
        .catch(function (error) {
            console.error('Ошибка:', error);
        });
}