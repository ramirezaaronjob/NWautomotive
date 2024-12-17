SELECT vt.type_name as "Vehicle Type" 
  , CASE WHEN COUNT(DISTINCT(v.vin)) = 0 THEN 'N/A' ELSE  COUNT(distinct(v.vin)) END AS "Vehicles Sold"
  , CASE WHEN ROUND(AVG(days_in_inventory)) IS NULL THEN 'N/A' ELSE ROUND(avg(days_in_inventory)) END AS "Average Days In Inventory"
FROM Vehicle_Type vt
LEFT OUTER JOIN
    (SELECT datediff(sale_date,purchase_date)+1 AS days_in_inventory
         , vin, vehicle_type 
	   FROM Vehicle v
	  WHERE v.sale_date IS NOT NULL) v
  ON vt.type_name = v.vehicle_type
GROUP BY  vt.type_name 
ORDER BY vt.type_name 
;
