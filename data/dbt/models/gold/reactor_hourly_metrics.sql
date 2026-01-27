{{
    config(
        materialized='incremental',
        unique_key='hour',
        on_schema_change='append_new_columns'
    )
}}

/*
    Reactor Hourly Metrics
    
    Aggregates per-second reactor time-series data into hourly metrics
    for the Reactor Performance Analytics dashboard.
    
    Source: Silver layer reactor_timeseries_clean
    Grain: One row per hour
    Refresh: Hourly incremental
*/

with source_data as (
    select
        date_trunc('hour', timestamp) as hour,
        linear_power_kw,
        fuel_temp_c,
        water_temp_c
    from {{ ref('reactor_timeseries_clean') }}
    {% if is_incremental() %}
    where timestamp > (select max(hour) from {{ this }})
    {% endif %}
),

aggregated as (
    select
        hour,
        avg(linear_power_kw) as avg_power_kw,
        max(linear_power_kw) as max_power_kw,
        min(linear_power_kw) as min_power_kw,
        avg(fuel_temp_c) as avg_fuel_temp_c,
        max(fuel_temp_c) as max_fuel_temp_c,
        avg(water_temp_c) as avg_water_temp_c,
        -- Energy = Power * Time, integrated over hour
        sum(linear_power_kw) / 3600.0 as energy_kwh,  -- Assuming per-second samples
        count(*) as sample_count,
        case
            when count(*) >= 3600 * 0.95 then 'GOOD'
            when count(*) >= 3600 * 0.50 then 'PARTIAL'
            when count(*) > 0 then 'INTERPOLATED'
            else 'MISSING'
        end as data_quality_flag
    from source_data
    group by hour
)

select * from aggregated
