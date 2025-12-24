create database AutoVoksal;
use AutoVoksal;

create table stations(
station_id int primary key auto_increment,
name varchar(255));

create table bus(
bus_id int primary key auto_increment,
mark_bus varchar(255),
gos_number varchar(255),
vmest int);

create table race(
race_id int primary key auto_increment,
station_id int,
bus_id int,
date_otp date);

-- Заполнение таблицы stations
INSERT INTO stations (name) VALUES 
('Центральный автовокзал'),
('Северный вокзал'),
('Южный автовокзал'),
('Западная станция'),
('Восточный терминал'),
('Железнодорожный вокзал'),
('Аэропорт'),
('Пригородный вокзал'),
('Автостанция "Центр"'),
('Междугородний терминал');

-- Заполнение таблицы bus
INSERT INTO bus (mark_bus, gos_number, vmest) VALUES 
('Mercedes Sprinter', 'A123BC', 18),
('ПАЗ-3205', 'B456DE', 25),
('Volkswagen Crafter', 'C789FG', 20),
('Ford Transit', 'D012HI', 16),
('ГАЗель Next', 'E345JK', 14),
('Hyundai County', 'F678LM', 22),
('Iveco Daily', 'G901NO', 28),
('MAN TGE', 'H234PQ', 19),
('Fiat Ducato', 'I567RS', 17),
('Луидор', 'J890TU', 30);

-- Заполнение таблицы race
INSERT INTO race (station_id, bus_id, date_otp) VALUES 
(1, 3, '2024-03-15'),
(2, 1, '2024-03-15'),
(3, 5, '2024-03-16'),
(1, 2, '2024-03-16'),
(4, 7, '2024-03-17'),
(5, 4, '2024-03-17'),
(6, 9, '2024-03-18'),
(7, 6, '2024-03-18'),
(8, 10, '2024-03-19'),
(9, 8, '2024-03-19'),
(10, 3, '2024-03-20'),
(1, 1, '2024-03-20'),
(2, 5, '2024-03-21'),
(3, 7, '2024-03-21'),
(4, 2, '2024-03-22');

select r.mark_bus, r.gos_number, sum(r.vmest) as total
from bus r
group by r.vmest, r.mark_bus, r.gos_number

select r.station_id, count(bus_id) as total_race
from race r
group by r.station_id