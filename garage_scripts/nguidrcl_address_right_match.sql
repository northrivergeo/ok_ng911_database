 select
     address_point.address, 
     address_point.nguid_add,
     address_point.ap_name,
     centerline.rcl_name,
     centerline.nguid_rdcl,
     centerline.parity_l, 
     centerline.parity_r,
     centerline.add_r_from::int,
     centerline.add_r_to::int
from (
     select
        address,
	nguid_add,
        concat_ws( ' ', ap.predir, ap.pretype, ap.street, ap.streettype, ap.sufdir) as ap_name
from
     ok911.address_point as ap) as address_point
inner join (
     select
        add_r_from::int,
        add_r_to::int,
        nguid_rdcl,
	parity_l, 
	parity_r,
        concat_ws( ' ', rc.predir, rc.pretype, rc.street, rc.streettype, rc.sufdir) as rcl_name
from
     ok911.road_centerline as rc) as centerline
     on address_point.ap_name = centerline.rcl_name
     where address_point.address between centerline.add_r_from::int and centerline.add_r_to::int;
