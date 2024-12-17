SELECT v.vin , v.vehicle_type , v.manufacturer , v.model 
    , v.model_year , v.fuel_type, vc.colors  
    , v.horsepower
    , CONCAT('$',FORMAT(ROUND((purchase_price*1.25) + (IFNULL(pp.part_cost,0)*1.1),2),2,'en_US'))  AS sale_price
    , CASE WHEN sale_date IS NOT NULL 
      THEN 'Sold' else 'Unsold' END AS sale_status
    , CASE WHEN pni.vin IS NOT NULL 
        THEN 'Y' ELSE 'N' END AS parts_pending
FROM Vehicle v
 JOIN (SELECT vin, GROUP_CONCAT(color) AS colors FROM Vehicle_Color GROUP BY vin) vc
   ON v.vin = vc.vin
 LEFT OUTER JOIN 
  (SELECT p.vin, SUM(p.quantity*p.unit_price) AS part_cost 
      FROM Part p GROUP BY p.vin) pp
   ON pp.vin = v.vin
 LEFT OUTER JOIN  
  (SELECT DISTINCT pi.vin FROM Part pi WHERE pi.status != 'installed') pni
   ON pni.vin = v.vin
WHERE upper(v.vin) =
      CASE WHEN '$vin' = '' THEN v.vin ELSE UPPER('$vin') END 
  AND CASE WHEN sale_date IS NOT NULL 
            AND UPPER('$sale_status') IN ('SOLD','ALL') 
           THEN 1 
           WHEN sale_date IS NULL
            AND UPPER('$sale_status') IN ('UNSOLD','ALL') 
           THEN 1 
           ELSE 0 END = 1
  AND v.manufacturer =
      CASE WHEN UPPER('$manufacturer') = 'ALL' OR '$manufacturer'= '' 
           THEN v.manufacturer ELSE '$manufacturer' END 
  AND UPPER(v.vehicle_type) =    
      CASE WHEN UPPER('$vehicle_type') = 'ALL' OR '$vehicle_type' = '' 
           THEN v.vehicle_type ELSE '$vehicle_type' END 
  AND v.fuel_type =  
      CASE WHEN upper('$fuel_type') = 'ALL' OR '$fuel_type' = '' 
           THEN v.fuel_type ELSE '$fuel_type' END 
  AND v.model_year = $model_year
  AND vc.colors LIKE  
      CASE WHEN UPPER('$color') = 'ALL' OR '$color' = '' 
           THEN vc.colors ELSE '%$color%' END
  AND (
       UPPER(v.manufacturer) LIKE CASE WHEN '$keyword' != '' 
                 THEN CONCAT('%',UPPER('$keyword'),'%') ELSE '%' END
    OR UPPER(v.model) LIKE CASE WHEN '$keyword' != '' 
                 THEN CONCAT('%',UPPER('$keyword'),'%') ELSE '%' END
    OR UPPER(v.model_year) LIKE CASE WHEN '$keyword' != '' 
                 THEN CONCAT('%',UPPER('$keyword'),'%') ELSE '%' END
    OR UPPER(v.`description`) LIKE CASE WHEN '$keyword' != '' 
                 THEN CONCAT('%',UPPER('$keyword'),'%') ELSE '%' END
  )
ORDER BY v.vin ASC
;