CREATE SCHEMA simulated_bank;
CREATE TABLE transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    account_id VARCHAR(20),
    amount INT,
    type VARCHAR(50),
    time DATETIME,
    target_account VARCHAR(50),
    tips VARCHAR(255)
);

INSERT INTO transactions
(account_id, amount, type, time, target_account, tips)
VALUES
('100001', 6000, 'salary', '2026-01-01 08:00:00', 'company_payroll', 'Salary Jan'),
('100001', -1200, 'rent', '2026-01-03 09:00:00', 'landlord', 'Rent Jan'),
('100001', -80, 'transport', '2026-01-05 07:40:00', 'metro', 'Transport card'),
('100001', -150, 'shopping', '2026-01-08 14:20:00', 'mall', 'Shopping'),
('100001', -200, 'transfer', '2026-01-10 12:00:00', '100002', 'Dinner split'),
('100002', 6000, 'salary', '2026-01-01 08:05:00', 'company_payroll', 'Salary Jan'),
('100002', -1000, 'rent', '2026-01-03 09:05:00', 'landlord', 'Rent Jan'),
('100002', -70, 'transport', '2026-01-06 08:00:00', 'metro', 'Bus card'),
('100002', -220, 'shopping', '2026-01-09 15:10:00', 'online_store', 'Online purchase'),
('100002', 200, 'transfer', '2026-01-10 12:00:05', '100001', 'Dinner split'),
('100001', 6000, 'salary', '2026-02-01 08:00:00', 'company_payroll', 'Salary Feb'),
('100001', -1200, 'rent', '2026-02-03 09:00:00', 'landlord', 'Rent Feb'),
('100001', -90, 'transport', '2026-02-05 07:50:00', 'metro', 'Transport card'),
('100001', -180, 'shopping', '2026-02-08 16:00:00', 'mall', 'Groceries'),
('100001', -250, 'transfer', '2026-02-11 12:30:00', '100002', 'Movie tickets'),
('100002', 6000, 'salary', '2026-02-01 08:05:00', 'company_payroll', 'Salary Feb'),
('100002', -1000, 'rent', '2026-02-03 09:05:00', 'landlord', 'Rent Feb'),
('100002', -65, 'transport', '2026-02-06 08:20:00', 'metro', 'Bus card'),
('100002', -210, 'shopping', '2026-02-09 17:00:00', 'online_store', 'Shopping'),
('100002', 250, 'transfer', '2026-02-11 12:30:05', '100001', 'Movie tickets');

CREATE TABLE cus_info (
    account_id VARCHAR(20) PRIMARY KEY,
    password VARCHAR(100),
    name VARCHAR(100),
    phone VARCHAR(20),
    citizen_id VARCHAR(50)
);

INSERT INTO cus_info
(account_id, password, name, phone, citizen_id)
VALUES
('100001', '123456', 'Tom Lee', '91234567', '123456'),
('100002', '123456', 'Chen Yu', '92345678', '234567');