with 
data_from_2021 as (select *, month(timestamp(datetime)) month from hired_employee where year(timestamp(datetime)) = 2021),
month_to_q as (select *, 
               		CASE
    					WHEN month >= 1 and month <= 3 THEN "Q1"
    					WHEN month >= 4 and month <= 6 THEN "Q2"
    					WHEN month >= 7 and month <= 9 THEN "Q3"
               			WHEN month >= 10 and month <= 12 THEN "Q4"
               		END q from data_from_2021)
select * from month_to_q