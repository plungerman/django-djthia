SELECT
    Program_Enrollment_Record.id,
    ID_Record.fullname,
    Program_Enrollment_Record.plan_grad_yr,
    Program_Enrollment_Record.plan_grad_sess,
    Program_Enrollment_Record.plan_grad_grp,
    Program_Enrollment_Record.prog,
    Program_Enrollment_Record.deg_app_date,
    Program_Enrollment_Record.subprog,
    Program_Enrollment_Record.acst,
    TRIM(
        CASE
            WHEN TRIM(Program_Enrollment_Record.deg) IN ("BA","BS")
            THEN major1.txt
            ELSE conc1.txt
        END
    ) AS major1,
    TRIM(
        CASE
            WHEN TRIM(Program_Enrollment_Record.deg) IN ("BA","BS")
            THEN major2.txt
            ELSE conc2.txt
        END
    ) AS major2,
    TRIM(
        CASE
            WHEN TRIM(Program_Enrollment_Record.deg) IN ("BA","BS")
            THEN major3.txt
            ELSE ""
        END
    ) AS major3,
    TRIM(
        CASE
            WHEN TRIM(Program_Enrollment_Record.deg) IN ("BA","BS")
            THEN minor1.txt
            ELSE conc1.txt
        END
    ) AS minor1,
    TRIM(
        CASE
            WHEN TRIM(Program_Enrollment_Record.deg) IN ("BA","BS")
            THEN minor2.txt
            ELSE conc2.txt
        END
    ) AS minor2,
    TRIM(
        CASE
            WHEN TRIM(Program_Enrollment_Record.deg) IN ("BA","BS")
            THEN minor3.txt
            ELSE ""
        END
    ) AS minor3,
    Program_Enrollment_Record.conc1,
    T9.txt,
    Program_Enrollment_Record.conc2,
    T10.txt,
    Program_Enrollment_Record.deg_grant_date,
    Student_Status_Record.cum_att_hrs,
    Student_Status_Record.cum_earn_hrs,
    Student_Status_Record.cum_gpa,
    ID_Record.addr_line1,
    ID_Record.addr_line2,
    CASE
        WHEN
            ID_Record.addr_line2 not like ' %'
        THEN
            TRIM(both FROM ID_Record.city)
            || ', ' || ID_Record.st || '  ' || ID_Record.zip
        ELSE
            ''
    END AS city_st_zip,
    ID_Record.city,
    ID_Record.st,
    ID_Record.zip,
    ID_Record.phone,
    Program_Enrollment_Record.adm_yr,
    Program_Enrollment_Record.adm_sess,
    Program_Enrollment_Record.cohort_yr,
    Program_Enrollment_Record.cohort_ctgry,
    Program_Enrollment_Record.date_compl,
    Student_Status_Record.cum_qual_hrs,
    Profile_Record.priv_code,
    ID_Record.middlename,
    ID_Record.firstname,
    ID_Record.lastname,
    Profile_Record.birth_date
FROM (
    (
        (
            (
                id_rec ID_Record
                INNER JOIN
                    profile_rec Profile_Record
                ON
                    ID_Record.id=Profile_Record.id
            )
            INNER JOIN
                prog_enr_rec Program_Enrollment_Record
            ON
                Program_Enrollment_Record.id=ID_Record.id
        )
        INNER JOIN
            stu_stat_rec Student_Status_Record
        ON
            Program_Enrollment_Record.id=Student_Status_Record.id
        AND
            Program_Enrollment_Record.prog=Student_Status_Record.prog
        AND
            Program_Enrollment_Record.site=Student_Status_Record.site
    )
    LEFT OUTER JOIN
        conc_table T9
    ON
        Program_Enrollment_Record.conc1 = T9.conc
)
LEFT JOIN
    major_table major1  ON  Program_Enrollment_Record.major1 = major1.major
LEFT JOIN
    major_table major2  ON  Program_Enrollment_Record.major2 = major2.major
LEFT JOIN
    major_table major3  ON  Program_Enrollment_Record.major3 = major3.major
LEFT JOIN
    minor_table minor1  ON  Program_Enrollment_Record.minor1 = minor1.minor
LEFT JOIN
    minor_table minor2  ON  Program_Enrollment_Record.minor2 = minor2.minor
LEFT JOIN
    minor_table minor3  ON  Program_Enrollment_Record.minor3 = minor3.minor
LEFT JOIN
    conc_table conc1    ON  Program_Enrollment_Record.conc1  = conc1.conc
LEFT JOIN
    conc_table conc2    ON  Program_Enrollment_Record.conc2  = conc2.conc
LEFT JOIN
    conc_table conc3    ON  Program_Enrollment_Record.conc3  = conc3.conc
LEFT OUTER JOIN
    conc_table T10
ON
    Program_Enrollment_Record.conc2=T10.conc
WHERE (
    (
        Program_Enrollment_Record.plan_grad_yr = '{{last_year}}'
    AND
        Program_Enrollment_Record.plan_grad_sess IN ('RA ', 'GA ', 'AA ', 'AB', 'GE')
    )
    OR
    (
        Program_Enrollment_Record.plan_grad_yr = '{{curr_year}}'
    AND
        Program_Enrollment_Record.plan_grad_sess IN (
            'RB ', 'RC ', 'RD', 'RE ', 'GB', 'GC ', 'GE ', 'AK ', 'AM ', 'AG ', 'AS ', 'AT'
        )
    )
    OR
    (
        Program_Enrollment_Record.plan_grad_yr = '{{next_year}}'
    AND
        Program_Enrollment_Record.plan_grad_sess IN ('RB', 'RC')
    )
)
AND
    Program_Enrollment_Record.prog IN ('UNDG', 'GRAD')
AND
    Program_Enrollment_Record.cl NOT IN (
        'AT', 'KU', 'NM', 'PA', 'PB', 'PC', 'PG', 'PR', 'UP', 'YO'
    )
