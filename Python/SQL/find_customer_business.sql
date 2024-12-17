SELECT c.street_address, c.city, c.state, c.postal_code, c.phone_number, c.email, b.business_name, b.business_tax_id, b.contact_firstname, b.contact_lastname, b.contact_job_title, c.customer_id 
FROM Customer c JOIN Business b ON c.customer_id = b.customer_id WHERE b.business_tax_id = '$business_tax_id';
