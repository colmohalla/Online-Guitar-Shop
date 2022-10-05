DROP TABLE IF EXISTS guitars;

CREATE TABLE guitars
(
    guitar_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    price REAL NOT NULL,
    image TEXT NOT NULL, 
    description TEXT NOT NULL
);

INSERT INTO guitars (guitar_id, name, price, image, description)
VALUES  (101, 'Stratocaster', 1899.99, 'stratocaster.jpg', 'A classic played by the greats. Find your inner Jimi Hendrix with this beautiful 1968 Custom Shop Stratocaster.'),
        (102, 'Les Paul', 2399.99, 'lespaul.jpg', 'The cream of the crop. Used on countless classic albums by everyone ranging from Led Zeppelin to Tool.'),
        (103, 'SG', 1199.99,'sg.jpg', 'Get your double-horned devil today. For those about to rock, we salute you.' ),
        (104, 'Jazzmaster', 1999.99, 'jazzmaster.jpg', 'Not so much used for jazz, but certainly able to make lots of noise.'),
        (105, 'Telecaster', 1499.99, 'telecaster.png', 'An incredibly versatile guitar that can be used for any genre, from country to death metal!'),
        (106, 'Flying-V', 1999.99, 'flyingv.jpg', 'Loud and proud. Only the bravest need apply.'),
        (107, 'Explorer', 1899.99, 'explorer.jpg', 'Channel your inner Edge and show them all what you got. So good you can hang your coat off it.'),
        (108, 'Jaguar', 1399.99, 'jaguar.jpg', 'There''s a reason this is Johnny Marr''s favourite guitar. For those who want a more refine look.'),
        (109, 'ES-335', 2299.99, 'es335.jpg', 'Made famous by the blues greats, this wonderful songbird will sing for days. Just make sure you play sitting down!'),
        (110, 'Mustang', 1599.99, 'mustang.jpg', 'This lightweight guitar was initially released as a budget option for beginners. It is now loved for its versatile sound.');

DROP TABLE IF EXISTS shapes;

CREATE TABLE shapes
(
    product_id INTEGER PRIMARY KEY,
    shape TEXT NOT NULL,
    price REAL NOT NULL
);

INSERT INTO shapes (product_id, shape, price)
VALUES  (201, 'Stratocaster', 800.00),
        (202, 'Les Paul', 1200.00),
        (203, 'SG', 400.00),
        (204, 'Jazzmaster', 900.00),
        (205, 'Telecaster', 400.00),
        (206, 'Flying-V', 900.00),
        (207, 'Explorer', 800.00),
        (208, 'Jaguar', 300.00),
        (209, 'ES-335', 1500.00),
        (210, 'Mustang', 500.00);

DROP TABLE IF EXISTS colours;

CREATE TABLE colours
(
    product_id INTEGER PRIMARY KEY,
    colour TEXT NOT NULL,
    price REAL NOT NULL
);

INSERT INTO colours (product_id, colour, price)
VALUES  (301, 'Candy-Apple Red', 200.00),
        (302, 'Pelham Blue', 260.00),
        (303, 'Olympic White', 300.00),
        (304, 'Bull Black', 340.00),
        (305, 'Shell Pink', 260.00),
        (306, 'Seafoam Green', 400.00),
        (307, 'Sunburst', 500.00),
        (308, 'Gold-Top', 550.00);

DROP TABLE IF EXISTS woods;

CREATE TABLE woods
(
    product_id INTEGER PRIMARY KEY,
    wood_type TEXT NOT NULL,
    price REAL NOT NULL
);

INSERT INTO woods (product_id, wood_type, price)
VALUES  (401, 'Maple', 150.00),
        (402, 'Rosewood', 200.00),
        (403, 'Ebony', 260.00),
        (404, 'Swamp Ash', 190.00),
        (405, 'Alder', 185.00),
        (406, 'Walnut', 210.00);

DROP TABLE IF EXISTS electronics;


CREATE TABLE electronics
(
    product_id INTEGER PRIMARY KEY,
    pickup_type TEXT NOT NULL,
    price REAL NOT NULL
);

INSERT INTO electronics (product_id, pickup_type, price)
VALUES  (501, 'Seymour Duncan P-90', 120.00),
        (502, 'Fender Vintera Single-Coil', 77.00),
        (503, 'Maplegrove 6X Humbucker', 210.00),
        (504, 'Seymour Duncan Double Barrel', 260.00),
        (505, 'Yellowbelly Humbucker', 400.00);

DROP TABLE IF EXISTS users;

CREATE TABLE users
(
    user_id TEXT PRIMARY KEY,
    password TEXT NOT NULL
);



DROP TABLE IF EXISTS admin;

CREATE TABLE admin
(
    admin_id TEXT PRIMARY KEY,
    admin_password TEXT NOT NULL
);

INSERT INTO admin(admin_id, admin_password)
VALUES  ('hello', 'pbkdf2:sha256:260000$OrRjtG9QOi7YeY5T$3f79465e7eae5abacd6022148de4ef6ed92bc29f48b15c685b06ce509a612ccb');


DROP TABLE IF EXISTS orders;

CREATE TABLE orders
(
    guitar TEXT NOT NULL ,
    first_name TEXT NOT NULL,
    surname TEXT NOT NULL,
    address TEXT NOT NULL,
    delivery_method NOT NULL,
    total REAL NOT NULL
);


