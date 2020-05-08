select *,
    case when julianday(order_estimated_delivery_date) < julianday(order_delivered_customer_date) then 1 else 0 end as atraso

from tb_orders