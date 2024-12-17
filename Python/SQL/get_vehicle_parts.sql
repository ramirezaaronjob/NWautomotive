select p.vendor_part_number, p.`description`, p.vendor_name
	  ,p.order_number, CONCAT('$',FORMAT(p.unit_price,2,'en_us')) as unit_price, p.quantity, p.`status`
FROM Part p
where p.vin = '$vin'
order by p.order_number, p.vendor_part_number;

