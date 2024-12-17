SELECT count(1) as customer_found 
FROM Customer c 
WHERE customer_id = $customer_id;
