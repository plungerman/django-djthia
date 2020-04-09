SELECT
    TRIM(invl_table.txt) txt
FROM
    invl_table
WHERE
    invl_table.invl MATCHES "S[0-9][0-9][0-9]"
ORDER BY
    TRIM(invl_table.txt)
