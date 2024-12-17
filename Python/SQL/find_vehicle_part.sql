SELECT vin, vendor_name, order_number, vendor_part_number, description, status, unit_price, quantity 
FROM Part 
WHERE vin = '$vin' 
AND order_number = '$order_number' 
AND vendor_name = '$vendor_name' 
AND vendor_part_number = '$vendor_part_number';
