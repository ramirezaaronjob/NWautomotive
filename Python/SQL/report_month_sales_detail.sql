SELECT
 CONCAT(e.first_name,' ',e.last_name) AS "Salesperson"
,DATE_FORMAT(v.sale_date,'%Y%m') AS "Year/Month"
,COUNT(1) AS "Vehicles Sold"
,CONCAT('$',FORMAT(ROUND(SUM(ROUND((purchase_price*1.25) + (IFNULL(pp.part_cost,0)*1.1),2) ),2),2,'en_US')) AS "Gross Income"
,CONCAT('$',FORMAT(ROUND(SUM((ROUND((purchase_price*1.25) + (IFNULL(pp.part_cost,0)*1.1),2))-v.purchase_price-IFNULL(pp.part_cost,0)),2),2,'en_US')) AS "Net Income"
FROM Vehicle v
JOIN Employee e 
  ON v.salesperson = e.username
 LEFT OUTER JOIN (SELECT p.vin, SUM(p.quantity*p.unit_price) AS part_cost FROM Part p GROUP BY p.vin) pp
   ON pp.vin = v.vin
where v.sale_date is not null
  and date_format(v.sale_date,'%Y%m') = '$yearmonth'
GROUP BY
  CONCAT(e.first_name,' ',e.last_name)
 ,DATE_FORMAT(v.sale_date,'%Y%m')
ORDER BY COUNT(1) DESC,
         SUM((ROUND((purchase_price*1.25) + (IFNULL(pp.part_cost,0)*1.1),2))-v.purchase_price-IFNULL(pp.part_cost,0))  DESC;	

