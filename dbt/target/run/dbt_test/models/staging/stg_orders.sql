
  create view "dbt_test"."staging"."stg_orders__dbt_tmp"
    
    
  as (
    

with source as (
    select * from "dbt_test"."raw"."orders"
),
casted as (
    select
        id           as order_id,
        user_id      as customer_id,
        order_date::timestamp as order_timestamp,
        lower(status) as status,
        total_amount::numeric(10,2) as total_amount
    from source
)
select * from casted
  );