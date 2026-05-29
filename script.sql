-- =====================================================
-- 1. Branches (4 филиала)
-- =====================================================
INSERT INTO branches (id, name, branch_code, description, address, landmark, latitude, longitude, delivery_price, is_active, created_at, updated_at)
VALUES
  (1, 'Центральный', 'BR001', 'Главный офис', 'ул. Ленина, 25', 'ТЦ "Центральный"', 55.7558, 37.6176, 150.00, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  (2, 'Северный', 'BR002', 'Филиал в северном районе', 'пр. Мира, 12', 'ост. "Северная"', 55.8756, 37.6537, 200.00, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  (3, 'Южный', 'BR003', 'Обслуживание юга', 'ул. Южная, 8', 'парк "Южный"', 55.6532, 37.5831, 180.00, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  (4, 'Восточный', 'BR004', 'Восточный округ', 'Восточное шоссе, 45', 'метро "Восточная"', 55.7925, 37.7213, 220.00, 0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- =====================================================
-- 2. Categories (6 категорий, с description)
-- =====================================================
INSERT INTO categories (id, name, description, branch_id, is_active, created_at, updated_at)
VALUES
  (1, 'Пицца',   'Итальянские пиццы на тонком тесте', 1, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  (2, 'Роллы',   'Японские роллы и суши', 1, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  (3, 'Бургеры', 'Сочные бургеры с говядиной', 2, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  (4, 'Суши',    'Сеты и отдельные суши', 2, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  (5, 'Напитки', 'Газировка, соки, вода', 3, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  (6, 'Десерты', 'Торты, пирожные, мороженое', 4, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- =====================================================
-- 3. Users (6 пользователей: 2 customer, 2 operator, 2 courier)
-- =====================================================
INSERT INTO users (id, telegram_id, phone_number, first_name, username, hashed_pwd, role, branch_id, created_at, updated_at)
VALUES
  (1, 100000001, '+79999999999', 'Алексей', 'alex_cust', '$2b$12$abc123hashedpassword1', 'customer', 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  (2, 100000002, '+79999999998', 'Мария',   'maria_cust','$2b$12$abc123hashedpassword2', 'customer', 2, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  (3, 100000003, '+79999999997', 'Олег',    'oleg_op',   '$2b$12$abc123hashedpassword3', 'operator', 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  (4, 100000004, '+79999999996', 'Ирина',   'irina_op',  '$2b$12$abc123hashedpassword4', 'operator', 2, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  (5, 100000005, '+79999999995', 'Дмитрий', 'dima_cour', '$2b$12$abc123hashedpassword5', 'courier',  1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  (6, 100000006, '+79999999994', 'Елена',   'elena_cour','$2b$12$abc123hashedpassword6', 'courier',  2, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- =====================================================
-- 4. Products (6 продуктов, с image_url)
-- =====================================================
INSERT INTO products (id, name, api_id, uzname, runame, enname, description, img, image_url, img_file_id, price, category_id, subcategoryindex, branch_id, is_active, created_at, updated_at)
VALUES
  (1, 'Маргарита', 'pizza_marg', 'Margarita', 'Маргарита', 'Margherita', 'Классическая пицца', 'pizza_marg.jpg', 'https://example.com/images/pizza_marg.jpg', 'file_001', 350.00, 1, 1, 1, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  (2, 'Филадельфия', 'roll_phil', 'Filadelfiya', 'Филадельфия', 'Philadelphia', 'Ролл с лососем', 'roll_phil.jpg', 'https://example.com/images/roll_phil.jpg', 'file_002', 480.00, 2, 1, 1, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  (3, 'Чизбургер', 'burger_cheese', 'Chizburger', 'Чизбургер', 'Cheeseburger', 'Говяжья котлета с сыром', 'burger_cheese.jpg', 'https://example.com/images/burger_cheese.jpg', 'file_003', 250.00, 3, 1, 2, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  (4, 'Калифорния', 'sushi_calif', 'Kaliforniya', 'Калифорния', 'California', 'Ролл с крабом', 'sushi_calif.jpg', 'https://example.com/images/sushi_calif.jpg', 'file_004', 520.00, 4, 1, 2, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  (5, 'Кока-Кола', 'coke', 'Koka-Kola', 'Кока-Кола', 'Coca-Cola', '0.5 л', 'coke.jpg', 'https://example.com/images/coke.jpg', 'file_005', 90.00, 5, 1, 3, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  (6, 'Тирамису', 'tiramisu', 'Tiramisu', 'Тирамису', 'Tiramisu', 'Итальянский десерт', 'tiramisu.jpg', 'https://example.com/images/tiramisu.jpg', 'file_006', 210.00, 6, 1, 4, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- =====================================================
-- 5. Orders (6 заказов)
-- =====================================================
INSERT INTO orders (id, customer_id, operator_id, courier_id, branch_id, status, payment_method, total_price, is_accepted, address, landmark, latitude, longitude, created_at, updated_at)
VALUES
  (1, 1, 3, 5, 1, 'delivered', 'cash', 830.00, 1, 'ул. Ленина, 10, кв.5', 'подъезд 2', 55.7550, 37.6170, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  (2, 1, 3, 5, 1, 'delivered', 'card', 480.00, 1, 'ул. Пушкина, 15', 'домофон 123', 55.7560, 37.6180, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  (3, 2, 4, 6, 2, 'in_transit', 'cash', 520.00, 1, 'пр. Мира, 34', 'офис 7', 55.8760, 37.6540, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  (4, 2, 4, 6, 2, 'preparing', 'card', 250.00, 1, 'ул. Гагарина, 5', 'сторона двора', 55.8740, 37.6520, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  (5, 1, 3, 5, 3, 'pending',   'cash', 90.00,  0, 'ул. Южная, 12', NULL, 55.6540, 37.5840, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  (6, 2, 4, 6, 4, 'confirmed',  'card', 210.00, 1, 'Восточное шоссе, 78', 'ТЦ "Восток"', 55.7930, 37.7220, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- =====================================================
-- 6. Order_items (6 позиций, поле price вместо price_at_purchase)
-- =====================================================
INSERT INTO order_items (id, order_id, product_id, quantity, price, created_at, updated_at)
VALUES
  (1, 1, 1, 1, 350.00, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  (2, 1, 5, 1, 90.00,  CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  (3, 2, 2, 1, 480.00, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  (4, 3, 4, 1, 520.00, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  (5, 4, 3, 1, 250.00, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  (6, 6, 6, 1, 210.00, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- =====================================================
-- 7. Messages (6 сообщений)
-- =====================================================
INSERT INTO messages (id, sender_id, order_id, text, created_at, updated_at)
VALUES
  (1, 1, 1, 'Здравствуйте, когда привезут заказ?', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  (2, 3, 1, 'Здравствуйте, курьер уже в пути', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  (3, 2, 3, 'Можно заменить напиток?', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  (4, 4, 3, 'Да, конечно, напишите какой', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  (5, 1, 2, 'Спасибо за быструю доставку!', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  (6, 2, 4, 'Когда будет готов заказ?', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- =====================================================
-- 8. Payment_logs (4 записи, добавлено поле status)
-- =====================================================
INSERT INTO payment_logs (id, order_id, courier_id, branch_id, amount, payment_method, status, is_closed, created_at, updated_at)
VALUES
  (1, 1, 5, 1, 830.00, 'cash', 'completed', 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  (2, 2, 5, 1, 480.00, 'card', 'completed', 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  (3, 3, 6, 2, 520.00, 'cash', 'pending',  0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  (4, 6, 6, 4, 210.00, 'card', 'pending',  0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);