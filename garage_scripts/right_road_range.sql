select right1.nguid_rdcl, right1.label, right1.add_r_from::int, right1.add_r_to::int, right2.nguid_rdcl, right2.label, right2.add_r_from::int, right2.add_r_to::int
from (select nguid_rdcl, 
	     label,
             add_r_from::int,
             add_r_to::int 
      from ok911.road_centerline) right1
inner join (select nguid_rdcl, 
	     label,
             add_r_from::int,
             add_r_to::int 
      from ok911.road_centerline) right2
 on right1.label = right2.label
 and right1.nguid_rdcl < right2.nguid_rdcl
where right2.add_r_from::int between right1.add_r_from::int and right1.add_r_to::int
 or right1.add_r_to::int between right2.add_r_from::int and right2.add_r_to::int;
