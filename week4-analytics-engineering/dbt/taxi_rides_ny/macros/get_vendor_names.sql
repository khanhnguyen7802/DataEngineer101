{% macro get_vendor_name(vendor_id) %}
CASE 
    WHEN {{ vendor_id }} = 1 THEN 'Creative Mobile Technologies, LLC'
    WHEN {{ vendor_id }} = 2 THEN 'VeriFone Inc.'
    ELSE 'Unknown Vendor'
END
{% endmacro %}