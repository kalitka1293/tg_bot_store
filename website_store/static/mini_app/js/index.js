const products = [
            {
                imageUrl: 'https://via.placeholder.com/300x150/FFCCCC?text=Футболка',
                discount: '33%',
                brand: 'Макс',
                oldPrice: '6688 руб.',
                newPrice: '4889 руб.',
                title: 'Спортивная футболка',
                stock: 'В наличии'
            },
            {
                imageUrl: 'https://via.placeholder.com/300x150/CCFFCC?text=Кроссовки',
                brand: 'Adidas',
                newPrice: '1589 руб.',
                title: 'Беговые кроссовки',
                stock: 'В наличии'
            },
            {
                imageUrl: 'https://via.placeholder.com/300x150/CCE5FF?text=Шорты',
                discount: '-25%',
                brand: 'Nike',
                oldPrice: '3288 руб.',
                newPrice: '2499 руб.',
                title: 'Спортивные шорты',
                stock: 'В наличии'
            },
            {
                imageUrl: 'https://via.placeholder.com/300x150/FFE5CC?text=Куртка',
                brand: 'Puma',
                newPrice: '5999 руб.',
                title: 'Спортивная куртка',
                stock: 'В наличии'
            }
        ];

        function createProductCard(product) {
            return `
                <div class="product-card">
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
            container.innerHTML = products.map(createProductCard).join('');
        });

        // Обработчик корзины
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('add-to-cart')) {
                const productCard = e.target.closest('.product-card');
                const productName = productCard.querySelector('.product-title').textContent;
                alert(`"${productName}" добавлен в корзину`);
            }
        });