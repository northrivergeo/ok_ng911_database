--###############################
--#Sync Primary key with nguid
--###############################

alter table ok911.address_point add column tempid integer;
update ok911.address_point set tempid = regexp_substr("nguid_add", '(\d+)')::int
alter table ok911.address_point drop column id;
alter table ok911.address_point rename tempid to id;
alter table ok911.address_point add primary key (id);
create sequence ok911.address_point_idpk_seq;
alter sequence ok911.address_point_idpk_seq owner to <owner>;
alter sequence ok911.address_point_idpk_seq owned by tn911.address_point.ogc_fid;
SELECT setval(pg_get_serial_sequence('ok911.address_point', 'id'), coalesce(max(id),0) + 1, false) FROM ok911.address_point;
alter table ok911.address_point alter column id set default nextval('ok911.address_point_idpk_seq');

--###############################
--#Sync Primary key with nguid
--###############################
alter table tn911.centerlines add column tempid integer;
update tn911.centerlines set tempid  = split_part(oirid, '_', 2)::int;
alter table tn911.centerlines drop column ogc_fid;
alter table tn911.centerlines rename tempid to ogc_fid;
alter table tn911.centerlines add primary key (ogc_fid);
create sequence tn911.centerlines_idpk_seq;
alter sequence tn911.centerlines_idpk_seq owner to <owner>;
alter sequence tn911.centerlines_idpk_seq owned by tn911.centerlines.ogc_fid;
SELECT setval(pg_get_serial_sequence('tn911.centerlines', 'ogc_fid'), coalesce(max(ogc_fid),0) + 1, false) FROM tn911.centerlines;
alter table tn911.centerlines alter column ogc_fid set default nextval('tn911.centerlines_idpk_seq');

