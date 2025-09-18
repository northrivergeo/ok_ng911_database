set search_path = 'garage', 'ok911', 'public';

DROP TABLE IF EXISTS check_address_centerlines_tbl;
CREATE TABLE check_address_centerlines_tbl as (
select
   concat_ws( ' ', ap.predir, ap.premod, ap.pretype, ap.street, ap.streettype, ap.sufdir,  ap.postmod) as address_name,
   concat_ws( ' ', rc.predir, rc.premod, rc.pretype,  rc.street, rc.streettype, rc.sufdir,  rc.postmod) as street_name
from
   address_points ap
left join
   centerlines rc on concat_ws( ' ', ap.predir,  ap.pretype,  ap.street, ap.streettype, ap.sufdir,  ap.postmod) = concat_ws( ' ', rc.predir,  rc.pretype,  rc.street, rc.streettype, rc.sufdir,  rc.postmod)
   group by street_name, address_name
order by address_name desc);

