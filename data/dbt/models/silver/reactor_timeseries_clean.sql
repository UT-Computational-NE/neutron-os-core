{{
    config(
        materialized='incremental',
        unique_key='timestamp',
        on_schema_change='append_new_columns'
    )
}}

/*
    Reactor Time-Series Cleaning
    
    Transforms raw CSV data from Bronze tier into clean, typed Silver data.
    
    Transformations:
    - Parse timestamps
    - Standardize column names
    - Handle nulls and missing values
    - Flag outliers (but don't remove - preserve for audit)
    - Calculate derived fields (avg fuel temp)
    
    Source: Bronze serial_data_raw
    Grain: Per-second measurements
*/

with source_data as (
    select * from {{ ref('serial_data_raw') }}
    {% if is_incremental() %}
    where ingested_at > (select max(ingested_at) from {{ this }})
    {% endif %}
),

cleaned as (
    select
        -- Timestamp parsing
        cast(timestamp as timestamp) as timestamp,
        
        -- Power (handle potential nulls/zeros)
        coalesce(cast("LinearPower" as double), 0.0) as linear_power_kw,
        
        -- Temperatures (average the two fuel temp sensors)
        (
            coalesce(cast("FuelTemp1" as double), 0.0) +
            coalesce(cast("FuelTemp2" as double), 0.0)
        ) / 2.0 as fuel_temp_c,
        coalesce(cast("WaterTemp" as double), 0.0) as water_temp_c,
        
        -- Rod positions
        coalesce(cast("Tran" as double), 0.0) as tran_position,
        coalesce(cast("Shim1" as double), 0.0) as shim1_position,
        coalesce(cast("Shim2" as double), 0.0) as shim2_position,
        coalesce(cast("Reg" as double), 0.0) as reg_position,
        
        -- Detector signals (for advanced analysis)
        coalesce(cast("NM" as double), 0.0) as nm_signal,
        coalesce(cast("NPP" as double), 0.0) as npp_signal,
        coalesce(cast("NP" as double), 0.0) as np_signal,
        
        -- Metadata
        source_file,
        ingested_at,
        
        -- Outlier detection (simple bounds check)
        case
            when cast("LinearPower" as double) < 0 then true
            when cast("LinearPower" as double) > {{ var('max_power_kw') }} * 1.1 then true
            when cast("FuelTemp1" as double) > {{ var('max_fuel_temp_c') }} then true
            when cast("FuelTemp2" as double) > {{ var('max_fuel_temp_c') }} then true
            else false
        end as is_outlier
        
    from source_data
    where timestamp is not null
)

select * from cleaned
