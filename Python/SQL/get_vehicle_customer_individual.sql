select concat(i.first_name,' ', i.last_name) as individual_name
     ,c.email ,c.phone_number ,c.street_address ,c.city ,c.state ,c.postal_code
 from Customer c join Individual i
   on c.customer_id = i.customer_id
where c.customer_id = $customer_id;

