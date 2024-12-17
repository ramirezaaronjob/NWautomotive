UPDATE Vehicle v
   SET sale_date = now()
     , buyer = $customer_id
     , salesperson = '$username'
WHERE v.vin = '$vin';
