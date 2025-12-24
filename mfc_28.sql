-- Создание базы данных МФЦ
CREATE DATABASE IF NOT EXISTS mfc;
USE mfc;

-- Типы документов (услуги МФЦ)
CREATE TABLE doc_types (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    processing_days INT DEFAULT 30
);

-- Заявители
CREATE TABLE applicants (
    id INT PRIMARY KEY AUTO_INCREMENT,
    full_name VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    registration_date DATE DEFAULT (CURDATE())
);

-- Заявки на документы
CREATE TABLE applications (
    id INT PRIMARY KEY AUTO_INCREMENT,
    applicant_id INT,
    doc_type_id INT,
    application_date DATE DEFAULT (CURDATE()),
    status VARCHAR(20) DEFAULT 'pending', -- pending, processing, completed
    completion_date DATE,
    FOREIGN KEY (applicant_id) REFERENCES applicants(id),
    FOREIGN KEY (doc_type_id) REFERENCES doc_types(id)
);

-- Социальные карты (особый случай)
CREATE TABLE social_cards (
    id INT PRIMARY KEY AUTO_INCREMENT,
    applicant_id INT,
    application_id INT,
    temp_card_issued DATE, -- дата выдачи временной карты
    temp_card_expires DATE, -- срок действия временной (45 дней)
    perm_card_ready DATE, -- дата готовности постоянной карты
    FOREIGN KEY (applicant_id) REFERENCES applicants(id),
    FOREIGN KEY (application_id) REFERENCES applications(id)
);

-- Вставка тестовых данных
INSERT INTO doc_types (name, processing_days) VALUES
('Детский сад (очередь)', 60),
('Ежемесячное пособие', 14),
('Пенсионное страховое свидетельство', 21),
('Заграничный паспорт', 30),
('Паспорт гражданина РФ', 14),
('Социальная карта', 45);

INSERT INTO applicants (full_name, phone) VALUES
('Иванов Иван Иванович', '+7(999)111-22-33'),
('Петрова Мария Сергеевна', '+7(999)222-33-44'),
('Сидоров Алексей Петрович', '+7(999)333-44-55'),
('Кузнецова Ольга Викторовна', '+7(999)444-55-66');

INSERT INTO applications (applicant_id, doc_type_id, application_date, status) VALUES
(1, 1, '2024-12-01', 'completed'),
(1, 6, '2024-12-10', 'processing'),
(2, 2, '2024-12-05', 'completed'),
(2, 3, '2024-12-15', 'pending'),
(3, 4, '2024-12-03', 'processing'),
(3, 5, '2024-12-12', 'pending'),
(4, 6, '2024-12-08', 'processing'),
(1, 5, '2024-12-20', 'pending');

INSERT INTO social_cards (applicant_id, application_id, temp_card_issued, temp_card_expires) VALUES
(1, 2, '2024-12-10', '2025-01-24'), -- 45 дней
(4, 7, '2024-12-08', '2025-01-22');