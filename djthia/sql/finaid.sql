-- FALNDLEI is stored in the field resrc.
-- E is stored in the field called stat.
-- For the current academic year ( 1920 ) , the filter value should be FY19 .

-- The filter value is always FYnn , where nn is the first two digits of the
-- academic year.

SELECT
    *
FROM
    ctc_rec
wHERE
    resrc = 'FALNDLEI'
AND
    stat='E'
AND
    tick='FY{{year}}'
