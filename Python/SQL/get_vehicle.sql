SELECT v.vin
    , v.purchaser
    , concat(epur.first_name, ' ', epur.last_name) AS purchaser_name
    , v.salesperson
    , CASE WHEN v.salesperson IS NOT NULL THEN CONCAT(esales.first_name, ' ', esales.last_name) ELSE '' END AS salesperson_name
    , v.seller
    , CASE WHEN isell.ssn IS NOT NULL THEN 'Individual' WHEN bsell.business_tax_id THEN 'Business' ELSE 'Error' END AS seller_type
    , v.buyer
    , CASE WHEN ibuy.ssn IS NOT NULL THEN 'Individual' WHEN bbuy.business_tax_id THEN 'Business' ELSE 'N/A' END AS buyer_type
    , vehicle_type, manufacturer, model,  model_year, fuel_type, horsepower
    , vc.colors  
    , purchase_date
    , CONCAT('$',FORMAT(purchase_price,2,'en_US')) as purchase_price
    , sale_date
    , CONCAT('$',FORMAT(ROUND(((purchase_price*1.25) + (IFNULL(pp.part_cost,0) *1.1) ),2),2,'en_US'))  AS sale_price
	, CONCAT('$',FORMAT(ROUND(part_cost,2),2,'en_US')) as part_cost
	, CASE WHEN pni.vin IS NOT NULL THEN 'Y' ELSE 'N' END AS parts_pending,
    `condition`, `description`
FROM Vehicle v
 JOIN (SELECT vin, GROUP_CONCAT(color) AS colors FROM Vehicle_Color GROUP BY vin) vc
   ON v.vin = vc.vin
 JOIN Employee epur ON v.purchaser = epur.username
 LEFT OUTER JOIN Employee esales ON v.salesperson = esales.username
 JOIN Customer csell ON v.seller = csell.customer_id
 LEFT OUTER JOIN Individual isell ON csell.customer_id = isell.customer_id
 LEFT OUTER JOIN Business bsell ON csell.customer_id = bsell.customer_id
 LEFT OUTER JOIN Customer cbuy ON v.buyer = cbuy.customer_id
 LEFT OUTER JOIN Individual ibuy ON cbuy.customer_id = ibuy.customer_id
 LEFT OUTER JOIN Business bbuy ON cbuy.customer_id = bbuy.customer_id
 LEFT OUTER JOIN (SELECT p.vin, SUM(p.quantity*p.unit_price) AS part_cost FROM Part p GROUP BY p.vin) pp
   ON pp.vin = v.vin
 LEFT OUTER JOIN (SELECT DISTINCT pi.vin FROM Part pi WHERE pi.status != 'installed') pni
   ON pni.vin = v.vin
WHERE v.vin = '$vin'; 
