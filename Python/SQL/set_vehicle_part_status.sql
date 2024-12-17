UPDATE Part 
   SET status = '$status'
 WHERE vin = '$vin' 
  AND order_number = '$order_number' 
  AND vendor_name = '$vendor_name' 
  AND vendor_part_number = '$vendor_part_number';