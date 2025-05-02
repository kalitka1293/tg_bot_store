
// Обработчик корзины
document.addEventListener('click', (e) => {
    if (e.target.classList.contains('add-to-cart')) {
        const productCard = e.target.closest('.product-card');
        const productID = productCard.querySelector('.id_product').value;
        const productName = productCard.querySelector('.product-title').textContent;

        const ButtinId = "button" + productID;
        const button = document.getElementById(ButtinId)

        const link = document.createElement('a');
        link.href = 'https://docs.djangoproject.com/fr/2.2/topics/class-based-views/generic-display/';
        link.className = button.className; // Сохраняем классы
        link.id = button.id; // Сохраняем ID
        link.innerText = 'Перейти в корзину';
        link.style.display = 'inline-block'; // Для корректного отображения
        link.style.padding = '10px 10px'; // Пример стилей кнопки
        link.style.textDecoration = 'none'; // Убираем подчеркивание
        link.style.background = "black";

        // Заменяем кнопку на ссылку
        button.parentNode.replaceChild(link, button);


        console.log('Добавляем товар ID:', productID);

        axios.put('http://127.0.0.1:8000/basket/', {
            product_id: productID,
            user: 3434,
            quantity: 1 
        })
            .then(function (response) {
                console.log('Ответ сервера:', response.data);
            })
            .catch(function (error) {
                console.error('Ошибка:', error);
            });
    }
});




const loadIcons = () => {
    const link = document.createElement('link');
    link.rel = 'stylesheet';
    link.href = 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css';
    document.head.appendChild(link);
}




// Функция для отображения результатов
const showResults = (results) => {
    console.log(results)
    const resultsContainer = document.getElementById('searchResults');
    resultsContainer.innerHTML = '';

    if (results.length === 0) {
        resultsContainer.innerHTML = '<div class="search-result-item">Ничего не найдено. Воспользуйтесь фильтром для товаров</div>';
        return;
    }

    // Ограничиваем до 5 результатов
    const limitedResults = results;

    limitedResults.forEach(item => {
        const resultItem = document.createElement('div');
        resultItem.className = 'search-result-item';
        resultItem.textContent = 'Кондиционер: ' + item.name + ' | бренд:' + item.brand; 
        resultItem.addEventListener('click', () => {
            document.getElementById('searchInput').value = item.title;
            resultsContainer.style.display = 'none';
            // Здесь можно добавить переход на страницу товара
        });
        resultsContainer.appendChild(resultItem);
    });
}




// Оптимизация запросов с задержкой
let searchTimeout = null;
const DEBOUNCE_DELAY = 300; // Задержка в миллисекундах

const performSearch = (query_search) => {
    if (query_search.trim() !== '') {
        console.log('Ищем:', query_search);
        axios.get('http://127.0.0.1:8000/products/search', {
            params: { query: query_search },
            headers: {
                'accept': 'application/json'
            }
        })
            .then(function (response) {
                list_product = response.data.hits;
                showResults(list_product)
            })
            .catch(function (error) {
                console.error('Ошибка:', error);
            });
    }
}

// Обработчики событий
document.addEventListener('DOMContentLoaded', () => {
    loadIcons();

    const searchInput = document.getElementById('searchInput');
    const searchBtn = document.getElementById('searchBtn');

    // Мгновенный поиск при вводе
    searchInput.addEventListener('input', (e) => {
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(() => {
            performSearch(e.target.value);
        }, DEBOUNCE_DELAY);
    });

    // По клику на кнопку
    searchBtn.addEventListener('click', () => {
        clearTimeout(searchTimeout);
        performSearch(searchInput.value);
    });

    // По нажатию Enter
    searchInput.addEventListener('keyup', (e) => {
        if (e.key === 'Enter') {
            clearTimeout(searchTimeout);
            performSearch(searchInput.value);
        }
    });

    // Автофокус на поле ввода
    searchInput.focus();
});


