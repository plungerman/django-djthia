SELECT
    TRIM(IT.invl) AS code,
    TRIM(IT.txt) AS name,
    INR.id AS id,
    INR.beg_date,
    INR.end_date
FROM
    invl_table IT
INNER JOIN
    involve_rec INR
ON
    TRIM(IT.invl) = TRIM(INR.invl)
WHERE
    invl_table.invl MATCHES "S[0-9][0-9][0-9]"
AND
    INR.id =
