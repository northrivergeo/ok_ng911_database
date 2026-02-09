select left1.nguid_rdcl, left1.label, left1.add_l_from::int, left1.add_l_to::int, left2.nguid_rdcl, left2.label, left2.add_l_from::int, left2.add_l_to::int
from (select nguid_rdcl, 
	     label,
             add_l_from::int,
             add_l_to::int 
      from ok911.road_centerline) left1
inner join (select nguid_rdcl, 
	     label,
             add_l_from::int,
             add_l_to::int 
      from ok911.road_centerline) left2
 on left1.label = left2.label
 and left1.nguid_rdcl < left2.nguid_rdcl
where left2.add_l_from::int between left1.add_l_from::int and left1.add_l_to::int
 or left1.add_l_to::int between left2.add_l_from::int and left2.add_l_to::int;
