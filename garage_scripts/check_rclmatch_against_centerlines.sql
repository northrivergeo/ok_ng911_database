set search_path = 'garage', 'ok911', 'public';

DROP TABLE IF EXISTS check_address_centerlines_tbl;
CREATE TABLE check_address_centerlines_tbl as (
select
   rclmatch as address_rclmatch,
   nguid_rdcl as Centerline
from
   address_points ap
left join
   centerlines rc on rclmatch = address_rclmatch 
   group by rclmatch, nguid_rcl
order by rclmatch desc);

