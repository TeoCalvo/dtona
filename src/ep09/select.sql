select *
from tb_churn_score
where churn = 1
order by score desc