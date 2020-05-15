drop table if exists tb_abt_churn;
create table tb_abt_churn as 

select t2.*,
       t1.flag_churn       

from(

    select t1.dt_ref,
        t1.seller_id,
        min( coalesce(t2.venda, 1) ) as flag_churn

    from tb_book_sellers as t1
    
    left join (
        select 
            strftime( '%Y-%m', t1.order_approved_at) || "-01" as dt_venda,
            t2.seller_id,
            max(0) as venda

        from tb_orders as t1

        left join tb_order_items as t2
        on t1.order_id = t2.order_id

        where order_approved_at is not null
        and seller_id is not null
        and t1.order_status = 'delivered'

        group by strftime( '%Y-%m', t1.order_approved_at) || "-01",
                t2.seller_id
        order by t2.seller_id,
                strftime( '%Y-%m', t1.order_approved_at) || "-01"
    ) as t2
    on t1.seller_id = t2.seller_id
    and t2.dt_venda BETWEEN t1.dt_ref and date(t1.dt_ref, '+2 months')

    group by  t1.dt_ref, t1.seller_id
    order by dt_ref
) as t1

left join tb_book_sellers as t2
on t1.seller_id = t2.seller_id
and t1.dt_ref = t2.dt_ref

order by seller_id

;