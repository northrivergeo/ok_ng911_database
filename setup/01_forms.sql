--=================================================================================================
--This will make ownership of tables a bit easier. BE SURE TO CHANGE THE ROLE
--=================================================================================================

CREATE OR REPLACE FUNCTION trg_create_set_owner()
 RETURNS event_trigger
 LANGUAGE plpgsql
AS $$
DECLARE
  obj record;
BEGIN
  FOR obj IN SELECT * FROM pg_event_trigger_ddl_commands() WHERE command_tag='CREATE TABLE' LOOP
    EXECUTE format('ALTER TABLE %s OWNER TO <role>', obj.object_identity);
  END LOOP;
END;
$$;


CREATE EVENT TRIGGER trg_create_set_owner
 ON ddl_command_end
 WHEN tag IN ('CREATE TABLE')
 EXECUTE PROCEDURE trg_create_set_owner();



/* postgis schema */ 

create schema ok911; 
create schema garage; 


/* qgis form for predir and reference*/ 

DROP TABLE IF EXISTS ok911.predir_tbl; 
create table ok911.predir_tbl (
       predir varchar(9) primary key,
       description varchar(9)
        );

insert into ok911.predir_tbl (predir, description) values ('NORTH', 'NORTH');
insert into ok911.predir_tbl (predir, description) values ('SOUTH', 'SOUTH');
insert into ok911.predir_tbl (predir, description) values ('EAST', 'EAST');
insert into ok911.predir_tbl (predir, description) values ('WEST', 'WEST');
insert into ok911.predir_tbl (predir, description) values ('NORTHEAST', 'NORTHEAST');
insert into ok911.predir_tbl (predir, description) values ('NORTHWEST', 'NORTHWEST');
insert into ok911.predir_tbl (predir, description) values ('SOUTHEAST', 'SOUTHEAST');
insert into ok911.predir_tbl (predir, description) values ('SOUTHWEST', 'SOUTHWEST');


/* qgis form for legacy Directional */ 

DROP TABLE IF EXISTS ok911.lgcypredir_tbl; 
create table ok911.lgcypredir_tbl (
       lgcypredir varchar(9) primary key,
       description varchar(9)
        );

insert into ok911.lgcypredir_tbl (lgcypredir, description) values ('N', 'NORTH');
insert into ok911.lgcypredir_tbl (lgcypredir, description) values ('S', 'SOUTH');
insert into ok911.lgcypredir_tbl (lgcypredir, description) values ('E', 'EAST');
insert into ok911.lgcypredir_tbl (lgcypredir, description) values ('W', 'WEST');
insert into ok911.lgcypredir_tbl (lgcypredir, description) values ('NE', 'NORTHEAST');
insert into ok911.lgcypredir_tbl (lgcypredir, description) values ('NW', 'NORTHWEST');
insert into ok911.lgcypredir_tbl (lgcypredir, description) values ('SE', 'SOUTHEAST');
insert into ok911.lgcypredir_tbl (lgcypredir, description) values ('SW', 'SOUTHWEST');


/* qgis tables seg_side */ 

DROP TABLE IF EXISTS ok911.segside_tbl; 
create table ok911.rclside_tbl (
    rclside varchar(1) primary Key,
	description varchar(5)
        );

insert into ok911.rclside_tbl (rclside, description) values ('L', 'L');
insert into ok911.rclside_tbl (rclside, description) values ('R', 'R');
insert into ok911.rclside_tbl (rclside, description) values ('N', 'N');

/* C1 Street Suffix Abbreviations. Also to be used for Pre-type and PostMod */
DROP TABLE IF EXISTS ok911.type_tbl;
create table ok911.type_tbl ( 
	type varchar(50) primary key,  
        description varchar(24)
        ); 

insert into ok911.type_tbl (type, description) values ('ALLEY', 'ALLEY'); 
insert into ok911.type_tbl (type, description) values ('ANEX', 'ANEX'); 
insert into ok911.type_tbl (type, description) values ('ARCADE', 'ARCADE'); 
insert into ok911.type_tbl (type, description) values ('AVENUE', 'AVENUE'); 
insert into ok911.type_tbl (type, description) values ('BAYOU', 'BAYOU'); 
insert into ok911.type_tbl (type, description) values ('BEACH', 'BEACH'); 
insert into ok911.type_tbl (type, description) values ('BEND', 'BEND'); 
insert into ok911.type_tbl (type, description) values ('BLUFF', 'BLUFF'); 
insert into ok911.type_tbl (type, description) values ('BLUFFS', 'BLUFFS'); 
insert into ok911.type_tbl (type, description) values ('BOTTOM', 'BOTTOM'); 
insert into ok911.type_tbl (type, description) values ('BOULEVARD', 'BOULEVARD'); 
insert into ok911.type_tbl (type, description) values ('BRANCH', 'BRANCH'); 
insert into ok911.type_tbl (type, description) values ('BRIDGE', 'BRIDGE'); 
insert into ok911.type_tbl (type, description) values ('BROOK', 'BROOK'); 
insert into ok911.type_tbl (type, description) values ('BROOKS', 'BROOKS'); 
insert into ok911.type_tbl (type, description) values ('BURG', 'BURG'); 
insert into ok911.type_tbl (type, description) values ('BURGS', 'BURGS'); 
insert into ok911.type_tbl (type, description) values ('BYPASS', 'BYPASS'); 
insert into ok911.type_tbl (type, description) values ('CAMP', 'CAMP'); 
insert into ok911.type_tbl (type, description) values ('CANYON', 'CANYON'); 
insert into ok911.type_tbl (type, description) values ('CAPE', 'CAPE'); 
insert into ok911.type_tbl (type, description) values ('CAUSEWAY', 'CAUSEWAY'); 
insert into ok911.type_tbl (type, description) values ('CENTER', 'CENTER'); 
insert into ok911.type_tbl (type, description) values ('CENTERS', 'CENTERS'); 
insert into ok911.type_tbl (type, description) values ('CIRCLE', 'CIRCLE'); 
insert into ok911.type_tbl (type, description) values ('CIRCLES', 'CIRCLES'); 
insert into ok911.type_tbl (type, description) values ('CLIFF', 'CLIFF'); 
insert into ok911.type_tbl (type, description) values ('CLIFFS', 'CLIFFS'); 
insert into ok911.type_tbl (type, description) values ('CLUB', 'CLUB'); 
insert into ok911.type_tbl (type, description) values ('COMMON', 'COMMON'); 
insert into ok911.type_tbl (type, description) values ('COMMONS', 'COMMONS'); 
insert into ok911.type_tbl (type, description) values ('CORNER', 'CORNER'); 
insert into ok911.type_tbl (type, description) values ('CORNERSS', 'CORNERS'); 
insert into ok911.type_tbl (type, description) values ('COURSE', 'COURSE'); 
insert into ok911.type_tbl (type, description) values ('COURT', 'COURT'); 
insert into ok911.type_tbl (type, description) values ('COURTS', 'COURTS'); 
insert into ok911.type_tbl (type, description) values ('COVE', 'COVE'); 
insert into ok911.type_tbl (type, description) values ('COVES', 'COVES'); 
insert into ok911.type_tbl (type, description) values ('CREEK', 'CREEK'); 
insert into ok911.type_tbl (type, description) values ('CRESCENT', 'CRESCENT'); 
insert into ok911.type_tbl (type, description) values ('CREST', 'CREST'); 
insert into ok911.type_tbl (type, description) values ('CROSSING', 'CROSSING'); 
insert into ok911.type_tbl (type, description) values ('CROSSROAD', 'CROSSROAD'); 
insert into ok911.type_tbl (type, description) values ('CROSSROADS', 'CROSSROADS'); 
insert into ok911.type_tbl (type, description) values ('CURVE', 'CURVE'); 
insert into ok911.type_tbl (type, description) values ('DALE', 'DALE'); 
insert into ok911.type_tbl (type, description) values ('DAM', 'DAM'); 
insert into ok911.type_tbl (type, description) values ('DIVIDE', 'DIVIDE'); 
insert into ok911.type_tbl (type, description) values ('DRIVE', 'DRIVE'); 
insert into ok911.type_tbl (type, description) values ('DRIVES', 'DRIVES'); 
insert into ok911.type_tbl (type, description) values ('ESTATE', 'ESTATE'); 
insert into ok911.type_tbl (type, description) values ('ESTATES', 'ESTATES'); 
insert into ok911.type_tbl (type, description) values ('EXPRESSWAY', 'EXPRESSWAY'); 
insert into ok911.type_tbl (type, description) values ('EXTENTION', 'EXTENTION'); 
insert into ok911.type_tbl (type, description) values ('EXTENTIONS', 'EXTENTIONS'); 
insert into ok911.type_tbl (type, description) values ('FALL', 'FALL'); 
insert into ok911.type_tbl (type, description) values ('FALLS', 'FALLS'); 
insert into ok911.type_tbl (type, description) values ('FERRY', 'FERRY');  
insert into ok911.type_tbl (type, description) values ('FIELD', 'FIELD'); 
insert into ok911.type_tbl (type, description) values ('FIELDS', 'FIELDS'); 
insert into ok911.type_tbl (type, description) values ('FLAT', 'FLAT');
insert into ok911.type_tbl (type, description) values ('FLATS', 'FLATS');
insert into ok911.type_tbl (type, description) values ('FORD', 'FORD');
insert into ok911.type_tbl (type, description) values ('FORDS', 'FORDS');
insert into ok911.type_tbl (type, description) values ('FORREST', 'FOREST');
insert into ok911.type_tbl (type, description) values ('FORGE', 'FORGE');
insert into ok911.type_tbl (type, description) values ('FORGES', 'FORGES');
insert into ok911.type_tbl (type, description) values ('FORK', 'FORK');
insert into ok911.type_tbl (type, description) values ('FORKS', 'F)RKS');
insert into ok911.type_tbl (type, description) values ('FORT', 'FORT');
insert into ok911.type_tbl (type, description) values ('FREEWAY', 'FREEWAY');
insert into ok911.type_tbl (type, description) values ('GARDEN', 'GARDEN');
insert into ok911.type_tbl (type, description) values ('GARDENS', 'GARDENS');
insert into ok911.type_tbl (type, description) values ('GATEWAY', 'GATEWAY');
insert into ok911.type_tbl (type, description) values ('GLEN', 'GLEN');
insert into ok911.type_tbl (type, description) values ('GLENS', 'GLENS');
insert into ok911.type_tbl (type, description) values ('GREEN', 'GREEN');
insert into ok911.type_tbl (type, description) values ('GREENS', 'GREENS');
insert into ok911.type_tbl (type, description) values ('GROVE', 'GROVE');
insert into ok911.type_tbl (type, description) values ('GROVES', 'GROVES');
insert into ok911.type_tbl (type, description) values ('HARBOR', 'HARBOR');
insert into ok911.type_tbl (type, description) values ('HARBORS', 'HARBORS');
insert into ok911.type_tbl (type, description) values ('HAVEN', 'HAVEN');
insert into ok911.type_tbl (type, description) values ('HEIGHTS', 'HEIGHTS');
insert into ok911.type_tbl (type, description) values ('HIGHWAY', 'HIGHWAY');
insert into ok911.type_tbl (type, description) values ('HILL', 'HILL');
insert into ok911.type_tbl (type, description) values ('HILLS', 'HILLS');
insert into ok911.type_tbl (type, description) values ('HOLLOW', 'HOLLOW');
insert into ok911.type_tbl (type, description) values ('INLT', 'INLET');
insert into ok911.type_tbl (type, description) values ('ISLAND', 'ISLAND');
insert into ok911.type_tbl (type, description) values ('ISLANDS', 'ISLANDS');
insert into ok911.type_tbl (type, description) values ('ISLE', 'ISLE');
insert into ok911.type_tbl (type, description) values ('JUNCTION', 'JUNCTION');
insert into ok911.type_tbl (type, description) values ('JUNCTIONS', 'JUNCTIONS');
insert into ok911.type_tbl (type, description) values ('KEY', 'KEY');
insert into ok911.type_tbl (type, description) values ('KEYS', 'KEYS');
insert into ok911.type_tbl (type, description) values ('KNOLL', 'KNOLL');
insert into ok911.type_tbl (type, description) values ('KNOLLS', 'KNOLLS');
insert into ok911.type_tbl (type, description) values ('LAKE', 'LAKE');
insert into ok911.type_tbl (type, description) values ('LAKES', 'LAKES');
insert into ok911.type_tbl (type, description) values ('LAND', 'LAND');
insert into ok911.type_tbl (type, description) values ('LANDING', 'LANDING');
insert into ok911.type_tbl (type, description) values ('LANE', 'LANE');
insert into ok911.type_tbl (type, description) values ('LIGHT', 'LIGHT');
insert into ok911.type_tbl (type, description) values ('LIGHTS', 'LIGHTS');
insert into ok911.type_tbl (type, description) values ('LOAF', 'LOAF');
insert into ok911.type_tbl (type, description) values ('LOCK', 'LOCK');
insert into ok911.type_tbl (type, description) values ('LOCKS', 'LOCKS');
insert into ok911.type_tbl (type, description) values ('LODGE', 'LODGE');
insert into ok911.type_tbl (type, description) values ('LOOP', 'LOOP');
insert into ok911.type_tbl (type, description) values ('MALL', 'MALL');
insert into ok911.type_tbl (type, description) values ('MANOR', 'MANOR');
insert into ok911.type_tbl (type, description) values ('MANORS', 'MANORS');
insert into ok911.type_tbl (type, description) values ('MEADOW', 'MEADOW');
insert into ok911.type_tbl (type, description) values ('MEADOWS', 'MEADOWS');
insert into ok911.type_tbl (type, description) values ('MEWS', 'MEWS');
insert into ok911.type_tbl (type, description) values ('MILL', 'MILL');
insert into ok911.type_tbl (type, description) values ('MILLS', 'MILLS');
insert into ok911.type_tbl (type, description) values ('MISSION', 'MISSION');
insert into ok911.type_tbl (type, description) values ('MOTORWAY', 'MOTORWAY');
insert into ok911.type_tbl (type, description) values ('MOUNT', 'MOUNT');
insert into ok911.type_tbl (type, description) values ('MOUNTAIN', 'MOUNTAIN');
insert into ok911.type_tbl (type, description) values ('MOUNTAINS', 'MOUNTAINS');
insert into ok911.type_tbl (type, description) values ('NECK', 'NECK');
insert into ok911.type_tbl (type, description) values ('ORCHARD', 'ORCHARD');
insert into ok911.type_tbl (type, description) values ('OVAL', 'OVAL');
insert into ok911.type_tbl (type, description) values ('OVERPASS', 'OVERPASS');
insert into ok911.type_tbl (type, description) values ('PARK', 'PARK');
insert into ok911.type_tbl (type, description) values ('PARKWAY', 'PARKWAY');
insert into ok911.type_tbl (type, description) values ('PASS', 'PASS');
insert into ok911.type_tbl (type, description) values ('PASSAGE', 'PASSAGE');
insert into ok911.type_tbl (type, description) values ('PATH', 'PATH');
insert into ok911.type_tbl (type, description) values ('PIKE', 'PIKE');
insert into ok911.type_tbl (type, description) values ('PINE', 'PINE');
insert into ok911.type_tbl (type, description) values ('PINES', 'PINES');
insert into ok911.type_tbl (type, description) values ('PLACE', 'PLACE');
insert into ok911.type_tbl (type, description) values ('PLAIN', 'PLAIN');
insert into ok911.type_tbl (type, description) values ('PLAINS', 'PLAINS');
insert into ok911.type_tbl (type, description) values ('PLAZA', 'PLAZA');
insert into ok911.type_tbl (type, description) values ('POINT', 'POINT');
insert into ok911.type_tbl (type, description) values ('POINTS', 'POINTS');
insert into ok911.type_tbl (type, description) values ('PORT', 'PORT');
insert into ok911.type_tbl (type, description) values ('PORTS', 'PORTS');
insert into ok911.type_tbl (type, description) values ('PRARIE', 'PRARIE');
insert into ok911.type_tbl (type, description) values ('RADIAL', 'RADIAL');
insert into ok911.type_tbl (type, description) values ('RAMP', 'RAMP');
insert into ok911.type_tbl (type, description) values ('RANCH', 'RANCH');
insert into ok911.type_tbl (type, description) values ('RAPID', 'RAPID');
insert into ok911.type_tbl (type, description) values ('RAPIDS', 'RAPIDS');
insert into ok911.type_tbl (type, description) values ('REST', 'REST');
insert into ok911.type_tbl (type, description) values ('RIDGE', 'RIDGE');
insert into ok911.type_tbl (type, description) values ('RIDGES', 'RIDGES');
insert into ok911.type_tbl (type, description) values ('RIVER', 'RIVER');
insert into ok911.type_tbl (type, description) values ('ROAD', 'ROAD');
insert into ok911.type_tbl (type, description) values ('ROADS', 'ROADS');
insert into ok911.type_tbl (type, description) values ('ROUTE', 'ROUTE');
insert into ok911.type_tbl (type, description) values ('ROW', 'ROW');
insert into ok911.type_tbl (type, description) values ('RUE', 'RUE');
insert into ok911.type_tbl (type, description) values ('RUN', 'RUN');
insert into ok911.type_tbl (type, description) values ('SHOAL', 'SHOAL');
insert into ok911.type_tbl (type, description) values ('SHOALS', 'SHOALS');
insert into ok911.type_tbl (type, description) values ('SHORE', 'SHORE');
insert into ok911.type_tbl (type, description) values ('SHORES', 'SHORES');
insert into ok911.type_tbl (type, description) values ('SKYWAY', 'SKYWAY');
insert into ok911.type_tbl (type, description) values ('SPRING', 'SPRING');
insert into ok911.type_tbl (type, description) values ('SPRINGS', 'SPRINGS');
insert into ok911.type_tbl (type, description) values ('SPUR', 'SPUR');
insert into ok911.type_tbl (type, description) values ('SQUARE', 'SQUARE');
insert into ok911.type_tbl (type, description) values ('SQUARES', 'SQUARES');
insert into ok911.type_tbl (type, description) values ('STATION', 'STATION');
insert into ok911.type_tbl (type, description) values ('STRAVENUE', 'STRAVENUE');
insert into ok911.type_tbl (type, description) values ('STREAM', 'STREAM');
insert into ok911.type_tbl (type, description) values ('STREET', 'STREET');
insert into ok911.type_tbl (type, description) values ('STREETS', 'STREETS');
insert into ok911.type_tbl (type, description) values ('SUMMIT', 'SUMMIT');
insert into ok911.type_tbl (type, description) values ('TERRACE', 'TERRACE');
insert into ok911.type_tbl (type, description) values ('TRHOUGHWAY', 'THROUGHWAY');
insert into ok911.type_tbl (type, description) values ('TRACE', 'TRACE');
insert into ok911.type_tbl (type, description) values ('TRACK', 'TRACK');
insert into ok911.type_tbl (type, description) values ('TRAFFICWAY', 'TRAFFICWAY');
insert into ok911.type_tbl (type, description) values ('TRAIL', 'TRAIL');
insert into ok911.type_tbl (type, description) values ('TRAILER', 'TRAILER');
insert into ok911.type_tbl (type, description) values ('TUNNEL', 'TUNNEL');
insert into ok911.type_tbl (type, description) values ('TURNPIKE', 'TURNPIKE');
insert into ok911.type_tbl (type, description) values ('UNDERPASS', 'UNDERPASS');
insert into ok911.type_tbl (type, description) values ('UNION', 'UNION');
insert into ok911.type_tbl (type, description) values ('UNIONS', 'UNIONS');
insert into ok911.type_tbl (type, description) values ('VALLEY', 'VALLEY');
insert into ok911.type_tbl (type, description) values ('VALLEYS', 'VALLEYS');
insert into ok911.type_tbl (type, description) values ('VIADUCT', 'VIADUCT');
insert into ok911.type_tbl (type, description) values ('VIEW', 'VIEW');
insert into ok911.type_tbl (type, description) values ('VIEWS', 'VIEWS');
insert into ok911.type_tbl (type, description) values ('VILLAGE', 'VILLAGE');
insert into ok911.type_tbl (type, description) values ('VILLAGES', 'VILLAGES');
insert into ok911.type_tbl (type, description) values ('VILLE', 'VILLE');
insert into ok911.type_tbl (type, description) values ('VISTA', 'VISTA');
insert into ok911.type_tbl (type, description) values ('WALK', 'WALK');
insert into ok911.type_tbl (type, description) values ('WALL', 'WALL');
insert into ok911.type_tbl (type, description) values ('WAY', 'WAY');
insert into ok911.type_tbl (type, description) values ('WAYS', 'WAYS');
insert into ok911.type_tbl (type, description) values ('WELL', 'WELL');
insert into ok911.type_tbl (type, description) values ('WELLS', 'WELLS');


/* C1 Street Suffix Abbreviations. Also to be used for Pre-type and PostMod */
DROP TABLE IF EXISTS ok911.lgcytype_tbl;
create table ok911.lgcytype_tbl ( 
        type varchar(50) primary key,  
        description varchar(24)
        ); 

insert into ok911.lgcytype_tbl (type, description) values ('ALY', 'ALLEY'); 
insert into ok911.lgcytype_tbl (type, description) values ('ANX', 'ANEX'); 
insert into ok911.lgcytype_tbl (type, description) values ('ARC', 'ARCADE'); 
insert into ok911.lgcytype_tbl (type, description) values ('AVE', 'AVENUE'); 
insert into ok911.lgcytype_tbl (type, description) values ('BYU', 'BAYOU'); 
insert into ok911.lgcytype_tbl (type, description) values ('BCH', 'BEACH'); 
insert into ok911.lgcytype_tbl (type, description) values ('BND', 'BEND'); 
insert into ok911.lgcytype_tbl (type, description) values ('BLF', 'BLUFF'); 
insert into ok911.lgcytype_tbl (type, description) values ('BLFS', 'BLUFFS'); 
insert into ok911.lgcytype_tbl (type, description) values ('BTM', 'BOTTOM'); 
insert into ok911.lgcytype_tbl (type, description) values ('BLVD', 'BOULEVARD'); 
insert into ok911.lgcytype_tbl (type, description) values ('BR', 'BRANCH'); 
insert into ok911.lgcytype_tbl (type, description) values ('BRG', 'BRIDGE'); 
insert into ok911.lgcytype_tbl (type, description) values ('BRK', 'BROOK'); 
insert into ok911.lgcytype_tbl (type, description) values ('BRKS', 'BROOKS'); 
insert into ok911.lgcytype_tbl (type, description) values ('BG', 'BURG'); 
insert into ok911.lgcytype_tbl (type, description) values ('BGS', 'BURGS'); 
insert into ok911.lgcytype_tbl (type, description) values ('BYP', 'BYPASS'); 
insert into ok911.lgcytype_tbl (type, description) values ('CP', 'CAMP'); 
insert into ok911.lgcytype_tbl (type, description) values ('CYN', 'CANYON'); 
insert into ok911.lgcytype_tbl (type, description) values ('CPE', 'CAPE'); 
insert into ok911.lgcytype_tbl (type, description) values ('CSWY', 'CAUSEWAY'); 
insert into ok911.lgcytype_tbl (type, description) values ('CTR', 'CENTER'); 
insert into ok911.lgcytype_tbl (type, description) values ('CTRS', 'CENTERS'); 
insert into ok911.lgcytype_tbl (type, description) values ('CIR', 'CIRCLE'); 
insert into ok911.lgcytype_tbl (type, description) values ('CIRS', 'CIRCLES'); 
insert into ok911.lgcytype_tbl (type, description) values ('CLF', 'CLIFF'); 
insert into ok911.lgcytype_tbl (type, description) values ('CLFS', 'CLIFFS'); 
insert into ok911.lgcytype_tbl (type, description) values ('CLB', 'CLUB'); 
insert into ok911.lgcytype_tbl (type, description) values ('CMN', 'COMMON'); 
insert into ok911.lgcytype_tbl (type, description) values ('CMNS', 'COMMONS'); 
insert into ok911.lgcytype_tbl (type, description) values ('COR', 'CORNER'); 
insert into ok911.lgcytype_tbl (type, description) values ('CORS', 'CORNERS'); 
insert into ok911.lgcytype_tbl (type, description) values ('CRSE', 'COURSE'); 
insert into ok911.lgcytype_tbl (type, description) values ('CT', 'COURT'); 
insert into ok911.lgcytype_tbl (type, description) values ('CTS', 'COURTS'); 
insert into ok911.lgcytype_tbl (type, description) values ('CV', 'COVE'); 
insert into ok911.lgcytype_tbl (type, description) values ('CVS', 'COVES'); 
insert into ok911.lgcytype_tbl (type, description) values ('CRK', 'CREEK'); 
insert into ok911.lgcytype_tbl (type, description) values ('CRES', 'CRESCENT'); 
insert into ok911.lgcytype_tbl (type, description) values ('CRST', 'CREST'); 
insert into ok911.lgcytype_tbl (type, description) values ('XING', 'CROSSING'); 
insert into ok911.lgcytype_tbl (type, description) values ('XRD', 'CROSSROAD'); 
insert into ok911.lgcytype_tbl (type, description) values ('XRDS', 'CROSSROADS'); 
insert into ok911.lgcytype_tbl (type, description) values ('CURV', 'CURVE'); 
insert into ok911.lgcytype_tbl (type, description) values ('DL', 'DALE'); 
insert into ok911.lgcytype_tbl (type, description) values ('DM', 'DAM'); 
insert into ok911.lgcytype_tbl (type, description) values ('DV', 'DIVIDE'); 
insert into ok911.lgcytype_tbl (type, description) values ('DR', 'DRIVE'); 
insert into ok911.lgcytype_tbl (type, description) values ('DRS', 'DRIVES'); 
insert into ok911.lgcytype_tbl (type, description) values ('EST', 'ESTATE'); 
insert into ok911.lgcytype_tbl (type, description) values ('ESTS', 'ESTATES'); 
insert into ok911.lgcytype_tbl (type, description) values ('EXPY', 'EXPRESSWAY'); 
insert into ok911.lgcytype_tbl (type, description) values ('EXT', 'EXTENTION'); 
insert into ok911.lgcytype_tbl (type, description) values ('EXTS', 'EXTENTIONS'); 
insert into ok911.lgcytype_tbl (type, description) values ('FALL', 'FALL'); 
insert into ok911.lgcytype_tbl (type, description) values ('FLS', 'FALLS'); 
insert into ok911.lgcytype_tbl (type, description) values ('FRY', 'FERRY');  
insert into ok911.lgcytype_tbl (type, description) values ('FLD', 'FIELD'); 
insert into ok911.lgcytype_tbl (type, description) values ('FLDS', 'FIELDS'); 
insert into ok911.lgcytype_tbl (type, description) values ('FLT', 'FLAT');
insert into ok911.lgcytype_tbl (type, description) values ('FLTS', 'FLATS');
insert into ok911.lgcytype_tbl (type, description) values ('FRD', 'FORD');
insert into ok911.lgcytype_tbl (type, description) values ('FRDS', 'FORDS');
insert into ok911.lgcytype_tbl (type, description) values ('FRST', 'FOREST');
insert into ok911.lgcytype_tbl (type, description) values ('FRG', 'FORGE');
insert into ok911.lgcytype_tbl (type, description) values ('FRGS', 'FORGES');
insert into ok911.lgcytype_tbl (type, description) values ('FRK', 'FORK');
insert into ok911.lgcytype_tbl (type, description) values ('FRKS', 'F)RKS');
insert into ok911.lgcytype_tbl (type, description) values ('FT', 'FORT');
insert into ok911.lgcytype_tbl (type, description) values ('FWY', 'FREEWAY');
insert into ok911.lgcytype_tbl (type, description) values ('GDN', 'GARDEN');
insert into ok911.lgcytype_tbl (type, description) values ('GDNS', 'GARDENS');
insert into ok911.lgcytype_tbl (type, description) values ('GTWY', 'GATEWAY');
insert into ok911.lgcytype_tbl (type, description) values ('GLN', 'GLEN');
insert into ok911.lgcytype_tbl (type, description) values ('GLNS', 'GLENS');
insert into ok911.lgcytype_tbl (type, description) values ('GRN', 'GREEN');
insert into ok911.lgcytype_tbl (type, description) values ('GRNS', 'GREENS');
insert into ok911.lgcytype_tbl (type, description) values ('GRV', 'GROVE');
insert into ok911.lgcytype_tbl (type, description) values ('GRVS', 'GROVES');
insert into ok911.lgcytype_tbl (type, description) values ('HBR', 'HARBOR');
insert into ok911.lgcytype_tbl (type, description) values ('HBRS', 'HARBORS');
insert into ok911.lgcytype_tbl (type, description) values ('HVN', 'HAVEN');
insert into ok911.lgcytype_tbl (type, description) values ('HTS', 'HEIGHTS');
insert into ok911.lgcytype_tbl (type, description) values ('HWY', 'HIGHWAY');
insert into ok911.lgcytype_tbl (type, description) values ('HL', 'HILL');
insert into ok911.lgcytype_tbl (type, description) values ('HLS', 'HILLS');
insert into ok911.lgcytype_tbl (type, description) values ('HOLW', 'HOLLOW');
insert into ok911.lgcytype_tbl (type, description) values ('INLT', 'INLET');
insert into ok911.lgcytype_tbl (type, description) values ('IS', 'ISLAND');
insert into ok911.lgcytype_tbl (type, description) values ('ISS', 'ISLANDS');
insert into ok911.lgcytype_tbl (type, description) values ('ISLE', 'ISLE');
insert into ok911.lgcytype_tbl (type, description) values ('JCT', 'JUNCTION');
insert into ok911.lgcytype_tbl (type, description) values ('JCTS', 'JUNCTIONS');
insert into ok911.lgcytype_tbl (type, description) values ('KY', 'KEY');
insert into ok911.lgcytype_tbl (type, description) values ('KYS', 'KEYS');
insert into ok911.lgcytype_tbl (type, description) values ('KNL', 'KNOLL');
insert into ok911.lgcytype_tbl (type, description) values ('KNLS', 'KNOLLS');
insert into ok911.lgcytype_tbl (type, description) values ('LK', 'LAKE');
insert into ok911.lgcytype_tbl (type, description) values ('LKS', 'LAKES');
insert into ok911.lgcytype_tbl (type, description) values ('LAND', 'LAND');
insert into ok911.lgcytype_tbl (type, description) values ('LNDG', 'LANDING');
insert into ok911.lgcytype_tbl (type, description) values ('LN', 'LANE');
insert into ok911.lgcytype_tbl (type, description) values ('LGT', 'LIGHT');
insert into ok911.lgcytype_tbl (type, description) values ('LGTS', 'LIGHTS');
insert into ok911.lgcytype_tbl (type, description) values ('LF', 'LOAF');
insert into ok911.lgcytype_tbl (type, description) values ('LCK', 'LOCK');
insert into ok911.lgcytype_tbl (type, description) values ('LCKS', 'LOCKS');
insert into ok911.lgcytype_tbl (type, description) values ('LDG', 'LODGE');
insert into ok911.lgcytype_tbl (type, description) values ('LOOP', 'LOOP');
insert into ok911.lgcytype_tbl (type, description) values ('MALL', 'MALL');
insert into ok911.lgcytype_tbl (type, description) values ('MNR', 'MANOR');
insert into ok911.lgcytype_tbl (type, description) values ('MNRS', 'MANORS');
insert into ok911.lgcytype_tbl (type, description) values ('MDW', 'MEADOW');
insert into ok911.lgcytype_tbl (type, description) values ('MDWS', 'MEADOWS');
insert into ok911.lgcytype_tbl (type, description) values ('MEWS', 'MEWS');
insert into ok911.lgcytype_tbl (type, description) values ('ML', 'MILL');
insert into ok911.lgcytype_tbl (type, description) values ('MLS', 'MILLS');
insert into ok911.lgcytype_tbl (type, description) values ('MSN', 'MISSION');
insert into ok911.lgcytype_tbl (type, description) values ('MTWY', 'MOTORWAY');
insert into ok911.lgcytype_tbl (type, description) values ('MT', 'MOUNT');
insert into ok911.lgcytype_tbl (type, description) values ('MTN', 'MOUNTAIN');
insert into ok911.lgcytype_tbl (type, description) values ('MTNS', 'MOUNTAINS');
insert into ok911.lgcytype_tbl (type, description) values ('NCK', 'NECK');
insert into ok911.lgcytype_tbl (type, description) values ('ORCH', 'ORCHARD');
insert into ok911.lgcytype_tbl (type, description) values ('OVAL', 'OVAL');
insert into ok911.lgcytype_tbl (type, description) values ('OPAS', 'OVERPASS');
insert into ok911.lgcytype_tbl (type, description) values ('PARK', 'PARK');
insert into ok911.lgcytype_tbl (type, description) values ('PKWY', 'PARKWAY');
insert into ok911.lgcytype_tbl (type, description) values ('PASS', 'PASS');
insert into ok911.lgcytype_tbl (type, description) values ('PSGE', 'PASSAGE');
insert into ok911.lgcytype_tbl (type, description) values ('PATH', 'PATH');
insert into ok911.lgcytype_tbl (type, description) values ('PIKE', 'PIKE');
insert into ok911.lgcytype_tbl (type, description) values ('PNE', 'PINE');
insert into ok911.lgcytype_tbl (type, description) values ('PNES', 'PINES');
insert into ok911.lgcytype_tbl (type, description) values ('PL', 'PLACE');
insert into ok911.lgcytype_tbl (type, description) values ('PLN', 'PLAIN');
insert into ok911.lgcytype_tbl (type, description) values ('PLNS', 'PLAINS');
insert into ok911.lgcytype_tbl (type, description) values ('PLZ', 'PLAZA');
insert into ok911.lgcytype_tbl (type, description) values ('PT', 'POINT');
insert into ok911.lgcytype_tbl (type, description) values ('PTS', 'POINTS');
insert into ok911.lgcytype_tbl (type, description) values ('PRT', 'PORT');
insert into ok911.lgcytype_tbl (type, description) values ('PRTS', 'PORTS');
insert into ok911.lgcytype_tbl (type, description) values ('PR', 'PRARIE');
insert into ok911.lgcytype_tbl (type, description) values ('RADL', 'RADIAL');
insert into ok911.lgcytype_tbl (type, description) values ('RAMP', 'RAMP');
insert into ok911.lgcytype_tbl (type, description) values ('RNCH', 'RANCH');
insert into ok911.lgcytype_tbl (type, description) values ('RPID', 'RAPID');
insert into ok911.lgcytype_tbl (type, description) values ('RPDS', 'RAPIDS');
insert into ok911.lgcytype_tbl (type, description) values ('RST', 'REST');
insert into ok911.lgcytype_tbl (type, description) values ('RDG', 'RIDGE');
insert into ok911.lgcytype_tbl (type, description) values ('RDGS', 'RIDGES');
insert into ok911.lgcytype_tbl (type, description) values ('RIV', 'RIVER');
insert into ok911.lgcytype_tbl (type, description) values ('RD', 'ROAD');
insert into ok911.lgcytype_tbl (type, description) values ('RDS', 'ROADS');
insert into ok911.lgcytype_tbl (type, description) values ('RTE', 'ROUTE');
insert into ok911.lgcytype_tbl (type, description) values ('ROW', 'ROW');
insert into ok911.lgcytype_tbl (type, description) values ('RUE', 'RUE');
insert into ok911.lgcytype_tbl (type, description) values ('RUN', 'RUN');
insert into ok911.lgcytype_tbl (type, description) values ('SHL', 'SHOAL');
insert into ok911.lgcytype_tbl (type, description) values ('SHLS', 'SHOALS');
insert into ok911.lgcytype_tbl (type, description) values ('SHR', 'SHORE');
insert into ok911.lgcytype_tbl (type, description) values ('SHRS', 'SHORES');
insert into ok911.lgcytype_tbl (type, description) values ('SKWY', 'SKYWAY');
insert into ok911.lgcytype_tbl (type, description) values ('SPG', 'SPRING');
insert into ok911.lgcytype_tbl (type, description) values ('SPGS', 'SPRINGS');
insert into ok911.lgcytype_tbl (type, description) values ('SPUR', 'SPUR');
insert into ok911.lgcytype_tbl (type, description) values ('SQ', 'SQUARE');
insert into ok911.lgcytype_tbl (type, description) values ('SQS', 'SQUARES');
insert into ok911.lgcytype_tbl (type, description) values ('STA', 'STATION');
insert into ok911.lgcytype_tbl (type, description) values ('STRA', 'STRAVENUE');
insert into ok911.lgcytype_tbl (type, description) values ('STRM', 'STREAM');
insert into ok911.lgcytype_tbl (type, description) values ('ST', 'STREET');
insert into ok911.lgcytype_tbl (type, description) values ('STS', 'STREETS');
insert into ok911.lgcytype_tbl (type, description) values ('SMT', 'SUMMIT');
insert into ok911.lgcytype_tbl (type, description) values ('TER', 'TERRACE');
insert into ok911.lgcytype_tbl (type, description) values ('TRWY', 'TRHOUGHWAY');
insert into ok911.lgcytype_tbl (type, description) values ('TRCE', 'TRACE');
insert into ok911.lgcytype_tbl (type, description) values ('TRAK', 'TRACK');
insert into ok911.lgcytype_tbl (type, description) values ('TRFY', 'TRAFFICWAY');
insert into ok911.lgcytype_tbl (type, description) values ('TRL', 'TRAIL');
insert into ok911.lgcytype_tbl (type, description) values ('TRLR', 'TRAILER');
insert into ok911.lgcytype_tbl (type, description) values ('TUNL', 'TUNNEL');
insert into ok911.lgcytype_tbl (type, description) values ('TPKE', 'TURNPIKE');
insert into ok911.lgcytype_tbl (type, description) values ('UPAS', 'UNDERPASS');
insert into ok911.lgcytype_tbl (type, description) values ('UN', 'UNION');
insert into ok911.lgcytype_tbl (type, description) values ('UNS', 'UNIONS');
insert into ok911.lgcytype_tbl (type, description) values ('VLY', 'VALLEY');
insert into ok911.lgcytype_tbl (type, description) values ('VLYS', 'VALLEYS');
insert into ok911.lgcytype_tbl (type, description) values ('VIA', 'VIADUCT');
insert into ok911.lgcytype_tbl (type, description) values ('VW', 'VIEW');
insert into ok911.lgcytype_tbl (type, description) values ('VWS', 'VIEWS');
insert into ok911.lgcytype_tbl (type, description) values ('VLG', 'VILLAGE');
insert into ok911.lgcytype_tbl (type, description) values ('VLGS', 'VILLAGES');
insert into ok911.lgcytype_tbl (type, description) values ('VL', 'VILLE');
insert into ok911.lgcytype_tbl (type, description) values ('VIS', 'VISTA');
insert into ok911.lgcytype_tbl (type, description) values ('WALK', 'WALK');
insert into ok911.lgcytype_tbl (type, description) values ('WALL', 'WALL');
insert into ok911.lgcytype_tbl (type, description) values ('WAY', 'WAY');
insert into ok911.lgcytype_tbl (type, description) values ('WAYS', 'WAYS');
insert into ok911.lgcytype_tbl (type, description) values ('WL', 'WELL');
insert into ok911.lgcytype_tbl (type, description) values ('WLS', 'WELLS');


DROP TABLE IF EXISTS ok911.oneway_tbl; 
create table ok911.oneway_tbl ( 
	oneway varchar(3) primary key,
	description varchar(12)
        ); 

insert into ok911.oneway_tbl (oneway, description) values ('B', 'BOTH'); 
insert into ok911.oneway_tbl (oneway, description) values ('FT', 'FROM TO'); 
insert into ok911.oneway_tbl (oneway, description) values ('TF', 'TO FROM'); 
insert into ok911.oneway_tbl (oneway, description) values ('N', 'NONE'); 

/*separator phrase*/


DROP TABLE IF EXISTS ok911.separator_tbl; 
create table ok911.separator_tbl ( 
	pretypesep varchar(20) primary key,
	description varchar(20)
        ); 

insert into ok911.separator_tbl (pretypesep, description) values ('OF THE', 'OF THE'); 
insert into ok911.separator_tbl (pretypesep, description) values ('AT', 'AT'); 
insert into ok911.separator_tbl (pretypesep, description) values ('DE LAS', 'DE LAS'); 
insert into ok911.separator_tbl (pretypesep, description) values ('DES', 'DES'); 
insert into ok911.separator_tbl (pretypesep, description) values ('IN THE', 'IN THE'); 
insert into ok911.separator_tbl (pretypesep, description) values ('TO THE', 'TO THE'); 
insert into ok911.separator_tbl (pretypesep, description) values ('OF', 'OF'); 
insert into ok911.separator_tbl (pretypesep, description) values ('ON THE', 'ON THE'); 
insert into ok911.separator_tbl (pretypesep, description) values ('TO', 'TO'); 


DROP TABLE IF EXISTS ok911.placetype_tbl; 
create table ok911.placetype_tbl ( 
	placetype varchar(50) primary key,
	description varchar(50)
        ); 

insert into ok911.placetype_tbl (placetype, description) values ('AIRCRAFT', 'AIRCRAFT');
insert into ok911.placetype_tbl (placetype, description) values ('AIRPORT', 'AIRPORT');
insert into ok911.placetype_tbl (placetype, description) values ('ARENA', 'ARENA');
insert into ok911.placetype_tbl (placetype, description) values ('AUTOMOBILE', 'AUTOMOBILE');
insert into ok911.placetype_tbl (placetype, description) values ('BANK,', 'BANK');
insert into ok911.placetype_tbl (placetype, description) values ('BAR,', 'BAR');
insert into ok911.placetype_tbl (placetype, description) values ('BICYCLE', 'BICYCLE');
insert into ok911.placetype_tbl (placetype, description) values ('BUS', 'BUS');
insert into ok911.placetype_tbl (placetype, description) values ('BUS-STATION', 'BUS-STATION');
insert into ok911.placetype_tbl (placetype, description) values ('CAFE', 'CAFE');
insert into ok911.placetype_tbl (placetype, description) values ('CLASSROOM', 'CLASSROOM');
insert into ok911.placetype_tbl (placetype, description) values ('CLUB', 'CLUB');
insert into ok911.placetype_tbl (placetype, description) values ('CONSTRUCTION', 'CONSTRUCTION');
insert into ok911.placetype_tbl (placetype, description) values ('CONVENTION-CENTER', 'CONVENTION-CENTER');
insert into ok911.placetype_tbl (placetype, description) values ('GOVERNMENT', 'GOVERNMENT');
insert into ok911.placetype_tbl (placetype, description) values ('HOSPITAL', 'HOSPITAL');
insert into ok911.placetype_tbl (placetype, description) values ('HOTEL', 'HOTEL');
insert into ok911.placetype_tbl (placetype, description) values ('INDUSTRIAL', 'INDUSTRIAL');
insert into ok911.placetype_tbl (placetype, description) values ('LIBRARY', 'LIBRARY');
insert into ok911.placetype_tbl (placetype, description) values ('MOTORCYCLE', 'MOTORCYCLE');
insert into ok911.placetype_tbl (placetype, description) values ('OFFICE', 'OFFICE');
insert into ok911.placetype_tbl (placetype, description) values ('OTHER', 'OTHER');
insert into ok911.placetype_tbl (placetype, description) values ('OUTDOORS', 'OUTDOORS');
insert into ok911.placetype_tbl (placetype, description) values ('PARKING', 'PARKING');
insert into ok911.placetype_tbl (placetype, description) values ('PLACE-OF-WORSHIP',  'PLACE-OF-WORSHIP');
insert into ok911.placetype_tbl (placetype, description) values ('PRISON',  'PRISON');
insert into ok911.placetype_tbl (placetype, description) values ('PUBLIC', 'PUBLIC');
insert into ok911.placetype_tbl (placetype, description) values ('PUBLIC-TRANSPORT', 'PUBLIC-TRANSPORT');
insert into ok911.placetype_tbl (placetype, description) values ('RESIDENCE', 'RESIDENCE');
insert into ok911.placetype_tbl (placetype, description) values ('RESTAURANT', 'RESTAURANT');
insert into ok911.placetype_tbl (placetype, description) values ('SCHOOL', 'SCHOOL');
insert into ok911.placetype_tbl (placetype, description) values ('SHOPPING-AREA', 'SHOPPING-AREA');
insert into ok911.placetype_tbl (placetype, description) values ('STADIUM', 'STADIUM');
insert into ok911.placetype_tbl (placetype, description) values ('STORE', 'STORE');
insert into ok911.placetype_tbl (placetype, description) values ('STREET', 'STREET');
insert into ok911.placetype_tbl (placetype, description) values ('THEATER', 'THEATER');
insert into ok911.placetype_tbl (placetype, description) values ('TRAIN', 'TRAIN');
insert into ok911.placetype_tbl (placetype, description) values ('TRAIN-STATION', 'TRAIN-STATION');
insert into ok911.placetype_tbl (placetype, description) values ('TRUCK', 'TRUCK');
insert into ok911.placetype_tbl (placetype, description) values ('UNDERWAY', 'UNDERWAY');
insert into ok911.placetype_tbl (placetype, description) values ('UNKNOWN', 'UNKNOWN');
insert into ok911.placetype_tbl (placetype, description) values ('WAREHOUSE', 'WAREHOUSE');
insert into ok911.placetype_tbl (placetype, description) values ('WATER', 'WATER');
insert into ok911.placetype_tbl (placetype, description) values ('WATERCRAFT', 'WATERCRAFT');

DROP TABLE IF EXISTS ok911.roadclass_tbl; 
create table ok911.roadclass_tbl ( 
	roadclass varchar(15) primary key,
	description varchar(15)
        ); 

insert into ok911.roadclass_tbl (roadclass, description) values ('PRIMARY', 'PRIMARY');
insert into ok911.roadclass_tbl (roadclass, description) values ('SECONDARY', 'SECONDARY');
insert into ok911.roadclass_tbl (roadclass, description) values ('LOCAL', 'LOCAL');
insert into ok911.roadclass_tbl (roadclass, description) values ('RAMP', 'RAMP');
insert into ok911.roadclass_tbl (roadclass, description) values ('SERVICE DRIVE', 'SERVICE DRIVE');
insert into ok911.roadclass_tbl (roadclass, description) values ('VEHICULAR TRAIL', 'VEHICULAR TRAIL');
insert into ok911.roadclass_tbl (roadclass, description) values ('WALKWAY', 'WALKWAY');
insert into ok911.roadclass_tbl (roadclass, description) values ('STAIRWAY', 'STAIRWAY');
insert into ok911.roadclass_tbl (roadclass, description) values ('ALLEY', 'ALLEY');
insert into ok911.roadclass_tbl (roadclass, description) values ('PRIVATE', 'PRIVATE');
insert into ok911.roadclass_tbl (roadclass, description) values ('PARKING LOT', 'PARKING LOT');
insert into ok911.roadclass_tbl (roadclass, description) values ('TRAIL', 'TRAIL');
insert into ok911.roadclass_tbl (roadclass, description) values ('BRIDLE PATH', 'BRIDLE PATH');
insert into ok911.roadclass_tbl (roadclass, description) values ('OTHER', 'OTHER');

DROP TABLE IF EXISTS ok911.county_tbl; 
create table ok911.county_tbl ( 
	county varchar(40) primary key,
	description varchar(40)
        ); 

insert into ok911.county_tbl (county, description) values ('ADAIR COUNTY', 'ADAIR COUNTY');
insert into ok911.county_tbl (county, description) values ('ALFALFA COUNTY', 'ALFALFA COUNTY');
insert into ok911.county_tbl (county, description) values ('ATOKA COUNTY', 'ATOKA COUNTY');
insert into ok911.county_tbl (county, description) values ('BEAVER COUNTY', 'BEAVER COUNTY');
insert into ok911.county_tbl (county, description) values ('BECKHAM COUNTY', 'BECKHAM COUNTY');
insert into ok911.county_tbl (county, description) values ('BLAINE COUNTY', 'BLAINE COUNTY');
insert into ok911.county_tbl (county, description) values ('BRYAN COUNTY', 'BRYAN COUNTY');
insert into ok911.county_tbl (county, description) values ('CADDO COUNTY', 'CADDO COUNTY');
insert into ok911.county_tbl (county, description) values ('CANADIAN COUNTY', 'CANADIAN COUNTY');
insert into ok911.county_tbl (county, description) values ('CARTER COUNTY', 'CARTER COUNTY');
insert into ok911.county_tbl (county, description) values ('CHEROKEE COUNTY', 'CHEROKEE COUNTY');
insert into ok911.county_tbl (county, description) values ('CHOCTAW COUNTY', 'CHOCTAW COUNTY');
insert into ok911.county_tbl (county, description) values ('CIMARRON COUNTY', 'CIMARRON COUNTY');
insert into ok911.county_tbl (county, description) values ('CLEVELAND COUNTY', 'CLEVELAND COUNTY');
insert into ok911.county_tbl (county, description) values ('COAL COUNTY', 'COAL COUNTY');
insert into ok911.county_tbl (county, description) values ('COMANCHE COUNTY', 'COMANCHE COUNTY');
insert into ok911.county_tbl (county, description) values ('COTTON COUNTY', 'COTTON COUNTY');
insert into ok911.county_tbl (county, description) values ('CRAIG COUNTY', 'CRAIG COUNTY');
insert into ok911.county_tbl (county, description) values ('CREEK COUNTY', 'CREEK COUNTY');
insert into ok911.county_tbl (county, description) values ('CUSTER COUNTY', 'CUSTER COUNTY');
insert into ok911.county_tbl (county, description) values ('DELAWARE COUNTY', 'DELAWARE COUNTY');
insert into ok911.county_tbl (county, description) values ('DEWEY COUNTY', 'DEWEY COUNTY');
insert into ok911.county_tbl (county, description) values ('ELLIS COUNTY', 'ELLIS COUNTY');
insert into ok911.county_tbl (county, description) values ('GARFIELD COUNTY', 'GARFIELD COUNTY');
insert into ok911.county_tbl (county, description) values ('GARVIN COUNTY', 'GARVIN COUNTY');
insert into ok911.county_tbl (county, description) values ('GRADY COUNTY', 'GRADY COUNTY');
insert into ok911.county_tbl (county, description) values ('GRANT COUNTY', 'GRANT COUNTY');
insert into ok911.county_tbl (county, description) values ('GREER COUNTY', 'GREER COUNTY');
insert into ok911.county_tbl (county, description) values ('HARMON COUNTY', 'HARMON COUNTY');
insert into ok911.county_tbl (county, description) values ('HARPER COUNTY', 'HARPER COUNTY');
insert into ok911.county_tbl (county, description) values ('HASKELL COUNTY', 'HASKELL COUNTY');
insert into ok911.county_tbl (county, description) values ('HUGHES COUNTY', 'HUGHES COUNTY');
insert into ok911.county_tbl (county, description) values ('JACKSON COUNTY', 'JACKSON COUNTY');
insert into ok911.county_tbl (county, description) values ('JEFFERSON COUNTY', 'JEFFERSON COUNTY');
insert into ok911.county_tbl (county, description) values ('JOHNSTON COUNTY', 'JOHNSTON COUNTY');
insert into ok911.county_tbl (county, description) values ('KAY COUNTY', 'KAY COUNTY');
insert into ok911.county_tbl (county, description) values ('KINGFISHER COUNTY', 'KINGFISHER COUNTY');
insert into ok911.county_tbl (county, description) values ('KIOWA COUNTY', 'KIOWA COUNTY');
insert into ok911.county_tbl (county, description) values ('LATIMER COUNTY', 'LATIMER COUNTY');
insert into ok911.county_tbl (county, description) values ('LE FLORE COUNTY', 'LE FLORE COUNTY');
insert into ok911.county_tbl (county, description) values ('LINCOLN COUNTY', 'LINCOLN COUNTY');
insert into ok911.county_tbl (county, description) values ('LOGAN COUNTY', 'LOGAN COUNTY');
insert into ok911.county_tbl (county, description) values ('LOVE COUNTY', 'LOVE COUNTY');
insert into ok911.county_tbl (county, description) values ('MAJOR COUNTY', 'MAJOR COUNTY');
insert into ok911.county_tbl (county, description) values ('MARSHALL COUNTY', 'MARSHALL COUNTY');
insert into ok911.county_tbl (county, description) values ('MAYES COUNTY', 'MAYES COUNTY');
insert into ok911.county_tbl (county, description) values ('MCCLAIN COUNTY', 'MCCLAIN COUNTY');
insert into ok911.county_tbl (county, description) values ('MCCURTAIN COUNTY', 'MCCURTAIN COUNTY');
insert into ok911.county_tbl (county, description) values ('MCINTOSH COUNTY', 'MCINTOSH COUNTY');
insert into ok911.county_tbl (county, description) values ('MURRAY COUNTY', 'MURRAY COUNTY');
insert into ok911.county_tbl (county, description) values ('MUSKOGEE COUNTY', 'MUSKOGEE COUNTY');
insert into ok911.county_tbl (county, description) values ('NOBLE COUNTY', 'NOBLE COUNTY');
insert into ok911.county_tbl (county, description) values ('NOWATA COUNTY', 'NOWATA COUNTY');
insert into ok911.county_tbl (county, description) values ('OKFUSKEE COUNTY', 'OKFUSKEE COUNTY');
insert into ok911.county_tbl (county, description) values ('OKLAHOMA COUNTY', 'OKLAHOMA COUNTY');
insert into ok911.county_tbl (county, description) values ('OKMULGEE COUNTY', 'OKMULGEE COUNTY');
insert into ok911.county_tbl (county, description) values ('OSAGE COUNTY', 'OSAGE COUNTY');
insert into ok911.county_tbl (county, description) values ('OTTAWA COUNTY', 'OTTAWA COUNTY');
insert into ok911.county_tbl (county, description) values ('PAWNEE COUNTY', 'PAWNEE COUNTY');
insert into ok911.county_tbl (county, description) values ('PAYNE COUNTY', 'PAYNE COUNTY');
insert into ok911.county_tbl (county, description) values ('PITTSBURG COUNTY', 'PITTSBURG COUNTY');
insert into ok911.county_tbl (county, description) values ('PONTOTOC COUNTY', 'PONTOTOC COUNTY');
insert into ok911.county_tbl (county, description) values ('POTTAWATOMIE COUNTY',  'POTTAWATOMIE COUNTY');
insert into ok911.county_tbl (county, description) values ('PUSHMATAHA COUNTY', 'PUSHMATAHA COUNTY');
insert into ok911.county_tbl (county, description) values ('ROGER MILLS COUNTY', 'ROGER MILLS COUNTY');
insert into ok911.county_tbl (county, description) values ('ROGERS COUNTY', 'ROGERS COUNTY');
insert into ok911.county_tbl (county, description) values ('SEMINOLE COUNTY', 'SEMINOLE COUNTY');
insert into ok911.county_tbl (county, description) values ('SEQUOYAH COUNTY', 'SEQUOYAH COUNTY');
insert into ok911.county_tbl (county, description) values ('STEPHENS COUNTY', 'STEPHENS COUNTY');
insert into ok911.county_tbl (county, description) values ('TEXAS COUNTY', 'TEXAS COUNTY');
insert into ok911.county_tbl (county, description) values ('TILLMAN COUNTY', 'TILLMAN COUNTY');
insert into ok911.county_tbl (county, description) values ('TULSA COUNTY', 'TULSA COUNTY');
insert into ok911.county_tbl (county, description) values ('WAGONER COUNTY', 'WAGONER COUNTY');
insert into ok911.county_tbl (county, description) values ('WASHINGTON COUNTY', 'WASHINGTON COUNTY');
insert into ok911.county_tbl (county, description) values ('WASHITA COUNTY', 'WASHITA COUNTY');
insert into ok911.county_tbl (county, description) values ('WOODS COUNTY', 'WOODS COUNTY');
insert into ok911.county_tbl (county, description) values ('WOODWARD COUNTY', 'WOODWARD COUNTY');
insert into ok911.county_tbl (county, description) values ('DALLAM COUNTY', 'DALLAM COUNTY');
insert into ok911.county_tbl (county, description) values ('SHERMAN COUNTY', 'SHERMAN COUNTY');
insert into ok911.county_tbl (county, description) values ('HANSFORD COUNTY', 'HANSFORD COUNTY');
insert into ok911.county_tbl (county, description) values ('OCHILTREE COUNTY',  'OCHILTREE COUNTY');
insert into ok911.county_tbl (county, description) values ('LIPSCOMB COUNTY',  'LIPSCOMB COUNTY');
insert into ok911.county_tbl (county, description) values ('HEMPHILL COUNTY',  'HEMPHILL COUNTY');
insert into ok911.county_tbl (county, description) values ('WHEELER COUNTY',  'WHEELER COUNTY');
insert into ok911.county_tbl (county, description) values ('COLLINGSWORTH COUNTY', 'COLLINGSWORTH COUNTY');
insert into ok911.county_tbl (county, description) values ('CHILDRESS COUNTY', 'CHILDRESS COUNTY');
insert into ok911.county_tbl (county, description) values ('HARDEMAN COUNTY',  'HARDEMAN COUNTY');
insert into ok911.county_tbl (county, description) values ('WILBARGER COUNTY', 'WILBARGER COUNTY');
insert into ok911.county_tbl (county, description) values ('WICHITA COUNTY',  'WICHITA COUNTY');
insert into ok911.county_tbl (county, description) values ('CLAY COUNTY',  'CLAY COUNTY');
insert into ok911.county_tbl (county, description) values ('MONTAGUE COUNTY',  'MONTAGUE COUNTY');
insert into ok911.county_tbl (county, description) values ('COOKE COUNTY',  'COOKE COUNTY');
insert into ok911.county_tbl (county, description) values ('GRAYSON COUNTY',  'GRAYSON COUNTY');
insert into ok911.county_tbl (county, description) values ('FANNIN COUNTY',  'FANNIN COUNTY');
insert into ok911.county_tbl (county, description) values ('LAMAR COUNTY',  'LAMAR COUNTY');
insert into ok911.county_tbl (county, description) values ('RED RIVER COUNTY', 'RED RIVER COUNTY');
insert into ok911.county_tbl (county, description) values ('BOWIE COUNTY',  'BOWIE COUNTY');
insert into ok911.county_tbl (county, description) values ('MORTON COUNTY',  'MORTON COUNTY');
insert into ok911.county_tbl (county, description) values ('STEVENS COUNTY',  'STEVENS COUNTY');
insert into ok911.county_tbl (county, description) values ('SEWARD COUNTY', 'SEWARD COUNTY');
insert into ok911.county_tbl (county, description) values ('MEADE COUNTY', 'MEADE COUNTY');
insert into ok911.county_tbl (county, description) values ('CLARK COUNTY', 'CLARK COUNTY');
insert into ok911.county_tbl (county, description) values ('BARBER COUNTY', 'BARBER COUNTY');
insert into ok911.county_tbl (county, description) values ('SUMNER COUNTY', 'SUMNER COUNTY');
insert into ok911.county_tbl (county, description) values ('COWLEY COUNTY', 'COWLEY COUNTY');
insert into ok911.county_tbl (county, description) values ('CHAUTAUQUA COUNTY', 'CHAUTAUQUA COUNTY');
insert into ok911.county_tbl (county, description) values ('MONTGOMERY COUNTY', 'MONTGOMERY COUNTY');
insert into ok911.county_tbl (county, description) values ('LABETTE COUNTY', 'LABETTE COUNTY');
insert into ok911.county_tbl (county, description) values ('BACA COUNTY', 'BACA COUNTY');
insert into ok911.county_tbl (county, description) values ('LAS ANIMAS COUNTY', 'LAS ANIMAS COUNTY');
insert into ok911.county_tbl (county, description) values ('UNION COUNTY', 'UNION COUNTY');
insert into ok911.county_tbl (county, description) values ('BENTON COUNTY', 'BENTON COUNTY');
insert into ok911.county_tbl (county, description) values ('CRAWFORD COUNTY', 'CRAWFORD COUNTY');
insert into ok911.county_tbl (county, description) values ('SEBASTAIN COUNTY', 'SEBASTAIN COUNTY');
insert into ok911.county_tbl (county, description) values ('SCOTT COUNTY', 'SCOTT COUNTY');
insert into ok911.county_tbl (county, description) values ('POLK COUNTY', 'POLK COUNTY');
insert into ok911.county_tbl (county, description) values ('SEVIER COUNTY', 'SEVIER COUNTY');
insert into ok911.county_tbl (county, description) values ('LITTLE RIVER COUNTY', 'LITTLE RIVER COUNTY');
insert into ok911.county_tbl (county, description) values ('MCDONALD COUNTY', 'MCDONALD COUNTY');
insert into ok911.county_tbl (county, description) values ('NEWTON COUNTY', 'NEWTON COUNTY');


DROP TABLE IF EXISTS ok911.roadlevel_tbl; 
create table ok911.roadlevel_tbl ( 
	level varchar(10) primary key,
	description varchar(25)
        ); 

insert into ok911.roadlevel_tbl (level, description) values ('0', 'OVERPASS LEVEL 0');
insert into ok911.roadlevel_tbl (level, description) values ('1', 'OVERPASS LEVEL 1');
insert into ok911.roadlevel_tbl (level, description) values ('2', 'OVERPASS LEVEL 2');
insert into ok911.roadlevel_tbl (level, description) values ('3', 'OVERPASS LEVEL 3');
insert into ok911.roadlevel_tbl (level, description) values ('4', 'OVERPASS LEVEL 4');



DROP TABLE IF EXISTS ok911.placement_tbl; 
create table ok911.placement_tbl ( 
	placement varchar(25) primary key,
	description varchar(25)
        ); 


insert into ok911.placement_tbl (placement, description) values ('0', 'OVERPASS LEVEL 0');
insert into ok911.placement_tbl (placement, description) values ('1', 'OVERPASS LEVEL 1');
insert into ok911.placement_tbl (placement, description) values ('2', 'OVERPASS LEVEL 2');
insert into ok911.placement_tbl (placement, description) values ('3', 'OVERPASS LEVEL 3');
insert into ok911.placement_tbl (placement, description) values ('4', 'OVERPASS LEVEL 4');



DROP TABLE IF EXISTS ok911.parity_tbl; 
create table ok911.parity_tbl ( 
	parity varchar(1) primary key,
	description varchar(6)
        ); 

insert into ok911.parity_tbl (parity, description) values ('O', 'ODD');
insert into ok911.parity_tbl (parity, description) values ('E', 'EVEN');
insert into ok911.parity_tbl (parity, description) values ('B', 'BOTH');
insert into ok911.parity_tbl (parity, description) values ('Z', 'ZERO');


DROP TABLE IF EXISTS ok911.number_tbl; 
create table ok911.number_tbl ( 
	number varchar(5) primary key,
	description varchar(5)
        ); 

insert into ok911.number_tbl (number, description) values ('1', '1');
insert into ok911.number_tbl (number, description) values ('2', '2');
insert into ok911.number_tbl (number, description) values ('3', '3');
insert into ok911.number_tbl (number, description) values ('4', '4');
insert into ok911.number_tbl (number, description) values ('5', '5');
insert into ok911.number_tbl (number, description) values ('6', '6');
insert into ok911.number_tbl (number, description) values ('7', '7');
insert into ok911.number_tbl (number, description) values ('8', '8');
insert into ok911.number_tbl (number, description) values ('9', '9');
insert into ok911.number_tbl (number, description) values ('10', '10');

DROP TABLE IF EXISTS ok911.strmsheltr_tbl; 
create table ok911.strmsheltr_tbl ( 
	strmsheltr varchar(25) primary key,
	description varchar(25)
        ); 

insert into ok911.strmsheltr_tbl (strmsheltr, description) values ('ABOVE GROUND IN STRUCTURE', 'ABOVE GROUND IN STRUCTURE');
insert into ok911.strmsheltr_tbl (strmsheltr, description) values ('ABOVE GROUND OUTSIDE', 'ABOVE GROUND OUTSIDE');
insert into ok911.strmsheltr_tbl (strmsheltr, description) values ('BELOW GROUND IN STRUCTURE', 'BELOW GROUND IN STRUCTURE');
insert into ok911.strmsheltr_tbl (strmsheltr, description) values ('BELOW GROUND OUTSIDE', 'BELOW GROUND OUTSIDE');

DROP TABLE IF EXISTS ok911.state_tbl; 
create table ok911.state_tbl ( 
	state varchar(2) primary key,
	description varchar(12)
        ); 

insert into ok911.state_tbl (state, description) values ('OK', 'OKLAHOMA');
insert into ok911.state_tbl (state, description) values ('TX', 'TEXAS');
insert into ok911.state_tbl (state, description) values ('CO', 'COLORADO');
insert into ok911.state_tbl (state, description) values ('NM', 'NEW MEXICO');
insert into ok911.state_tbl (state, description) values ('AR', 'ARKANSAS');
insert into ok911.state_tbl (state, description) values ('KS', 'KANSAS');
insert into ok911.state_tbl (state, description) values ('MO', 'MISSOURI');


DROP TABLE IF EXISTS ok911.topoexcept_tbl; 
create table ok911.topoexcept_tbl ( 
	topoexcept varchar(20) primary key,
	description varchar(100)
        ); 

insert into ok911.topoexcept_tbl (topoexcept, description) values ('DANGLE_EXCEPTION', 'Feature is an exception to the "Must Not Have Dangles" topology rule');
insert into ok911.topoexcept_tbl (topoexcept, description) values ('INSIDE_EXCEPTION', 'Feature is an exception to the "Must be Inside Discrepancy Agency  Boundary" topology rule');
insert into ok911.topoexcept_tbl (topoexcept, description) values ('BOTH_EXCEPTION', 'Feature is an exception to both topology rules');
insert into ok911.topoexcept_tbl (topoexcept, description) values ('NO_EXCEPTION', 'Feature is not an exception to the topology rules');

DROP TABLE IF EXISTS ok911.yesno_tbl; 
create table ok911.yesno_tbl ( 
	yesno varchar(1) primary key,
	description varchar(1)
        ); 

insert into ok911.yesno_tbl (yesno, description) values ('Y', 'Y');
insert into ok911.yesno_tbl (yesno, description) values ('N', 'N');


DROP TABLE IF EXISTS ok911.serviceurn_tbl; 
create table ok911.serviceurn_tbl ( 
	serviceurn varchar(50) primary key,
	description varchar(50)
        ); 

insert into ok911.serviceurn_tbl (serviceurn, description) values ('urn:nena:service:additionalData', 'urn:nena:service:additionalData');
insert into ok911.serviceurn_tbl (serviceurn, description) values ('urn:nena:service:responder.coast_guard', 'urn:nena:service:responder.coast_guard');
insert into ok911.serviceurn_tbl (serviceurn, description) values ('urn:nena:service:responder.ems', 'urn:nena:service:responder.ems');
insert into ok911.serviceurn_tbl (serviceurn, description) values ('urn:nena:service:responder.federal_police.atf', 'urn:nena:service:responder.federal_police.atf');
insert into ok911.serviceurn_tbl (serviceurn, description) values ('urn:nena:service:responder.federal_police.cbp', 'urn:nena:service:responder.federal_police.cbp');
insert into ok911.serviceurn_tbl (serviceurn, description) values ('urn:nena:service:responder.federal_police.dea', 'urn:nena:service:responder.federal_police.dea');
insert into ok911.serviceurn_tbl (serviceurn, description) values ('urn:nena:service:responder.federal_police.dss', 'urn:nena:service:responder.federal_police.dss');
insert into ok911.serviceurn_tbl (serviceurn, description) values ('urn:nena:service:responder.federal_police.fbi', 'urn:nena:service:responder.federal_police.fbi');
insert into ok911.serviceurn_tbl (serviceurn, description) values ('urn:nena:service:responder.federal_police.fps', 'urn:nena:service:responder.federal_police.fps');
insert into ok911.serviceurn_tbl (serviceurn, description) values ('urn:nena:service:responder.federal_police.ice', 'urn:nena:service:responder.federal_police.ice');
insert into ok911.serviceurn_tbl (serviceurn, description) values ('urn:nena:service:responder.federal_police.marshal', 'urn:nena:service:responder.federal_police.marshal');
insert into ok911.serviceurn_tbl (serviceurn, description) values ('urn:nena:service:responder.federal_police.pp', 'urn:nena:service:responder.federal_police.pp');
insert into ok911.serviceurn_tbl (serviceurn, description) values ('urn:nena:service:responder.federal_police.rcmp', 'urn:nena:service:responder.federal_police.rcmp');
insert into ok911.serviceurn_tbl (serviceurn, description) values ('urn:nena:service:responder.federal_police.usss', 'urn:nena:service:responder.federal_police.usss');
insert into ok911.serviceurn_tbl (serviceurn, description) values ('urn:nena:service:responder.fire', 'urn:nena:service:responder.fire');
insert into ok911.serviceurn_tbl (serviceurn, description) values ('urn:nena:service:responder.mountain_rescue', 'urn:nena:service:responder.mountain_rescue');
insert into ok911.serviceurn_tbl (serviceurn, description) values ('urn:nena:service:responder.poison_control', 'urn:nena:service:responder.poison_control');
insert into ok911.serviceurn_tbl (serviceurn, description) values ('urn:nena:service:responder.police', 'urn:nena:service:responder.police');
insert into ok911.serviceurn_tbl (serviceurn, description) values ('urn:nena:service:responder.psap', 'urn:nena:service:responder.psap');
insert into ok911.serviceurn_tbl (serviceurn, description) values ('urn:nena:service:responder.sheriff', 'urn:nena:service:responder.sheriff');
insert into ok911.serviceurn_tbl (serviceurn, description) values ('urn:nena:service:responder.stateProvincial_police', 'urn:nena:service:responder.stateProvincial_police');
insert into ok911.serviceurn_tbl (serviceurn, description) values ('urn:nena:service:sos.call_taker', 'urn:nena:service:sos.call_taker');
insert into ok911.serviceurn_tbl (serviceurn, description) values ('urn:nena:service:sos.level_2_esrp', 'urn:nena:service:sos.level_2_esrp');
insert into ok911.serviceurn_tbl (serviceurn, description) values ('urn:nena:service:sos.level_3_esrp', 'urn:nena:service:sos.level_3_esrp');
insert into ok911.serviceurn_tbl (serviceurn, description) values ('urn:nena:service:sos.psap', 'urn:nena:service:sos.psap');
insert into ok911.serviceurn_tbl (serviceurn, description) values ('urn:service:sos', 'urn:service:sos');
insert into ok911.serviceurn_tbl (serviceurn, description) values ('urn:service:sos.ambulance', 'urn:service:sos.ambulance');
insert into ok911.serviceurn_tbl (serviceurn, description) values ('urn:service:sos.animal-control', 'urn:service:sos.animal-control');
insert into ok911.serviceurn_tbl (serviceurn, description) values ('urn:service:sos.fire', 'urn:service:sos.fire');
insert into ok911.serviceurn_tbl (serviceurn, description) values ('urn:service:sos.gas', 'urn:service:sos.gas');
insert into ok911.serviceurn_tbl (serviceurn, description) values ('urn:service:sos.marine', 'urn:service:sos.marine');
insert into ok911.serviceurn_tbl (serviceurn, description) values ('urn:service:sos.mountain', 'urn:service:sos.mountain');
insert into ok911.serviceurn_tbl (serviceurn, description) values ('urn:service:sos.physician', 'urn:service:sos.physician');
insert into ok911.serviceurn_tbl (serviceurn, description) values ('urn:service:sos.poison', 'urn:service:sos.poison');
insert into ok911.serviceurn_tbl (serviceurn, description) values ('urn:service:sos.police', 'urn:service:sos.police');


DROP TABLE IF EXISTS ok911.agencyid_tbl; 
create table ok911.agencyid_tbl ( 
	agencyid varchar(100) primary key,
	description varchar(100)
        ); 

insert into ok911.agencyid_tbl (agencyid, description) values ('psap.5578.ok.gov', 'psap.5578.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('psap.5603.ok.gov', 'psap.5603.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('psap.5579.ok.gov', 'psap.5579.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('psap.5585.ok.gov', 'psap.5585.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('cog.acog.ok.gov', 'cog.acog.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('cog.ascog.ok.gov', 'cog.ascog.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('psap.5586.ok.gov', 'psap.5586.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('psap.5589.ok.gov', 'psap.5589.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('psap.5592.ok.gov', 'psap.5592.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('psap.5593.ok.gov', 'psap.5593.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('psap.5594.ok.gov', 'psap.5594.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('psap.5595.ok.gov', 'psap.5595.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('psap.8642.ok.gov', 'psap.8642.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('psap.5596.ok.gov', 'psap.5596.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('psap.5597.ok.gov', 'psap.5597.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('psap.5631.ok.gov', 'psap.5631.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('psap.8328.ok.gov', 'psap.8328.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('cog.coedd.ok.gov', 'cog.coedd.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('psap.8835.ok.gov', 'psap.8835.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('psap.5604.ok.gov', 'psap.5604.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('psap.5608.ok.gov', 'psap.5608.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('psap.5657.ok.gov', 'psap.5657.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('psap.5610.ok.gov', 'psap.5610.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('psap.5616.ok.gov', 'psap.5616.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('psap.5615.ok.gov', 'psap.5615.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('psap.5612.ok.gov', 'psap.5612.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('psap.5617.ok.gov', 'psap.5617.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('psap.5618.ok.gov', 'psap.5618.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('psap.5669.ok.gov', 'psap.5669.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('psap.5622.ok.gov', 'psap.5622.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('psap.5623.ok.gov', 'psap.5623.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('psap.5741.ok.gov', 'psap.5741.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('psap.5625.ok.gov', 'psap.5625.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('psap.5626.ok.gov', 'psap.5626.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('ven.datamark.ok.gov', 'ven.datamark.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('psap.5627.ok.gov', 'psap.5627.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('psap.5628.ok.gov', 'psap.5628.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('psap.5629.ok.gov', 'psap.5629.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('psap.8394.ok.gov', 'psap.8394.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('psap.5630.ok.gov', 'psap.5630.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('cog.eodd.ok.gov', 'cog.eodd.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('psap.5633.ok.gov', 'psap.5633.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('psap.5634.ok.gov', 'psap.5634.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('psap.8134.ok.gov', 'psap.8134.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('psap.5635.ok.gov', 'psap.5635.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('psap.5636.ok.gov', 'psap.5636.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('psap.8274.ok.gov', 'psap.8274.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('ven.geocomm.ok.gov', 'ven.geocomm.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('ven.geotg.ok.gov', 'ven.geotg.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('psap.5643.ok.gov', 'psap.5643.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('psap.5644.ok.gov', 'psap.5644.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('cog.ggeda.ok.gov', 'cog.ggeda.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('psap.5645.ok.gov', 'psap.5645.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('psap.5646.ok.gov', 'psap.5646.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('psap.5647.ok.gov', 'psap.5647.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('psap.5648.ok.gov', 'psap.5648.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('psap.5650.ok.gov', 'psap.5650.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('psap.8406.ok.gov', 'psap.8406.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('psap.5652.ok.gov', 'psap.5652.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('psap.5653.ok.gov', 'psap.5653.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('psap.5655.ok.gov', 'psap.5655.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('psap.5654.ok.gov', 'psap.5654.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('cog.incog.ok.gov', 'cog.incog.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('ven.intrado.ok.gov', 'ven.intrado.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('psap.5659.ok.gov', 'psap.5659.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('psap.5661.ok.gov', 'psap.5661.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('psap.5662.ok.gov', 'psap.5662.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('cog.keddo.ok.gov', 'cog.keddo.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('psap.8417.ok.gov', 'psap.8417.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('psap.5667.ok.gov', 'psap.5667.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('psap.5670.ok.gov', 'psap.5670.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('psap.8215.ok.gov', 'psap.8215.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('psap.8331.ok.gov', 'psap.8331.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('psap.5639.ok.gov', 'psap.5639.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('psap.5673.ok.gov', 'psap.5673.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('psap.8288.ok.gov', 'psap.8288.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('psap.5674.ok.gov', 'psap.5674.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('psap.8180.ok.gov', 'psap.8180.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('psap.8097.ok.gov', 'psap.8097.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('psap.5613.ok.gov', 'psap.5613.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('psap.8334.ok.gov', 'psap.8334.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('psap.5679.ok.gov', 'psap.5679.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('psap.5680.ok.gov', 'psap.5680.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('psap.5682.ok.gov', 'psap.5682.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('psap.5684.ok.gov', 'psap.5684.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('psap.5685.ok.gov', 'psap.5685.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('psap.5686.ok.gov', 'psap.5686.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('psap.5687.ok.gov', 'psap.5687.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('psap.5689.ok.gov', 'psap.5689.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('psap.5688.ok.gov', 'psap.5688.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('psap.5690.ok.gov', 'psap.5690.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('cog.noda.ok.gov', 'cog.noda.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('psap.5691.ok.gov', 'psap.5691.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('psap.5692.ok.gov', 'psap.5692.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('psap.5693.ok.gov', 'psap.5693.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('psap.5694.ok.gov', 'psap.5694.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('cog.oeda.ok.gov', 'cog.oeda.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('psap.5697.ok.gov', 'psap.5697.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('psap.5698.ok.gov', 'psap.5698.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('psap.5700.ok.gov', 'psap.5700.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('psap.5678.ok.gov', 'psap.5678.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('psap.5705.ok.gov', 'psap.5705.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('psap.5708.ok.gov', 'psap.5708.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('psap.5710.ok.gov', 'psap.5710.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('psap.5676.ok.gov', 'psap.5676.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('psap.5713.ok.gov', 'psap.5713.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('psap.5714.ok.gov', 'psap.5714.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('psap.5577.ok.gov', 'psap.5577.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('psap.8183.ok.gov', 'psap.8183.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('psap.5719.ok.gov', 'psap.5719.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('psap.5720.ok.gov', 'psap.5720.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('ven.rsdigital.ok.gov', 'ven.rsdigital.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('psap.5721.ok.gov', 'psap.5721.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('psap.5722.ok.gov', 'psap.5722.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('psap.5725.ok.gov', 'psap.5725.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('psap.5726.ok.gov', 'psap.5726.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('psap.5727.ok.gov', 'psap.5727.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('psap.8145.ok.gov', 'psap.8145.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('psap.5729.ok.gov', 'psap.5729.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('psap.5730.ok.gov', 'psap.5730.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('psap.5732.ok.gov', 'psap.5732.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('cog.swoda.ok.gov', 'cog.swoda.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('cog.soda.ok.gov', 'cog.soda.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('ven.sdr.ok.gov', 'ven.sdr.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('psap.5733.ok.gov', 'psap.5733.ok.go');
insert into ok911.agencyid_tbl (agencyid, description) values ('psap.5734.ok.gov', 'psap.5734.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('psap.8614.ok.gov', 'psap.8614.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('psap.5736.ok.gov', 'psap.5736.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('psap.5640.ok.gov', 'psap.5640.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('psap.5737.ok.gov', 'psap.5737.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('psap.8550.ok.gov', 'psap.8550.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('psap.5738.ok.gov', 'psap.5738.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('psap.5739.ok.gov', 'psap.5739.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('psap.5740.ok.gov', 'psap.5740.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('psap.8397.ok.gov', 'psap.8397.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('psap.5742.ok.gov', 'psap.5742.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('psap.8408.ok.gov', 'psap.8408.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('psap.5743.ok.gov', 'psap.5743.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('psap.5588.ok.gov', 'psap.5588.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('psap.5621.ok.gov', 'psap.5621.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('psap.5744.ok.gov', 'psap.5744.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('psap.5581.ok.gov', 'psap.5581.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('psap.5746.ok.gov', 'psap.5746.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('psap.8529.ok.gov', 'psap.8529.ok.gov');
insert into ok911.agencyid_tbl (agencyid, description) values ('psap.5749.ok.gov', 'psap.5749.ok.gov');



DROP TABLE IF EXISTS ok911.country_tbl; 
create table ok911.country_tbl ( 
	country varchar(100) primary key,
	description varchar(100)
        ); 

insert into ok911.country_tbl (country, description) values ('US', 'UNITED STATES OF AMERICA')
