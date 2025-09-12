--updae psap discrpagid
update 
  marlow.address_point ap
    set discrpagid=e.discrpagid
    from marlow.esb_psap_boundary e
  where st_dwithin(ap.geom, e.geom,0);


--update zip
update marlow.address_point set zipcode = "ZIP"; 

--update road type
update marlow.address_point set streettype = 'ALLEY' where street_typ = 'ALY';
update marlow.address_point set streettype = 'AVENUE' where street_typ = 'AVE';
update marlow.address_point set streettype = 'BOULEVARD' where street_typ = 'BLVD';
update marlow.address_point set streettype = 'BRANCH' where street_typ = 'BR';
update marlow.address_point set streettype = 'CIRCLE' where street_typ = 'CIR';
update marlow.address_point set streettype = 'COURT' where street_typ = 'CT';
update marlow.address_point set streettype = 'DRIVE' where street_typ = 'DR';
update marlow.address_point set streettype = 'ESTATE' where street_typ = 'EST';
update marlow.address_point set streettype = 'ESTATES' where street_typ = 'ESTS';
update marlow.address_point set streettype = 'HIGHWAY' where street_typ = 'HWY';
update marlow.address_point set streettype = 'LANE' where street_typ = 'LN';
update marlow.address_point set streettype = 'LOOP' where street_typ = 'LOOP';
update marlow.address_point set streettype = 'PASS' where street_typ = 'PASS';
update marlow.address_point set streettype = 'PLACE' where street_typ = 'PL';
update marlow.address_point set streettype = 'ROAD' where street_typ = 'RD';
update marlow.address_point set streettype = 'RUN' where street_typ = 'RUN';
update marlow.address_point set streettype = 'ROAD' where street_typ = 'Raod';
update marlow.address_point set streettype = 'ROAD' where street_typ = 'Road';
update marlow.address_point set streettype = 'STREET' where street_typ = 'ST';
update marlow.address_point set streettype = 'TERRACE' where street_typ = 'TER';
update marlow.address_point set streettype = 'TRAIL' where street_typ = 'TRL';
update marlow.address_point set streettype = 'WAY' where street_type = 'WAY';


--update lgcytype 
update marlow.address_point set lgcytype = 'ALY' where street_typ = 'ALY';
update marlow.address_point set lgcytype = 'AVE' where street_typ = 'AVE';
update marlow.address_point set lgcytype = 'BLVD' where street_typ = 'BLVD';
update marlow.address_point set lgcytype = 'BR' where street_typ = 'BR';
update marlow.address_point set lgcytype = 'CIR' where street_typ = 'CIR';
update marlow.address_point set lgcytype = 'CT' where street_typ = 'CT';
update marlow.address_point set lgcytype = 'DR' where street_typ = 'DR';
update marlow.address_point set lgcytype = 'EST' where street_typ = 'EST';
update marlow.address_point set lgcytype = 'ESTS' where street_typ = 'ESTS';
update marlow.address_point set lgcytype = 'HWY' where street_typ = 'HWY';
update marlow.address_point set lgcytype = 'LN' where street_typ = 'LN';
update marlow.address_point set lgcytype = 'LOOP' where street_typ = 'LOOP';
update marlow.address_point set lgcytype = 'PASS' where street_typ = 'PASS';
update marlow.address_point set lgcytype = 'PL' where street_typ = 'PL';
update marlow.address_point set lgcytype = 'RD' where street_typ = 'RD';
update marlow.address_point set lgcytype = 'RUN' where street_typ = 'RUN';
update marlow.address_point set lgcytype = 'RD' where street_typ = 'Raod';
update marlow.address_point set lgcytype = 'RD' where street_typ = 'Road';
update marlow.address_point set lgcytype = 'ST' where street_typ = 'ST';
update marlow.address_point set lgcytype = 'TER' where street_typ = 'TER';
update marlow.address_point set lgcytype = 'TRL' where street_typ = 'TRL';
update marlow.address_point set lgcytype = 'WAY' where street_type = 'WAY';

--update predir 
update marlow.address_point set predir = 'EAST' where pre_dir = 'E';
update marlow.address_point set predir = 'NORTH' where pre_dir = 'N';
update marlow.address_point set predir = 'NORTHEAST' where pre_dir = 'NE';
update marlow.address_point set predir = 'SOUTH' where pre_dir = 'S';
update marlow.address_point set predir = 'SOUTHWEST' where pre_dir = 'SW';
update marlow.address_point set predir = 'WEST' where pre_dir = 'W';

update pontotoc.address_point set predir = 'EAST' where name_road ILIKE 'E %'; 
update pontotoc.address_point set predir = 'WEST' where name_road ILIKE 'W %'; 
update pontotoc.address_point set predir = 'SOUTH' where name_road ILIKE 'S %'; 
update pontotoc.address_point set predir = 'NORTH' where name_road ILIKE 'N %'; 

--update lgcypredir 
update marlow.address_point set lgcypredir = 'E' where pre_dir = 'E';
update marlow.address_point set lgcypredir = 'N' where pre_dir = 'N';
update marlow.address_point set lgcypredir = 'NE' where pre_dir = 'NE';
update marlow.address_point set lgcypredir = 'S' where pre_dir = 'S';
update marlow.address_point set lgcypredir = 'SW' where pre_dir = 'SW';
update marlow.address_point set lgcypredir = 'W' where pre_dir = 'W';

update pontotoc.address_point set lgcypredir = 'E' where name_road ILIKE 'E %'; 
update pontotoc.address_point set lgcypredir = 'W' where name_road ILIKE 'W %'; 
update pontotoc.address_point set lgcypredir = 'S' where name_road ILIKE 'S %'; 
update pontotoc.address_point set lgcypredir = 'N' where name_road ILIKE 'N %'; 
