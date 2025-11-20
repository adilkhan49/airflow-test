{{ config(materialized='view') }}

with source as (
    select * from {{ source('raw', 'customers') }}
),
renamed as (
    select
        id                as customer_id,
        lower(trim(first_name)) as first_name,
        lower(trim(last_name))  as last_name,
        lower(trim(email))      as email,
        created_at
    from source
)
select * from renamed
