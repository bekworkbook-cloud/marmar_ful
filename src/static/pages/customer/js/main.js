/* js/main.js */
const app = {
    cart: JSON.parse(localStorage.getItem('cart')) || [],
    currentBranchId: null,

    async api(endpoint, method = 'GET', body = null) {
        const token = localStorage.getItem('jwt');
        const headers = { 'Content-Type': 'application/json' };
        if (token) headers['Authorization'] = `Bearer ${token}`;

        const config = { method, headers };
        if (body) config.body = JSON.stringify(body);

        const response = await fetch(`/api/v1${endpoint}`, config);
        if (!response.ok) throw new Error('API Error');
        return await response.json();
    },

    showView(viewId) {
        document.querySelectorAll('.view').forEach(v => v.classList.remove('active'));
        document.getElementById(viewId).classList.add('active');
        if (viewId === 'branches-view') this.loadBranches();
        if (viewId === 'history-view') this.loadHistory();
        this.updateCartWidget();
        this.renderCart();
    },

    async loadBranches() {
        try {
            const data = await this.api('/branches/');
            const container = document.getElementById('branches-list');
            container.innerHTML = '';
            
            data.branches.forEach(branch => {
                const div = document.createElement('div');
                
                // Вставляем вашу Tailwind разметку
                div.innerHTML = `
                    <div onclick="app.selectBranch(${branch.id})" class="fade-up flex items-center p-5 bg-card rounded-2xl border border-slate-700/50 shadow-md transition active:scale-95 text-txt cursor-pointer">
                        <div class="w-12 h-12 flex items-center justify-center bg-surface rounded-xl mr-4 text-accent flex-shrink-0">
                            <i data-lucide="map-pin" class="w-6 h-6"></i>
                        </div>
                        <div class="flex-1">
                            <span class="block text-lg font-semibold">${branch.name}</span>
                            <span class="block text-sm text-slate-400 mt-0.5">${branch.address}</span>
                        </div>
                        <i data-lucide="chevron-right" class="w-5 h-5 text-slate-500 flex-shrink-0"></i>
                    </div>
                `;
                container.appendChild(div);
            });
            
            // Запускаем отрисовку иконок Lucide для новых элементов, которые вставил JS
            if (window.lucide) {
                window.lucide.createIcons();
            }
            
        } catch (e) {
            console.error('Ошибка загрузки филиалов:', e);
        }
    },

    async selectBranch(branchId) {
        this.currentBranchId = branchId;
        this.showView('menu-view');
        this.loadMenu(branchId);
    },

    // ... (начало объекта app, методы api, showView, loadBranches, selectBranch остаются без изменений)

    async loadMenu(branchId) {
        try {
            // Загружаем ТОЛЬКО категории при открытии меню
            const categoriesData = await this.api(`/categories/?branch_id=${branchId}&limit=150`);
            this.renderCategories(categoriesData.categories);
            
            // Если в филиале есть категории, сразу загружаем товары для первой категории
            if (categoriesData.categories.length > 0) {
                this.loadProductsByCategory(categoriesData.categories[0].id);
            } else {
                document.getElementById('products-grid').innerHTML = '<p style="text-align: center; grid-column: 1 / -1;">В этом филиале пока нет категорий.</p>';
            }
        } catch (e) {
            console.error('Ошибка загрузки меню:', e);
        }
    },

    renderCategories(categories) {
        const nav = document.getElementById('categories-nav');
        nav.innerHTML = '';
        categories.forEach(cat => {
            const btn = document.createElement('button');
            btn.innerText = cat.name;
            // При клике на категорию делаем запрос к API за нужными товарами
            btn.onclick = () => this.loadProductsByCategory(cat.id);
            nav.appendChild(btn);
        });
    },

    async loadProductsByCategory(categoryId) {
        try {
            // Отправляем запрос с указанием branch_id, category_id и limit
            const productsData = await this.api(`/products/?branch_id=${this.currentBranchId}&category_id=${categoryId}&limit=150`);
            this.renderProducts(productsData.products);
        } catch (e) {
            console.error('Ошибка загрузки продуктов категории:', e);
        }
    },

    renderProducts(products) {
        const grid = document.getElementById('products-grid');
        grid.innerHTML = '';
        
        if (!products || products.length === 0) {
            grid.innerHTML = '<p style="grid-column: 1 / -1; text-align: center;">В этой категории пока нет товаров.</p>';
            return;
        }

        products.forEach(prod => {
            const div = document.createElement('div');
            div.className = 'card product-card';
            
            const imageUrl = prod.image_url ? prod.image_url : 'https://via.placeholder.com/150';
            
            div.innerHTML = `
                <img src="${imageUrl}" alt="${prod.name}" style="width: 100%; height: 120px; object-fit: cover; border-radius: 6px; margin-bottom: 8px;">
                <h4 style="margin: 5px 0; font-size: 14px;">${prod.name}</h4>
                <p style="margin: 5px 0; font-weight: bold;">${prod.price} сум</p>
                <button style="width: 100%; padding: 8px; margin-top: auto;" onclick="app.addToCart(${prod.id}, '${prod.name}', ${prod.price})">В корзину</button>
            `;
            
            div.style.display = 'flex';
            div.style.flexDirection = 'column';
            
            grid.appendChild(div);
        });
    },

    // ... (остальные методы cart и orders остаются без изменений)

    addToCart(id, name, price) {
        const existing = this.cart.find(item => item.id === id);
        if (existing) {
            existing.quantity += 1;
        } else {
            this.cart.push({ id, name, price, quantity: 1 });
        }
        this.saveCart();
    },

    saveCart() {
        localStorage.setItem('cart', JSON.stringify(this.cart));
        this.updateCartWidget();
        this.renderCart();
    },

    updateCartWidget() {
        const count = this.cart.reduce((sum, item) => sum + item.quantity, 0);
        document.getElementById('cart-count').innerText = count;
        document.getElementById('cart-widget').style.display = count > 0 ? 'block' : 'none';
    },

    renderCart() {
        const container = document.getElementById('cart-items');
        container.innerHTML = '';
        let total = 0;
        this.cart.forEach((item, index) => {
            total += item.price * item.quantity;
            const div = document.createElement('div');
            div.innerHTML = `
                <p>${item.name} - ${item.quantity} шт. (${item.price * item.quantity} сум)</p>
                <button onclick="app.cart.splice(${index}, 1); app.saveCart()">Удалить</button>
            `;
            container.appendChild(div);
        });
        document.getElementById('total-price').innerText = total;
    },

    async submitOrder() {
        if (this.cart.length === 0) return;
        const address = document.getElementById('address-input').value;
        const payload = {
            branch_id: this.currentBranchId,
            address: address,
            items: this.cart.map(item => ({ product_id: item.id, quantity: item.quantity }))
        };

        try {
            await this.api('/orders/', 'POST', payload);
            this.cart = [];
            this.saveCart();
            window.Telegram.WebApp.close();
        } catch (e) {
            console.error('Ошибка создания заказа');
        }
    },

    async loadHistory() {
        try {
            const data = await this.api('/orders/?limit=150');
            const container = document.getElementById('orders-list');
            container.innerHTML = '';
            data.orders.forEach(order => {
                const div = document.createElement('div');
                div.className = 'card';
                div.innerHTML = `
                    <p>Заказ #${order.id}</p>
                    <p>Статус: ${order.status}</p>
                    <p>Сумма: ${order.total_price}</p>
                `;
                container.appendChild(div);
            });
        } catch (e) {
            console.error(e);
        }
    }
};
document.addEventListener('DOMContentLoaded', () => {
    app.showView('branches-view');
});