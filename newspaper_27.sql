CREATE DATABASE IF NOT EXISTS newspaper;
USE newspaper;
-- Таблица авторов
CREATE TABLE IF NOT EXISTS authors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL
);
-- Таблица статей
CREATE TABLE IF NOT EXISTS articles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    content TEXT,
    author_id INT,
    line_count INT,
    status VARCHAR(20) DEFAULT 'pending',
    created_date DATE,
    check_date DATE
);

-- Таблица выплат
CREATE TABLE IF NOT EXISTS payments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    author_id INT,
    article_id INT,
    amount DECIMAL(10, 2),
    payment_date DATE
);

-- Тестовые данные
INSERT INTO authors (full_name) VALUES
('Иванов Петр'),
('Смирнова Анна'),
('Кузнецов Михаил');

INSERT INTO articles (title, content, author_id, line_count, status, created_date) VALUES
('Статья 1', 'Текст статьи 1...', 1, 10, 'pending', '2024-01-15'),
('Статья 2', 'Текст статьи 2...', 2, 15, 'pending', '2024-01-15'),
('Статья 3', 'Текст статьи 3...', 3, 12, 'approved', '2024-01-14'),
('Статья 4', 'Текст статьи 4...', 1, 20, 'pending', '2024-01-16');

INSERT INTO payments (author_id, article_id, amount, payment_date) VALUES
(1, 3, 1120.00, '2024-01-15'),
(2, 3, 1120.00, '2024-01-15'),
(1, 3, 1120.00, '2024-01-20');