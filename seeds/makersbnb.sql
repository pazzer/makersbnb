-- The job of this file is to reset all of our important database tables.
-- And add any data that is needed for the tests to run.
-- This is so that our tests, and application, are always operating from a fresh
-- database state, and that tests don't interfere with each other.

------------------------ users ------------------------

-- Delete (drop) all our tables
DROP TABLE IF EXISTS users CASCADE;
DROP SEQUENCE IF EXISTS users_id_seq;

-- Recreate them
CREATE SEQUENCE IF NOT EXISTS users_id_seq;
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    email_address VARCHAR(255),
    password VARCHAR(255),
    name VARCHAR(255)
);

-- Add any records that are needed for the tests to run

-- These passwords have been created like so:
--    password = '12345678!'
--    utf8_password = password.encode('utf-8')
--    hashed = bcrypt.hashpw(utf8_password, bcrypt.gensalt())
--    hex_hashed_password = hashed.hex()
-- The value of `hex_hashed_password` is the value stored in the 'password' column.
INSERT INTO users (email_address, password, name) VALUES
-- id: 1
('alice@example.com',
'243262243132244c637232783267554c6b4b677a3472754c645857306567476451522f38517346646c52426d7334736a547159656372445037733769',
'Alice'),
-- password123!

-- id: 2
('bob@example.com',
'2432622431322444307a4a4a464b6c79686c7a3062494a5832636f4f753263615077516761435257536e7a786470576c564d58516e464c4d62534843',
'Bob'),
-- _@qwerty456£

-- id: 3
('carol@example.com',
'24326224313224634b45356d65626b6a555971725762454d7056494a2e5457577231497a73344e6876617665303948324c5338685264323961656671',
'Carol'),
-- securepass789$$^

-- id: 4
('dave@example.com',
'243262243132246d345154686d5534536d64732e4a756575464630774f76454b744469756951576234726e6630535a416d4c4c6f766d2f31396a4979',
'Dave'),
-- &&let&mei&n321

-- id: 5
('eve@example.com',
'2432622431322468724b72786a325936667765544173637944546a4a4f4257515356664367654f63516674663979516468376f707135745436787979',
'Eve'),
-- a@dmi£n1234

-- id: 6
('developer@example.com',
'24326224313224736c3978776b566563534e4d69377057625771757865474a70386b3063413579634c666d5763706261514b7a444450504b50656343',
'Developer'),
-- ev@fr£pa!ze^abcd_pw

-- id: 7
('rory@example.com',
'24326224313224584a7a6a5a4b4b4b474e5232756236784a68474b534f514f384f3068437638767430347a7531436278636d715466367539304b6757',
'Rory'),
-- 4gtdWRT435Dn!£

-- id: 8
('laura@example.com',
'243262243132246a65596e72596b696e61386455577039473441304d2e564447392e584246326a4858484d3747682f535073777674795a7941766857',
'Laura');
-- 23sdf728jgv[];!
------------------------ spaces ------------------------

-- Delete (drop) all our tables
DROP TABLE IF EXISTS spaces CASCADE;
DROP SEQUENCE IF EXISTS spaces_id_seq;

-- Recreate them
CREATE SEQUENCE IF NOT EXISTS spaces_id_seq;
CREATE TABLE spaces (
    space_id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    description VARCHAR(255),
    price_per_night INT,
    user_id INT,
        CONSTRAINT fk_users FOREIGN KEY(user_id) REFERENCES users(user_id)
        ON DELETE CASCADE
);

-- Add any records that are needed for the tests to run
INSERT INTO spaces (name, description, price_per_night, user_id) VALUES
('Cozy Cabin', 'Rustic cabin in the forest.', 100, 1), -- Owned by Alice
('Urban Loft', 'Sleek apartment in downtown.', 150, 2), -- Owned by Bob
('Beach Bungalow', 'Sunny spot by the sea.', 200, 3), -- Owned by Carol
('Mountain Retreat', 'Quiet escape in the hills.', 180, 4), -- Owned by Dave
('Modern Studio', 'Compact yet luxurious.', 120, 5), -- Owned by Eve
('Cool Castle', 'Spacious but drafty.', 99, 6); -- Owned by Rory

------------------------ available_ranges ------------------------

-- Delete (drop) all our tables
DROP TABLE IF EXISTS available_ranges CASCADE;
DROP SEQUENCE IF EXISTS available_ranges_id_seq;

-- Recreate them
CREATE SEQUENCE IF NOT EXISTS available_ranges_id_seq;
CREATE TABLE available_ranges (
    availability_id SERIAL PRIMARY KEY,
    start_range DATE,
    end_range DATE,
    space_id INT,
        CONSTRAINT fk_spaces FOREIGN KEY(space_id) REFERENCES spaces(space_id)
        ON DELETE CASCADE
);

-- Add any records that are needed for the tests to run
INSERT INTO available_ranges (start_range, end_range, space_id) VALUES
('2025-06-01', '2025-06-10', 1), -- 'Crazy Cabin,
('2025-06-05', '2025-06-15', 2), -- 'Urban Loft'
('2025-07-01', '2025-07-10', 3), -- 'Beach Bungalow'
('2025-07-15', '2025-07-25', 4), -- 'Mountain Retreat'
('2025-08-01', '2025-08-10', 5), -- 'Modern Studio'
('2025-09-01', '2025-12-31', 6); -- 'Cool Castle'

------------------------ bookings ------------------------

-- Delete (drop) all our tables
DROP TABLE IF EXISTS bookings CASCADE;
DROP SEQUENCE IF EXISTS bookings_id_seq;

-- Recreate them
CREATE SEQUENCE IF NOT EXISTS bookings_id_seq;
CREATE TABLE bookings (
    booking_id SERIAL PRIMARY KEY,
    start_range DATE,
    end_range DATE,
    space_id INT,
        CONSTRAINT fk_spaces FOREIGN KEY(space_id) REFERENCES spaces(space_id)
        ON DELETE CASCADE,
    user_id INT,
        CONSTRAINT fk_users FOREIGN KEY(user_id) REFERENCES users(user_id)
        ON DELETE CASCADE,
    is_confirmed BOOLEAN
);

-- Add any records that are needed for the tests to run
INSERT INTO bookings (start_range, end_range, space_id, user_id, is_confirmed) VALUES
('2025-06-02', '2025-06-05', 1, 2, FALSE), --  1, Cozy Cabin, requested by bob
('2025-06-06', '2025-06-09', 2, 3, FALSE), --  2. Urban Loft, requested by carol
('2025-07-02', '2025-07-04', 3, 4, FALSE), --  3, Beach Bungalow, requested by dave
('2025-07-16', '2025-07-20', 4, 5, FALSE), --  4, Mountain Retreat, requested by eve
('2025-08-02', '2025-08-06', 5, 1, FALSE), --  5, Modern Studio, requested by alice
('2025-08-04', '2025-08-11', 5, 2, TRUE),  --  6, Modern Studio, requested by bob
('2025-06-17', '2025-06-22', 5, 2, TRUE),  --  7, Modern Studio, requested by bob
('2025-07-02', '2025-07-06', 5, 4, TRUE),  --  8, Modern Studio, requested by dave
('2025-07-02', '2025-07-06', 5, 3, FALSE), --  9, Modern Studio, requested by carol

('2025-09-12', '2025-09-15', 6, 2, FALSE), -- 10, Cool Castle, requested by Bob
('2025-09-05', '2025-09-13', 6, 5, FALSE), -- 11, Cool Castle, requested by Eve
('2025-09-23', '2025-09-26', 6, 3, FALSE), -- 12, Cool Castle, requested by Carol
('2025-09-21', '2025-09-23', 6, 4, FALSE), -- 13, Cool Castle, requested by Dave
('2025-10-03', '2025-10-09', 6, 1, TRUE),  -- 14, Cool Castle, requested by Alice
('2025-10-13', '2025-10-28', 6, 5, FALSE), -- 15, Cool Castle, requested by Eve
('2025-11-17', '2025-11-26', 6, 2, TRUE), --  16, Cool Castle, requested by Bob
('2025-11-30', '2025-12-03', 6, 3, FALSE), -- 17, Cool Castle, requested by Carol
('2025-12-08', '2025-12-12', 6, 3, FALSE), -- 18, Cool Castle, requested by Carol
('2025-12-09', '2025-12-12', 6, 2, FALSE), -- 19, Cool Castle, requested by Bob
('2025-12-12', '2025-12-18', 6, 5, FALSE), -- 20, Cool Castle, requested by Eve
('2025-12-23', '2025-12-25', 6, 4, TRUE),  -- 21, Cool Castle, requested by Dave
('2025-12-29', '2025-12-31', 6, 4, TRUE);  -- 22, Cool Castle, requested by Dave











