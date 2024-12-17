SELECT
   vtc.type_name AS VehicleType
  ,CONCAT('$',FORMAT(ROUND(AVG(CASE vtc.`condition` WHEN 'Excellent' THEN IFNULL(v.purchase_price,0.0) ELSE 0.0 end),2),2,'en_US')) AS "Excellent"
  ,CONCAT('$',FORMAT(ROUND(AVG(CASE vtc.`condition` WHEN 'Very Good' THEN IFNULL(v.purchase_price,0.0) ELSE 0.0 end),2),2,'en_US')) AS "Very Good"
  ,CONCAT('$',FORMAT(ROUND(AVG(CASE vtc.`condition` WHEN 'Good' THEN IFNULL(v.purchase_price,0.0) ELSE 0.0 end),2),2,'en_US')) AS "Good"
  ,CONCAT('$',FORMAT(ROUND(AVG(CASE vtc.`condition` WHEN 'Fair' THEN IFNULL(v.purchase_price,0.0) ELSE 0.0 end),2),2,'en_US')) AS "Fair"
FROM
(SELECT vt.type_name, c.`condition`
  FROM Vehicle_Type vt
  JOIN `Condition` c) vtc
LEFT OUTER JOIN Vehicle v
  ON vtc.type_name = v.vehicle_type
  AND vtc.`condition` = v.`condition`
GROUP BY vtc.type_name
ORDER BY vtc.type_name; 