create database Time2order;
use Time2order;
CREATE TABLE vendors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL
);
select * from vendors;
CREATE TABLE yettoapprove (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    mobile_number VARCHAR(15) NOT NULL,
    email VARCHAR(100) NOT NULL,
    shop_name VARCHAR(100) NOT NULL,
    shop_owner_name VARCHAR(100) NOT NULL,
    map_link TEXT NOT NULL,
    category VARCHAR(50) NOT NULL,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
select * from yettoapprove;

CREATE TABLE IF NOT EXISTS products (
    id INT PRIMARY KEY AUTO_INCREMENT,
    vendor_username VARCHAR(255),
    product_name VARCHAR(255),
    product_image VARCHAR(255),
    product_price DECIMAL(10, 2),
    product_measure VARCHAR(50),
    availability VARCHAR(50)
);
select * from products;

