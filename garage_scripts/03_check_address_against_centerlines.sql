select
   concat_ws( ' ', ap.predir, ap.premod, ap.pretype, ap.street, ap.streettype, ap.sufdir) as address_name,
   concat_ws( ' ', rc.predir, rc.premod, rc.pretype,  rc.street, rc.streettype, rc.sufdir) as street_name
from
   ok911.address_point ap
full outer join
   ok911.road_centerline rc on concat_ws( ' ', ap.predir,  ap.pretype,  ap.street, ap.streettype, ap.sufdir) = concat_ws( ' ', rc.predir,  rc.pretype,  rc.street, rc.streettype, rc.sufdir)
   group by street_name, address_name
order by address_name asc;

