select * from commodities_price_data_analytics
         group by id, metal
         order by id limit 100;


-- Creating price rate view for today
create or replace temporary view commodities_price_today
    as
select metal,
       max(rate_price) as max_rate_price_today,
       min(rate_price) as min_rate_price_today,
       current_date as date_today
from commodities_price_data_analytics
where timestamp >= current_date
or timestamp >= now()::date + interval '1h'
group by metal
order by metal;

select * from commodities_price_today;


-- Creating price rate view for yesterday
create or replace temporary view commodities_price_yesterday
    as
select metal,
       max(rate_price) as max_rate_price_today,
       min(rate_price) as min_rate_price_today,
       current_date as date_yesterday
from commodities_price_data_analytics
where timestamp >= current_date - 1
or timestamp >= (now()::date - 1) + interval '1h'
group by metal
order by metal;

select * from commodities_price_yesterday;


-- Creating price rate view for current week
create or replace temporary view commodities_price_this_week
    as
select metal,
       max(rate_price) as max_rate_price_today,
       min(rate_price) as min_rate_price_today,
       current_date as start_of_current_week
from commodities_price_data_analytics
where timestamp >= date_trunc('week', current_date::date)
group by metal
order by metal;

select * from commodities_price_this_week;


-- Creating price rate view for the last 7 days
create or replace temporary view commodities_price_last_7_days
    as
select metal,
       max(rate_price) as max_rate_price_today,
       min(rate_price) as min_rate_price_today,
       date_trunc('week', current_date - interval '7 days') as beginning_last_7_days
from commodities_price_data_analytics
where timestamp >= current_date::date - interval '7 days'
and timestamp <= current_date
group by metal
order by metal;

SELECT
    commodities_price_data_analytics.metal,
    max_rate_price_today,
    MAX(CASE WHEN rate_price = max_rate_price_today THEN timestamp END) AS date_max_rate_price,
    min_rate_price_today,
    MIN(CASE WHEN rate_price = min_rate_price_today THEN timestamp END) AS date_min_rate_price
FROM
    commodities_price_last_7_days
LEFT JOIN
    commodities_price_data_analytics
    ON commodities_price_last_7_days.metal = commodities_price_data_analytics.metal
WHERE
    timestamp >= CURRENT_DATE::DATE - INTERVAL '7 days'
    AND timestamp <= CURRENT_DATE
GROUP BY
    commodities_price_data_analytics.metal,
    max_rate_price_today,
    min_rate_price_today
ORDER BY
    metal;