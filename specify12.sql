-- Создаем БД
CREATE DATABASE specification;
USE specification;

-- Таблицы
CREATE TABLE sections (
    section_id INT,
    name VARCHAR(100)
);

CREATE TABLE items (
    item_id INT,
    designation VARCHAR(50),
    name VARCHAR(100),
    unit VARCHAR(20)
);

CREATE TABLE composition (
    comp_id INT,
    node_id INT,
    subnode_id INT,
    quantity INT,
    position INT
);

-- Заполняем данными
INSERT INTO sections VALUES 
(1, 'Детали'),
(2, 'Стандартные изделия'),
(3, 'Материалы');

INSERT INTO items VALUES 
(1, 'Д-001', 'Корпус', 'шт'),
(2, 'СИ-001', 'Болт М6', 'шт'),
(3, 'М-001', 'Сталь', 'кг'),
(4, 'СИ-002', 'Гайка М6', 'шт'),
(5, 'Д-002', 'Крышка', 'шт');

INSERT INTO composition VALUES 
(1, 100, 1, 1, 1),
(2, 100, 2, 4, 2),
(3, 100, 4, 4, 3),
(4, 100, 3, 2, 4);

-- 1. Спецификация по изделию (код узла=100)
SELECT s.name, i.designation, i.name, i.unit, c.quantity
FROM sections s, items i, composition c
WHERE i.item_id = c.subnode_id 
    AND s.section_id = i.item_id
    AND c.node_id = 100
ORDER BY s.section_id, c.position;

-- 2. Алфавитный список стандартных изделий
SELECT name, designation
FROM items
WHERE designation = 'Стандартные изделия'
ORDER BY name;