SELECT replace(position,' ','') as position 
FROM Employee e 
JOIN Employee_type et
  ON e.username = et.username
WHERE e.username = '$Username' 
  AND e.password = '$Password'; 
