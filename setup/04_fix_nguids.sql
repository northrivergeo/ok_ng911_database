--###############################
--#Sync Primary key with nguid_add
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
--#Sync Primary key with nguid_rdcl
--###############################

alter table ok911.road_centerline add column tempid integer;
update ok911.road_centerline set tempid  = split_part(nguid_rdcl, '_', 2)::int;
alter table ok911.road_centerline drop column id;
alter table ok911.road_centerline rename tempid to id;
alter table ok911.road_centerline add primary key (id);
create sequence ok911.road_centerline;
alter sequence ok911.road_centerline_idpk_seq owner to <owner>;
alter sequence ok911.road_centerline_idpk_seq owned by tn911.centerlines.ogc_fid;
SELECT setval(pg_get_serial_sequence('ok911.road_centerline', 'id'), coalesce(max(id),0) + 1, false) FROM ok911.road_centerline;
alter table ok911.road_centerline alter column ogc_fid set default nextval('ok911.road_centerline_idpk_seq');

--###############################
--#Sync Primary key with nguid_psap
--###############################

alter table ok911.psap_boundary add column tempid integer;
update ok911.psap_boundary set tempid = regexp_substr("nguid_psap", '(\d+)')::int
alter table ok911.psap_boundary drop column id;
alter table ok911.psap_boundary rename tempid to id;
alter table ok911.psap_boundary add primary key (id);
create sequence ok911.psap_boundary_idpk_seq;
alter sequence ok911.psap_boundary_idpk_seq owner to <owner>;
alter sequence ok911.psap_boundary_idpk_seq owned by ok911.psap_boundary.id;
SELECT setval(pg_get_serial_sequence('ok911.psap_boundary', 'id'), coalesce(max(id),0) + 1, false) FROM ok911.psap_boundary;
alter table ok911.psap_boundary alter column id set default nextval('ok911.psap_boundary_idpk_seq');

--###############################
--#Sync Primary key with nguid_esz
--###############################

alter table ok911.esz_boundary add column tempid integer;
update ok911.esz_boundary set tempid = regexp_substr("nguid_esz", '(\d+)')::int
alter table ok911.esz_boundary drop column id;
alter table ok911.esz_boundary rename tempid to id;
alter table ok911.esz_boundary add primary key (id);
create sequence ok911.esz_boundary_idpk_seq;
alter sequence ok911.esz_boundary_idpk_seq owner to <owner>;
alter sequence ok911.esz_boundary_idpk_seq owned by ok911.psap_boundary.id;
SELECT setval(pg_get_serial_sequence('ok911.esz_boundary', 'id'), coalesce(max(id),0) + 1, false) FROM ok911.esz_boundary;
alter table ok911.esz_boundary alter column id set default nextval('ok911.esz_boundary_idpk_seq');


--###############################
--#Sync Primary key with nguid_ems
--###############################

alter table ok911.esb_ems_boundary add column tempid integer;
update ok911.esb_ems_boundary set tempid = regexp_substr("nguid_ems", '(\d+)')::int
alter table ok911.esb_ems_boundary drop column id;
alter table ok911.esb_ems_boundary rename tempid to id;
alter table ok911.esb_ems_boundary add primary key (id);
create sequence ok911.esb_ems_boundary_idpk_seq;
alter sequence ok911.esb_ems_boundary_idpk_seq owner to <owner>;
alter sequence ok911.esb_ems_boundary_idpk_seq owned by ok911.esb_ems_boundary.id;
SELECT setval(pg_get_serial_sequence('ok911.esb_ems_boundary', 'id'), coalesce(max(id),0) + 1, false) FROM ok911.esb_ems_boundary;
alter table ok911.esb_ems_boundary alter column id set default nextval('ok911.esb_ems_boundary_idpk_seq');

--###############################
--#Sync Primary key with nguid_fire
--###############################

alter table ok911.esb_fire_boundary add column tempid integer;
update ok911.esb_fire_boundary set tempid = regexp_substr("nguid_fire", '(\d+)')::int
alter table ok911.esb_fire_boundary drop column id;
alter table ok911.esb_fire_boundary rename tempid to id;
alter table ok911.esb_fire_boundary add primary key (id);
create sequence ok911.esb_fire_boundary_idpk_seq;
alter sequence ok911.esb_fire_boundary_idpk_seq owner to <owner>;
alter sequence ok911.esb_fire_boundary_idpk_seq owned by ok911.esb_fire_boundary.id;
SELECT setval(pg_get_serial_sequence('ok911.esb_fire_boundary', 'id'), coalesce(max(id),0) + 1, false) FROM ok911.esb_fire_boundary;
alter table ok911.esb_fire_boundary alter column id set default nextval('ok911.esb_fire_boundary_idpk_seq');


--###############################
--#Sync Primary key with nguid_law
--###############################

alter table ok911.esb_law_boundary add column tempid integer;
update ok911.esb_law_boundary set tempid = regexp_substr("nguid_law", '(\d+)')::int
alter table ok911.esb_law_boundary drop column id;
alter table ok911.esb_law_boundary rename tempid to id;
alter table ok911.esb_law_boundary add primary key (id);
create sequence ok911.esb_law_boundary_idpk_seq;
alter sequence ok911.esb_law_boundary_idpk_seq owner to <owner>;
alter sequence ok911.esb_law_boundary_idpk_seq owned by ok911.esb_law_boundary.id;
SELECT setval(pg_get_serial_sequence('ok911.esb_law_boundary', 'id'), coalesce(max(id),0) + 1, false) FROM ok911.esb_law_boundary;
alter table ok911.esb_law_boundary alter column id set default nextval('ok911.esb_law_boundary_idpk_seq');

--###############################
--#Sync Primary key with nguid_disc
--###############################

alter table ok911.discrepancyagency_boundary add column tempid integer;
update ok911.discrepancyagency_boundary set tempid = regexp_substr("nguid_disc", '(\d+)')::int
alter table ok911.discrepancyagency_boundary drop column id;
alter table ok911.discrepancyagency_boundary rename tempid to id;
alter table ok911.discrepancyagency_boundary add primary key (id);
create sequence ok911.discrepancyagency_boundary_idpk_seq;
alter sequence ok911.discrepancyagency_boundary_idpk_seq owner to <owner>;
alter sequence ok911.discrepancyagency_boundary_idpk_seq owned by ok911.discrepancyagency_boundary.id;
SELECT setval(pg_get_serial_sequence('ok911.discrepancyagency_boundary', 'id'), coalesce(max(id),0) + 1, false) FROM ok911.discrepancyagency_boundary;
alter table ok911.discrepancyagency_boundary alter column id set default nextval('ok911.discrepancyagency_boundary_idpk_seq');




