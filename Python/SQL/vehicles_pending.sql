SELECT COUNT(DISTINCT(v.vin)) as VEHICLES_PENDING
  FROM Vehicle v
 JOIN 
  (SELECT DISTINCT po.vin
   FROM Parts_Order po  
   JOIN Part p
     ON po.vin = p.vin
     AND po.vendor_name = p.vendor_name
     AND po.order_number = p.order_number
   WHERE p.`status` != 'installed') pp
     ON v.vin = pp.vin
  WHERE sale_date IS NULL;
  

