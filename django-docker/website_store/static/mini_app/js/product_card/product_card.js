function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}


document.addEventListener('click', (e) => {
    if (e.target.classList.contains('buy-btn')) {
        const text_to_basket = 'Перейти в корзину'
        const productCard = e.target.closest('.price-block');

        if (e.target.tagName === 'A') {
            // Если это уже ссылка - позволяем переходу произойти естественным образом
            return;
        }
        const productID = document.querySelectorAll('.id_product')[0].value;

        const ButtinId = "button" + productID;
        const button = document.getElementById(ButtinId)

        const link = document.createElement('a');
        link.href = window.URL_SITE.basket;
        link.className = button.className; // Сохраняем классы
        link.id = button.id; // Сохраняем ID
        link.innerText = text_to_basket;
        link.style.display = 'inline-block'; // Для корректного отображения
        link.style.padding = '17px 32px'; // Пример стилей кнопки
        link.style.textDecoration = 'none'; // Убираем подчеркивание
        link.style.background = "black";

        // Заменяем кнопку на ссылку
        button.parentNode.replaceChild(link, button);


        console.log('Добавляем товар ID:', productID);

        axios({
            method: 'PUT',
            url: `${window.URL_FASTAPI.url}/basket/`,
            data: {
                product_id: productID,
                quantity: 1
            },
            withCredentials: true,
            headers: {
                "Content-Type": "application/json",
                "X-CSRF-Token": getCookie('fastapi-csrf-token'),
            }
        }).then(function (response) {
            console.log('Ответ сервера:', response.status);
        })
            .catch(function (error) {
                const e = error.response.data.type;
                if (error.response.status === 401) {
                    window.location.replace(window.URL_SITE.main_page);
                    alert(e)
                } else {
                    window.location.replace(window.URL_SITE.main_page);
                    alert(e)
                }
                console.error('Ошибка:', error.response.status);
            });
    }
});

/////////////////////////////////////////////////////////////////////////////////////////////

function showReviewForm() {
    // Ваша логика открытия формы
    alert('Функция добавления комментариев временно недоступна');
}