CREATE TABLE IF NOT EXISTS inventory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    manufacturer TEXT NOT NULL,
    model TEXT,
    firmware_version TEXT,
    agency TEXT NOT NULL,
    criticality TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT NOT NULL,
    agency TEXT
);

INSERT INTO users (username, password, role, agency)
VALUES
('admin', 'admin123', 'Admin', NULL),

('dot_user', 'viewer123', 'Viewer', 'DOT'),

('nypd_user', 'viewer123', 'Viewer', 'NYPD'),

('analyst', 'analyst123', 'Analyst', NULL);