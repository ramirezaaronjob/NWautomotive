INSERT INTO Individual (customer_id, ssn, first_name, last_name) 
VALUES 
(LAST_INSERT_ID(), '$ssn', '$first_name', '$last_name');
