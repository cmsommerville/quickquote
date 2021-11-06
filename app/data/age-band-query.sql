select 
	ab.plan_id, br.family_code, br.smoker_status, ab.lower_age, ab.upper_age, 
	round(sum(br.benefit_rate_final_premium * aw.weight) / sum(aw.weight), 5) as premium
from benefit_rates as br
left join age_bands as ab on 
	br.plan_id = ab.plan_id and 
	br.age between ab.lower_age and ab.upper_age
left join age_weights as aw on 
	br.age = aw.age
where 
	br.plan_id = 2
group by ab.plan_id, br.family_code, br.smoker_status, ab.lower_age, ab.upper_age
order by ab.plan_id, br.family_code, br.smoker_status, ab.lower_age, ab.upper_age
;

