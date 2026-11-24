-- ============================================================
-- StudyTrack – Database Initialization Script
-- Runs automatically on first container start via
-- /docker-entrypoint-initdb.d/init.sql
-- ============================================================

-- Use the database created by MYSQL_DATABASE env var
USE studytrack;

-- -------------------- USERS TABLE --------------------
CREATE TABLE IF NOT EXISTS users (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    name            VARCHAR(100)  NOT NULL,
    email           VARCHAR(150)  NOT NULL UNIQUE,
    password_hash   VARCHAR(255)  NOT NULL,
    created_at      TIMESTAMP     DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- -------------------- ASSIGNMENTS TABLE --------------------
CREATE TABLE IF NOT EXISTS assignments (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    user_id         INT           NOT NULL,
    title           VARCHAR(200)  NOT NULL,
    subject         VARCHAR(100)  NOT NULL,
    description     TEXT,
    due_date        DATE          NOT NULL,
    priority        ENUM('High', 'Medium', 'Low') DEFAULT 'Medium',
    status          ENUM('Pending', 'In Progress', 'Completed') DEFAULT 'Pending',
    created_at      TIMESTAMP     DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP     DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_status (user_id, status),
    INDEX idx_user_due (user_id, due_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- -------------------- EXAMS TABLE --------------------
CREATE TABLE IF NOT EXISTS exams (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    user_id         INT           NOT NULL,
    title           VARCHAR(200)  NOT NULL,
    subject         VARCHAR(100)  NOT NULL,
    exam_type       ENUM('Quiz', 'Lab Exam', 'Mid-Sem', 'Semester Exam') NOT NULL,
    exam_date       DATE          NOT NULL,
    exam_time       TIME,
    syllabus        TEXT,
    venue           VARCHAR(200),
    created_at      TIMESTAMP     DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP     DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_exam_date (user_id, exam_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- -------------------- NOTIFICATION LOG TABLE --------------------
-- Prevents sending duplicate reminder emails.
CREATE TABLE IF NOT EXISTS notification_log (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    user_id         INT           NOT NULL,
    item_type       ENUM('assignment', 'exam') NOT NULL,
    item_id         INT           NOT NULL,
    days_before     INT           NOT NULL,       -- e.g. 1 or 3
    sent_at         TIMESTAMP     DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE KEY uq_notification (user_id, item_type, item_id, days_before)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================================
-- SEED DATA – Optional demo user for screenshots / demos
-- Password: Demo@123  (hashed with werkzeug)
-- ============================================================
INSERT INTO users (name, email, password_hash) VALUES
('Demo Student', 'demo@studytrack.com',
 'scrypt:32768:8:1$FOwLH6ZxU6rBqHyx$d38b21433b13052a63a63e2be7a2b23728d4fcdf1d9e0400b21c9ea353f9d4394013b8468a40f78ecc44f3d658e1976ca163b5cbd9737429644707e932ca4755');

-- Seed assignments for demo user (user_id = 1)
INSERT INTO assignments (user_id, title, subject, description, due_date, priority, status) VALUES
(1, 'Docker Networking Lab Report', 'Cloud Computing', 'Write a lab report on Docker bridge and overlay networks.', DATE_ADD(CURDATE(), INTERVAL 1 DAY), 'High', 'In Progress'),
(1, 'Binary Search Tree Implementation', 'Data Structures', 'Implement BST with insert, delete, and traversal in C++.', DATE_ADD(CURDATE(), INTERVAL 3 DAY), 'Medium', 'Pending'),
(1, 'ER Diagram for Library System', 'Database Management', 'Design a complete ER diagram with all constraints.', DATE_ADD(CURDATE(), INTERVAL -1 DAY), 'High', 'Pending'),
(1, 'Linux Commands Worksheet', 'Operating Systems', 'Complete the worksheet on file permissions and processes.', DATE_ADD(CURDATE(), INTERVAL 7 DAY), 'Low', 'Pending'),
(1, 'REST API Mini Project', 'Web Technology', 'Build a simple REST API using Flask with CRUD operations.', DATE_ADD(CURDATE(), INTERVAL 5 DAY), 'Medium', 'Pending'),
(1, 'TCP/UDP Socket Programming', 'Computer Networks', 'Implement client-server chat using TCP sockets in Python.', DATE_ADD(CURDATE(), INTERVAL -3 DAY), 'Medium', 'Completed');

-- Seed exams for demo user (user_id = 1)
INSERT INTO exams (user_id, title, subject, exam_type, exam_date, exam_time, syllabus, venue) VALUES
(1, 'Cloud Computing Mid-Sem', 'Cloud Computing', 'Mid-Sem', DATE_ADD(CURDATE(), INTERVAL 5 DAY), '10:00:00', 'Docker, Containers, Virtualization, Cloud Models (IaaS/PaaS/SaaS)', 'Room 301, CS Block'),
(1, 'DSA Lab Exam', 'Data Structures', 'Lab Exam', DATE_ADD(CURDATE(), INTERVAL 2 DAY), '14:00:00', 'Linked List, Stack, Queue, BST – hands-on coding', 'Lab 204, IT Block'),
(1, 'DBMS Quiz 3', 'Database Management', 'Quiz', DATE_ADD(CURDATE(), INTERVAL 1 DAY), '09:30:00', 'Normalization, SQL Joins, Transactions', 'Room 102, CS Block'),
(1, 'OS Semester Exam', 'Operating Systems', 'Semester Exam', DATE_ADD(CURDATE(), INTERVAL 15 DAY), '10:00:00', 'Full syllabus – Process, Memory, File, I/O Management', 'Exam Hall A');
