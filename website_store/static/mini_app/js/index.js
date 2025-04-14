const products = [
    {
        id: 1,  // Добавлен ID товара
        imageUrl: 'https://via.placeholder.com/300x150/FFCCCC?text=Футболка',
        discount: '33%',
        brand: 'Макс',
        oldPrice: '6688 руб.',
        newPrice: '4889 руб.',
        title: 'Спортивная футболка',
        stock: 'В наличии'
    },
    // ... остальные товары тоже должны иметь id
];

function createProductCard(product) {
    return `
        <div class="product-card">
            <input type="hidden" class="id_product" value="${product.id}">
            ${product.discount ? `<div class="discount-badge">${product.discount}</div>` : ''}
            <img src="${product.imageUrl}" alt="${product.title}" class="product-image">
            <div class="brand">${product.brand}</div>
            <h3 class="product-title">${product.title}</h3>
            <div class="price-container">
                ${product.oldPrice ? `<span class="old-price">${product.oldPrice}</span>` : ''}
                <span class="new-price">${product.newPrice}</span>
            </div>
            <div class="stock-status">${product.stock}</div>
            <button class="add-to-cart">В корзину</button>
        </div>
    `;
}

document.addEventListener('DOMContentLoaded', () => {
    const container = document.getElementById('productsContainer');
    if (container) {
        container.innerHTML = products.map(createProductCard).join('');
    }
});

// Обработчик корзины
document.addEventListener('click', (e) => {
    if (e.target.classList.contains('add-to-cart')) {
        const productCard = e.target.closest('.product-card');
        const productID = productCard.querySelector('.id_product').value;
        const productName = productCard.querySelector('.product-title').textContent;

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