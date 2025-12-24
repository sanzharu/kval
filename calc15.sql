-- Создаем БД
CREATE DATABASE cost;
USE cost;

-- Таблицы
CREATE TABLE cost_items (
    item_id INT,
    name VARCHAR(100)
);

CREATE TABLE products (
    product_id INT,
    name VARCHAR(100)
);

CREATE TABLE calculation (
    calc_id INT,
    product_id INT,
    item_id INT,
    amount DECIMAL(10,2)
);

CREATE TABLE production_plan (
    plan_id INT,
    product_id INT,
    quantity INT
);

-- Заполняем данными
INSERT INTO cost_items VALUES 
(1, 'Материалы'),
(2, 'Зарплата'),
(3, 'Электроэнергия');

INSERT INTO products VALUES 
(1, 'Изделие А'),
(2, 'Изделие Б');

INSERT INTO calculation VALUES 
(1, 1, 1, 5000),
(2, 1, 2, 3000),
(3, 2, 1, 7000),
(4, 2, 2, 4000),
(5, 2, 3, 1000);

INSERT INTO production_plan VALUES 
(1, 1, 100),
(2, 2, 50);

-- 1. Суммарная себестоимость выпуска изделий на план
SELECT SUM(c.amount * p.quantity) as total_cost
FROM calculation c, production_plan p
WHERE c.product_id = p.product_id;

-- 2. Доля каждой статьи затрат в общей себестоимости
SELECT 
    ci.name,
    SUM(c.amount * p.quantity) as item_total,
    ROUND(SUM(c.amount * p.quantity) * 100 / (
        SELECT SUM(c2.amount * p2.quantity)
        FROM calculation c2, production_plan p2
        WHERE c2.product_id = p2.product_id
    ), 2) as percent
FROM cost_items ci, calculation c, production_plan p
WHERE ci.item_id = c.item_id 
    AND c.product_id = p.product_id
GROUP BY ci.item_id, ci.name;