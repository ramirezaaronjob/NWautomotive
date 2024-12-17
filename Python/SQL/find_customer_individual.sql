SELECT c.street_address, c.city, c.state, c.postal_code, c.phone_number, c.email, i.first_name, i.last_name, i.ssn, c.customer_id 
FROM Customer c JOIN Individual i ON c.customer_id = i.customer_id WHERE i.ssn = '$ssn';
