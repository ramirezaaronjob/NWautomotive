SELECT
  CONCAT(CASE WHEN i.ssn IS NOT NULL THEN concat(i.first_name, ' ', i.last_name)
       WHEN b.business_tax_id IS NOT NULL THEN  b.business_name END,' (',convert(c.customer_id, char),')') AS "Seller Name"
  , COUNT(DISTINCT(v.vin)) AS "Total Vehicles Sold"
  , CONCAT('$',FORMAT(ROUND(AVG(purchase_price),2),2,'en_US')) AS "Average Purchase Price"
  , ROUND(AVG(coalesce(p.part_count,0)),2) AS "Average Parts Count"
  , CONCAT('$',FORMAT(ROUND(AVG(coalesce(p.parts_cost,0)),2),2,'en_US')) AS "Average Parts Cost"
FROM Vehicle v
JOIN Customer c ON v.seller = c.customer_id
LEFT OUTER JOIN
  (SELECT vin
        , sum(p.quantity) as part_count
        , sum(p.unit_price * p.quantity) as parts_cost
		FROM Part p
     GROUP BY vin) p on v.vin = p.vin
LEFT OUTER JOIN Individual i on c.customer_id = i.customer_id
LEFT OUTER JOIN Business B on c.customer_id = b.customer_id
GROUP BY
  CONCAT(CASE WHEN i.ssn IS NOT NULL THEN concat(i.first_name, ' ', i.last_name)
       WHEN b.business_tax_id IS NOT NULL THEN  b.business_name END,' (',convert(c.customer_id,char),')')
ORDER BY
           count(distinct(v.vin)) DESC,
           AVG(purchase_price) ASC;