INSERT INTO Business (customer_id, business_tax_id, business_name, contact_firstname, contact_lastname, contact_job_title) 
VALUES (LAST_INSERT_ID(), '$business_tax_id', '$business_name', '$contact_firstname', '$contact_lastname', '$contact_job_title');
