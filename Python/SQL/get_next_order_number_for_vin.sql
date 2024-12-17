SELECT LPAD(CAST(SUBSTRING(order_number, LENGTH(vin) + 2) AS UNSIGNED)+1,3,'0') AS next_order 
 FROM Parts_Order WHERE vin = '$vin' 
 ORDER BY next_order DESC LIMIT 1;
