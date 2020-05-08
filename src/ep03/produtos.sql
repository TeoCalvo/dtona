select product_category_name,
       count(1)

from tb_order_items as t1

left join tb_products as t2
on t1.product_id = t2.product_id

group by product_category_name
order by count(1) desc
