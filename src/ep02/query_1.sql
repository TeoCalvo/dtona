select t2.seller_id,
    
    t3.idade_base as idade_base_dias,
    1 + cast(t3.idade_base / 30 as integer) as idade_base_mes,

    count( distinct strftime('%m', t1.order_approved_at) ) as qtde_mes_ativacao,
    cast( count( distinct strftime('%m', t1.order_approved_at) ) as float) / min( 1 + cast( t3.idade_base / 30 as integer), 6 ) as prop_ativacao,

    sum( t2.price ) as receita_total,
    sum( t2.price ) / count( distinct t2.order_id) as avg_vl_venda,
    sum( t2.price ) / min( 1 + cast( t3.idade_base / 30 as integer), 6 ) as avg_vl_venda_mes,
    sum( t2.price ) / count( distinct strftime('%m', t1.order_approved_at) ) as avg_vl_venda_mes_ativado,
    count( distinct t2.order_id) as qtde_vendas,
   
    count( t2.product_id ) as qtde_produto,
    count( distinct t2.product_id ) as qtde_produto_dst,
    sum( t2.price ) / count( t2.product_id ) as avg_vl_produto,

    count( t2.product_id ) / count( distinct t2.order_id) as avg_qtde_produto_venda

from tb_orders as t1

left join tb_order_items as t2
on t1.order_id = t2.order_id

left join(
   select 
        t2.seller_id,
        max(julianday('2017-04-01') - julianday(t1.order_approved_at)) as idade_base

    from tb_orders as t1

    left join tb_order_items as t2
    on t1.order_id = t2.order_id

    where t1.order_approved_at < '2017-04-01'
    and t1.order_status = 'delivered'

    group by t2.seller_id
) as t3
on t2.seller_id = t3.seller_id

where t1.order_approved_at between '2016-10-01'
and '2017-04-01'
and t1.order_status = 'delivered'

group by t2.seller_id;