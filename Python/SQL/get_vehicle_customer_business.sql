select concat(b.contact_firstname,' ',b.contact_lastname) as contact_name
     ,b.contact_job_title, b.business_name
     ,c.email ,c.phone_number ,c.street_address ,c.city ,c.state ,c.postal_code
 from Customer c join Business b
   on c.customer_id = b.customer_id
where c.customer_id = $customer_id;
