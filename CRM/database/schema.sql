-- Database Schema for CRM

CREATE TABLE IF NOT EXISTS leads (
    lead_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    service VARCHAR(255),
    message TEXT,
    status ENUM('New', 'Follow-Up', 'Contract', 'Project Given', 'Finished') DEFAULT 'New',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS email_templates (
    template_id INT AUTO_INCREMENT PRIMARY KEY,
    status ENUM('New', 'Follow-Up', 'Contract', 'Project Given', 'Finished') UNIQUE,
    subject VARCHAR(255) NOT NULL,
    body TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS notifications (
    notification_id INT AUTO_INCREMENT PRIMARY KEY,
    message TEXT NOT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Stored Procedures

DELIMITER //

CREATE PROCEDURE InsertMetaLead(
    IN p_name VARCHAR(255),
    IN p_email VARCHAR(255),
    IN p_phone VARCHAR(20),
    IN p_service VARCHAR(255),
    IN p_message TEXT
)
BEGIN
    INSERT INTO leads (customer_name, email, phone, service, message, status)
    VALUES (p_name, p_email, p_phone, p_service, p_message, 'New');
    
    INSERT INTO notifications (message)
    VALUES (CONCAT('New lead received: ', p_name));
END //

CREATE PROCEDURE UpdateLeadStatus(
    IN p_lead_id INT,
    IN p_status ENUM('New', 'Follow-Up', 'Contract', 'Project Given', 'Finished')
)
BEGIN
    UPDATE leads SET status = p_status WHERE lead_id = p_lead_id;
    
    INSERT INTO notifications (message)
    VALUES (CONCAT('Lead ID ', p_lead_id, ' status updated to ', p_status));
END //

CREATE PROCEDURE FetchLeadsByStatus(
    IN p_status VARCHAR(50)
)
BEGIN
    IF p_status = 'All' THEN
        SELECT * FROM leads ORDER BY created_at DESC;
    ELSE
        SELECT * FROM leads WHERE status = p_status ORDER BY created_at DESC;
    END IF;
END //

DELIMITER ;

-- Initial Email Templates
INSERT INTO email_templates (status, subject, body) VALUES
('New', 'Welcome to our service!', 'Hi {name}, thanks for reaching out. We will get back to you soon.'),
('Follow-Up', 'Following up on your inquiry', 'Hi {name}, just checking in to see if you have any questions.'),
('Contract', 'Your Contract is Ready', 'Hi {name}, please find the attached contract for your project.'),
('Project Given', 'Project Details & Next Steps', 'Hi {name}, we have received the project. Here are the details...'),
('Finished', 'Project Completed!', 'Hi {name}, your project is now finished. Thank you for choosing us!');
