-- Создаем БД
CREATE DATABASE budget;
USE budget;

-- Таблицы
CREATE TABLE expense_items (
    item_id INT,
    name VARCHAR(50)
);

CREATE TABLE sections (
    section_id INT,
    name VARCHAR(50),
    item_id INT,
    unit VARCHAR(20)
);

CREATE TABLE expenses (
    expense_id INT,
    section_id INT,
    date DATE,
    quantity INT,
    price DECIMAL(10,2)
);

-- Заполняем данными
INSERT INTO expense_items VALUES 
(1, 'Продукты'),
(2, 'Транспорт'),
(3, 'Коммунальные');

INSERT INTO sections VALUES 
(1, 'Хлеб', 1, 'шт'),
(2, 'Молоко', 1, 'л'),
(3, 'Проезд', 2, 'поездка'),
(4, 'Электричество', 3, 'кВт');

INSERT INTO expenses VALUES 
(1, 1, '2024-12-01', 2, 50),
(2, 2, '2024-12-01', 1, 80),
(3, 3, '2024-12-02', 10, 40),
(4, 4, '2024-12-03', 100, 5),
(5, 1, '2024-12-10', 1, 50);

-- 1. Месячный бюджет семьи (декабрь 2024)
SELECT SUM(quantity * price) as month_budget
FROM expenses
WHERE MONTH(date) = 12 AND YEAR(date) = 2024;

-- 2. Доля каждой статьи в общем бюджете
SELECT ei.name,
       SUM(e.quantity * e.price) as sum,
       SUM(e.quantity * e.price) * 100 / (
           SELECT SUM(quantity * price) FROM expenses
       ) as percent
FROM expense_items ei, sections s, expenses e
WHERE ei.item_id = s.item_id AND s.section_id = e.section_id
GROUP BY ei.item_id;