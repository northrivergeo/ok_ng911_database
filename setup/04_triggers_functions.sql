--=================================================================================================
--address point
--=================================================================================================

--address_point
--update discrpagid

 CREATE OR REPLACE FUNCTION ok911.address_func_discrpagid()
 RETURNS TRIGGER AS $$
 BEGIN
    NEW.discrpagid := (select discrpagid from ok911.psap_boundary where st_within(new.geom, geom));
    RETURN NEW;
 END;
 $$
LANGUAGE PLPGSQL;

 CREATE TRIGGER update_address_discrpagid
 BEFORE insert or update
     ON ok911.address_point FOR EACH ROW
     EXECUTE PROCEDURE
     ok911.address_func_discrpagid();

--address_point
--Revdate and reveditor 

CREATE OR REPLACE FUNCTION ok911.address_func_date()
RETURNS TRIGGER AS $$
BEGIN
   NEW.reveditor = current_user;
   NEW.revdate = current_timestamp;
   NEW.effectdate = current_timestamp;
   NEW.expiredate = current_timestamp + interval '10 years';
   RETURN NEW;
END;
$$
LANGUAGE PLPGSQL;

CREATE TRIGGER update_address_date BEFORE INSERT OR UPDATE
    ON ok911.address_point FOR EACH ROW EXECUTE PROCEDURE
    ok911.address_func_date();


--address_point
--updating agency_id 
 CREATE OR REPLACE FUNCTION ok911.address_func_agency_id()
 RETURNS TRIGGER AS $$
 BEGIN
    NEW.agency_id := (select agency_id from ok911.psap_boundary where st_within(new.geom, geom));
    RETURN NEW;
 END;
 $$
LANGUAGE PLPGSQL;

CREATE TRIGGER update_address_agency_id BEFORE insert or update
     ON ok911.address_point FOR EACH ROW
     EXECUTE PROCEDURE
     ok911.address_func_agency_id();

--address_point
--lat and long 
CREATE OR REPLACE FUNCTION ok911.address_func_location()
RETURNS TRIGGER AS $$
BEGIN
   NEW.longitude := st_x(NEW.geom);
   NEW.latitude := st_y(NEW.geom);
   RETURN NEW;
END;
$$
LANGUAGE PLPGSQL;

CREATE TRIGGER update_address_location BEFORE insert or update
    ON ok911.address_point FOR EACH ROW EXECUTE PROCEDURE
    ok911.address_func_location();

--Set the Nguid 
CREATE OR REPLACE FUNCTION ok911.address_func_nguid()
RETURNS TRIGGER AS $$
BEGIN
   NEW.nguid_add = 'ADDRESS_POINT_'||new.id||'@'||new.agency_id;
   RETURN NEW;
END;
$$
LANGUAGE PLPGSQL;

CREATE TRIGGER update_address_oirid BEFORE INSERT
    ON ok911.address_point FOR EACH ROW EXECUTE PROCEDURE
    ok911.address_func_nguid();

CREATE OR REPLACE FUNCTION ok911.address_func_label()
RETURNS TRIGGER AS $$
BEGIN
   NEW.label := initcap(concat_ws( ' ', new.addpre, new.address, new.addsuf, new.predir, new.pretype, new.pretypesep, new.street, new.streettype, new.sufdir, new.sufmod));  
   RETURN NEW;
END;
$$
LANGUAGE PLPGSQL;

CREATE TRIGGER update_address_label BEFORE insert or update
    ON ok911.address_point FOR EACH ROW EXECUTE PROCEDURE
    ok911.address_func_label();



--=================================================================================================
--centerline
--=================================================================================================
CREATE OR REPLACE FUNCTION ok911.cent_func_date()
RETURNS TRIGGER AS $$
BEGIN
   NEW.reveditor = current_user;
   NEW.revdate = current_timestamp;
   NEW.effectdate = current_timestamp;
   NEW.expiredate = current_timestamp + interval '10 years';
   RETURN NEW;
END;
$$
LANGUAGE PLPGSQL;

CREATE TRIGGER update_cent_oirid BEFORE INSERT OR UPDATE
    ON ok911.road_centerline FOR EACH ROW EXECUTE PROCEDURE
    ok911.cent_func_date();


CREATE OR REPLACE FUNCTION ok911.cent_func_roadlength()
RETURNS TRIGGER AS $$
BEGIN
   NEW.roadlength = st_length(st_transform(new.geom, 3640));
   RETURN NEW;
END;
$$
LANGUAGE PLPGSQL;

CREATE TRIGGER update_roadlength BEFORE INSERT OR UPDATE
    ON ok911.road_centerline FOR EACH ROW EXECUTE PROCEDURE
    ok911.cent_func_roadlength();

--Set the Nguid 
CREATE OR REPLACE FUNCTION ok911.centerline_func_nguid()
RETURNS TRIGGER AS $$
BEGIN
   NEW.nguid_rdcl = 'ROAD_CENTERLINE_'||new.id||'@'||new.agency_id;
   RETURN NEW;
END;
$$
LANGUAGE PLPGSQL;

CREATE TRIGGER update_centerline_nguid BEFORE INSERT
    ON ok911.road_centerline FOR EACH ROW EXECUTE PROCEDURE
    ok911.centerline_func_nguid();



--=================================================================================================
--psap_boundary
--=================================================================================================
CREATE OR REPLACE FUNCTION ok911.psap_func_nguid()
RETURNS TRIGGER AS $$
BEGIN
   NEW.nguid_psap = 'PSAP_'||new.agency||'_'||new.id||'@'||new.agency_id;
   RETURN NEW;
END;
$$
LANGUAGE PLPGSQL;

CREATE TRIGGER update_psap_nguid BEFORE INSERT
    ON ok911.psap_boundary FOR EACH ROW EXECUTE PROCEDURE
    ok911.psap_func_nguid();


CREATE OR REPLACE FUNCTION ok911.psap_func_date()
RETURNS TRIGGER AS $$
BEGIN
   NEW.reveditor = current_user;
   NEW.revdate = current_timestamp;
   NEW.effectdate = current_timestamp;
   NEW.expiredate = current_timestamp + interval '10 years';
   RETURN NEW;
END;
$$
LANGUAGE PLPGSQL;

CREATE TRIGGER update_psap_date BEFORE INSERT OR UPDATE
    ON ok911.psap_boundary FOR EACH ROW EXECUTE PROCEDURE
    ok911.psap_func_date();


CREATE OR REPLACE FUNCTION ok911.psap_func_initidate()
RETURNS TRIGGER AS $$
BEGIN
   NEW.initidate = current_timestamp;
   RETURN NEW;
END;
$$
LANGUAGE PLPGSQL;

CREATE TRIGGER update_psap_initidate BEFORE INSERT 
    ON ok911.psap_boundary FOR EACH ROW EXECUTE PROCEDURE
    ok911.psap_func_initidate();


--=================================================================================================
--esb_law
--=================================================================================================
CREATE OR REPLACE FUNCTION ok911.law_func_nguid()
RETURNS TRIGGER AS $$
BEGIN
   NEW.nguid_law = 'ESB_LAW_'||new.agency||'_'||new.id||'@'||new.agency_id;
   RETURN NEW;
END;
$$
LANGUAGE PLPGSQL;

CREATE TRIGGER update_law_nguid BEFORE INSERT 
    ON ok911.esb_law_boundary FOR EACH ROW EXECUTE PROCEDURE
    ok911.law_func_nguid();


CREATE OR REPLACE FUNCTION ok911.law_func_date()
RETURNS TRIGGER AS $$
BEGIN
   NEW.reveditor = current_user;
   NEW.revdate = current_timestamp;
   NEW.effectdate = current_timestamp;
   NEW.expiredate = current_timestamp + interval '10 years';
   RETURN NEW;
END;
$$
LANGUAGE PLPGSQL;

CREATE TRIGGER update_law_date BEFORE INSERT OR UPDATE
    ON ok911.esb_law_boundary FOR EACH ROW EXECUTE PROCEDURE
    ok911.law_func_date();


CREATE OR REPLACE FUNCTION ok911.law_func_initidate()
RETURNS TRIGGER AS $$
BEGIN
   NEW.initidate = current_timestamp;
   RETURN NEW;
END;
$$
LANGUAGE PLPGSQL;

CREATE TRIGGER update_law_initidate BEFORE INSERT 
    ON ok911.esb_law_boundary FOR EACH ROW EXECUTE PROCEDURE
    ok911.law_func_initidate();


--=================================================================================================
--esb_fire
--=================================================================================================
CREATE OR REPLACE FUNCTION ok911.fire_func_nguid()
RETURNS TRIGGER AS $$
BEGIN
   NEW.nguid_fire = 'ESB_FIRE_'||new.agency||'_'||new.id||'@'||new.agency_id;
   RETURN NEW;
END;
$$
LANGUAGE PLPGSQL;

CREATE TRIGGER update_fire_nguid BEFORE INSERT
    ON ok911.esb_fire_boundary FOR EACH ROW EXECUTE PROCEDURE
    ok911.fire_func_nguid();


CREATE OR REPLACE FUNCTION ok911.fire_func_date()
RETURNS TRIGGER AS $$
BEGIN
   NEW.reveditor = current_user;
   NEW.revdate = current_timestamp;
   NEW.effectdate = current_timestamp;
   NEW.expiredate = current_timestamp + interval '10 years';
   RETURN NEW;
END;
$$
LANGUAGE PLPGSQL;

CREATE TRIGGER update_law_date BEFORE INSERT OR UPDATE
    ON ok911.esb_fire_boundary FOR EACH ROW EXECUTE PROCEDURE
    ok911.fire_func_date();


CREATE OR REPLACE FUNCTION ok911.fire_func_initidate()
RETURNS TRIGGER AS $$
BEGIN
   NEW.initidate = current_timestamp;
   RETURN NEW;
END;
$$
LANGUAGE PLPGSQL;

CREATE TRIGGER update_fire_initidate BEFORE INSERT 
    ON ok911.esb_fire_boundary FOR EACH ROW EXECUTE PROCEDURE
    ok911.fire_func_initidate();

--=================================================================================================
--esb_ems
--=================================================================================================
CREATE OR REPLACE FUNCTION ok911.ems_func_nguid()
RETURNS TRIGGER AS $$
BEGIN
   NEW.nguid_ems = 'ESB_EMS_'||new.agency||'_'||new.id||'@'||new.agency_id;
   RETURN NEW;
END;
$$
LANGUAGE PLPGSQL;

CREATE TRIGGER update_ems_nguid BEFORE INSERT
    ON ok911.esb_ems_boundary FOR EACH ROW EXECUTE PROCEDURE
    ok911.ems_func_nguid();


CREATE OR REPLACE FUNCTION ok911.ems_func_date()
RETURNS TRIGGER AS $$
BEGIN
   NEW.reveditor = current_user;
   NEW.revdate = current_timestamp;
   NEW.effectdate = current_timestamp;
   NEW.expiredate = current_timestamp + interval '10 years';
   RETURN NEW;
END;
$$
LANGUAGE PLPGSQL;

CREATE TRIGGER update_ems_date BEFORE INSERT OR UPDATE
    ON ok911.esb_ems_boundary FOR EACH ROW EXECUTE PROCEDURE
    ok911.ems_func_date();


CREATE OR REPLACE FUNCTION ok911.ems_func_initidate()
RETURNS TRIGGER AS $$
BEGIN
   NEW.initidate = current_timestamp;
   RETURN NEW;
END;
$$
LANGUAGE PLPGSQL;

CREATE TRIGGER update_ems_initidate BEFORE INSERT 
    ON ok911.esb_ems_boundary FOR EACH ROW EXECUTE PROCEDURE
    ok911.ems_func_initidate();

--=================================================================================================
--esn
--=================================================================================================
CREATE OR REPLACE FUNCTION ok911.esn_func_nguid()
RETURNS TRIGGER AS $$
BEGIN
   NEW.nguid_esz = 'ESN_'||new.agency||'_'||new.id||'@'||new.agency_id;
   RETURN NEW;
END;
$$
LANGUAGE PLPGSQL;

CREATE TRIGGER update_esn_nguid BEFORE INSERT
    ON ok911.esz_boundary FOR EACH ROW EXECUTE PROCEDURE
    ok911.esn_func_nguid();

CREATE OR REPLACE FUNCTION ok911.esn_func_date()
RETURNS TRIGGER AS $$
BEGIN
   NEW.reveditor = current_user;
   NEW.revdate = current_timestamp;
   NEW.effectdate = current_timestamp;
   NEW.expiredate = current_timestamp + interval '10 years';
   RETURN NEW;
END;
$$
LANGUAGE PLPGSQL;

CREATE TRIGGER update_esn_date BEFORE INSERT OR UPDATE
    ON ok911.esz_boundary FOR EACH ROW EXECUTE PROCEDURE
    ok911.esn_func_date();


CREATE OR REPLACE FUNCTION ok911.esn_func_initidate()
RETURNS TRIGGER AS $$
BEGIN
   NEW.initidate = current_timestamp;
   RETURN NEW;
END;
$$
LANGUAGE PLPGSQL;

CREATE TRIGGER update_esn_initidate BEFORE INSERT 
    ON ok911.esz_boundary FOR EACH ROW EXECUTE PROCEDURE
    ok911.esn_func_initidate();

--=================================================================================================
--municipal_boundary
--=================================================================================================
CREATE OR REPLACE FUNCTION ok911.muni_func_nguid()
RETURNS TRIGGER AS $$
BEGIN
   NEW.nguid_muni = 'ESB_EMS_'||new.agency||'_'||new.id||'@'||new.agency_id;
   RETURN NEW;
END;
$$
LANGUAGE PLPGSQL;

CREATE TRIGGER update_muni_nguid BEFORE INSERT
    ON ok911.municipal_boundary FOR EACH ROW EXECUTE PROCEDURE
    ok911.muni_func_nguid();


CREATE OR REPLACE FUNCTION ok911.muni_func_date()
RETURNS TRIGGER AS $$
BEGIN
   NEW.reveditor = current_user;
   NEW.revdate = current_timestamp;
   NEW.effectdate = current_timestamp;
   NEW.expiredate = current_timestamp + interval '10 years';
   RETURN NEW;
END;
$$
LANGUAGE PLPGSQL;

CREATE TRIGGER update_muni_date BEFORE INSERT OR UPDATE
    ON ok911.municipal_boundary FOR EACH ROW EXECUTE PROCEDURE
    ok911.muni_func_date();


CREATE OR REPLACE FUNCTION ok911.muni_func_initidate()
RETURNS TRIGGER AS $$
BEGIN
   NEW.initidate = current_timestamp;
   RETURN NEW;
END;
$$
LANGUAGE PLPGSQL;

CREATE TRIGGER update_muni_initidate BEFORE INSERT 
    ON ok911.municipal_boundary FOR EACH ROW EXECUTE PROCEDURE
    ok911.muni_func_initidate();

--=================================================================================================
--discrepancyagency_boundary
--=================================================================================================
CREATE OR REPLACE FUNCTION ok911.dscbound_func_nguid()
RETURNS TRIGGER AS $$
BEGIN
   NEW.nguid_disc = 'discrepancyagency_boundary_'||new.agency||'_'||new.id||'@'||new.agency_id;
   RETURN NEW;
END;
$$
LANGUAGE PLPGSQL;

CREATE TRIGGER update_dscbound_nguid BEFORE INSERT
    ON ok911.discrepancyagency_boundary FOR EACH ROW EXECUTE PROCEDURE
    ok911.dscbound_func_nguid();


CREATE OR REPLACE FUNCTION ok911.discbound_func_date()
RETURNS TRIGGER AS $$
BEGIN
   NEW.reveditor = current_user;
   NEW.revdate = current_timestamp;
   NEW.effectdate = current_timestamp;
   NEW.expiredate = current_timestamp + interval '10 years';
   RETURN NEW;
END;
$$
LANGUAGE PLPGSQL;

CREATE TRIGGER update_dscbound_date BEFORE INSERT OR UPDATE
    ON ok911.discrepancyagency_boundary FOR EACH ROW EXECUTE PROCEDURE
    ok911.discbound_func_date();


CREATE OR REPLACE FUNCTION ok911.discbound_func_initidate()
RETURNS TRIGGER AS $$
BEGIN
   NEW.initidate = current_timestamp;
   RETURN NEW;
END;
$$
LANGUAGE PLPGSQL;

CREATE TRIGGER update_dscbound_initidate BEFORE INSERT 
    ON ok911.discrepancyagency_boundary FOR EACH ROW EXECUTE PROCEDURE
    ok911.discbound_func_initidate();

