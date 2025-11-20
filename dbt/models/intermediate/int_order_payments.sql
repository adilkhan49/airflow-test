{{ config(materialized='view') }}

with payments as (
    select
        order_id,
        sum(amount) as total_paid,
        count(*)    as payment_count
    from {{ ref('stg_payments') }}
    group by 1
)

select
    o.order_id,
    o.customer_id,
    o.order_timestamp,
    o.status,
    o.total_amount,
    coalesce(p.total_paid, 0)   as total_paid,
    coalesce(p.payment_count, 0) as payment_count,
    (o.total_amount - coalesce(p.total_paid, 0)) as outstanding_amount
from {{ ref('stg_orders') }} o
left join payments p on o.order_id = p.order_id
