-- ============================================
-- Programs
-- ============================================

INSERT INTO programs (name, department) VALUES
('Computer Science', 'Computer Science'),
('Data Science', 'Computer Science'),
('Software Engineering', 'Computer Science'),
('Business Administration', 'Business'),
('Mathematics', 'Mathematics');


-- ============================================
-- Courses
-- ============================================

INSERT INTO courses (code, name, credits, program_id) VALUES
('CS101', 'Introduction to Programming', 6, 1),
('CS102', 'Database Systems', 6, 1),
('CS103', 'Computer Networks', 5, 1),
('CS104', 'Operating Systems', 6, 1),

('DS101', 'Statistics', 6, 2),
('DS102', 'Machine Learning', 6, 2),
('DS103', 'Data Visualization', 5, 2),
('DS104', 'Data Engineering', 6, 2),

('SE101', 'Software Architecture', 6, 3),
('SE102', 'Software Testing', 5, 3),
('SE103', 'DevOps', 5, 3),
('SE104', 'Web Engineering', 6, 3),

('BA101', 'Accounting', 5, 4),
('BA102', 'Marketing', 5, 4),
('BA103', 'Financial Management', 6, 4),
('BA104', 'Business Analytics', 6, 4),

('MA101', 'Calculus', 6, 5),
('MA102', 'Linear Algebra', 6, 5),
('MA103', 'Probability', 5, 5),
('MA104', 'Discrete Mathematics', 5, 5);

-- ============================================
-- Students
-- ============================================

INSERT INTO students
(first_name, last_name, birth_date, program_id, enrollment_year)
VALUES
('Adam', 'Martin', '2001-03-12', 1, 2022),
('Sarah', 'Dubois', '2002-07-21', 1, 2023),
('Lucas', 'Bernard', '2001-11-05', 1, 2022),
('Emma', 'Leroy', '2002-01-18', 1, 2023),
('Hugo', 'Moreau', '2000-09-30', 1, 2021),

('Nora', 'Laurent', '2002-04-14', 2, 2023),
('Louis', 'Simon', '2001-06-22', 2, 2022),
('Chloe', 'Michel', '2002-10-11', 2, 2023),
('Nathan', 'Garcia', '2001-02-28', 2, 2022),
('Lea', 'Roux', '2003-05-17', 2, 2023),

('Thomas', 'Fournier', '2001-08-19', 3, 2022),
('Alice', 'Girard', '2002-03-25', 3, 2023),
('Jules', 'Andre', '2001-12-09', 3, 2022),
('Camille', 'Mercier', '2002-06-03', 3, 2023),
('Arthur', 'Dupont', '2000-11-27', 3, 2021),

('Sophie', 'Lambert', '2002-02-13', 4, 2023),
('Gabriel', 'Bonnet', '2001-07-08', 4, 2022),
('Manon', 'Francois', '2002-09-16', 4, 2023),
('Antoine', 'Legrand', '2001-04-02', 4, 2022),
('Julie', 'Gauthier', '2003-01-29', 4, 2023),

('Paul', 'Robert', '2001-05-11', 5, 2022),
('Ines', 'Petit', '2002-08-24', 5, 2023),
('Maxime', 'Durand', '2001-10-06', 5, 2022),
('Clara', 'Richard', '2002-12-15', 5, 2023),
('Theo', 'Morel', '2000-06-20', 5, 2021);

-- ============================================
-- Enrollments
-- ============================================

INSERT INTO enrollments
(student_id, course_id, academic_year, semester)
SELECT
    s.id,
    c.id,
    2025,
    1
FROM students s
JOIN courses c
    ON c.program_id = s.program_id
WHERE s.enrollment_year <= 2025
  AND c.id % 2 = 0;

  -- ============================================
-- Exams
-- ============================================

INSERT INTO exams (course_id, exam_date, exam_type)
SELECT
    id,
    '2025-06-15',
    'Final'
FROM courses;

-- ============================================
-- Exam Results
-- ============================================

INSERT INTO exam_results
(exam_id, student_id, score, passed)
SELECT
    e.id,
    en.student_id,
    CASE
        WHEN (en.student_id + e.course_id) % 10 < 2 THEN 8
        WHEN (en.student_id + e.course_id) % 10 < 4 THEN 10
        WHEN (en.student_id + e.course_id) % 10 < 6 THEN 12
        WHEN (en.student_id + e.course_id) % 10 < 8 THEN 14
        ELSE 17
    END AS score,
    CASE
        WHEN (en.student_id + e.course_id) % 10 < 2 THEN FALSE
        ELSE TRUE
    END AS passed
FROM enrollments en
JOIN exams e
    ON e.course_id = en.course_id;