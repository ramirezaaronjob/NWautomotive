SELECT 
v.vendor_name AS "Vendor Name" 
,SUM(IFNULL(p.quantity,0)) AS "Parts Supplied" 
,CONCAT('$',FORMAT(ROUND(IFNULL(SUM(p.quantity * p.unit_price),0), 2),2,'en_US')) AS "Parts Cost" 
FROM Vendor v 
LEFT OUTER JOIN Part p 
ON v.vendor_name = p.vendor_name 
GROUP BY v.vendor_name  
ORDER BY ROUND(IFNULL(SUM(p.quantity * p.unit_price),0), 2)  DESC; 