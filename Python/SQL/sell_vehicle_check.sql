SELECT v.vin
    , sale_date
	, CASE WHEN pni.vin IS NOT NULL THEN 'Y' ELSE 'N' END AS parts_pending
FROM Vehicle v
 LEFT OUTER JOIN (SELECT p.vin, SUM(p.quantity*p.unit_price) AS part_cost FROM Part p GROUP BY p.vin) pp
   ON pp.vin = v.vin
 LEFT OUTER JOIN (SELECT DISTINCT pi.vin FROM Part pi WHERE pi.status != 'installed') pni
   ON pni.vin = v.vin
WHERE v.vin = '$vin';
