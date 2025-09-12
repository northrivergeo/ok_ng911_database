-----address_point

create table pontotoc.address_point (
    id serial primary key,
    geom geometry (point, 4326),
        discrpagid varchar(75) references pontotoc.agencyid_tbl(agencyid),
        revdate timestamp,
        reveditor varchar(75),
        effectdate timestamp,
        expiredate timestamp,
        nguid_add varchar(254),
        country varchar(2) references pontotoc.country_tbl(country),
        state  varchar(2) references pontotoc.state_tbl(state),
        county varchar(40) references pontotoc.county_tbl(county),
        city varchar(100),
        addpre varchar(15),
        stnum bigint,
        addsuf varchar(15),
        predir varchar(9) references pontotoc.predir_tbl(predir),
        premod varchar(15),
        pretype varchar(50) references pontotoc.type_tbl(type),
        pretypesep varchar(20) references pontotoc.separator_tbl(pretypesep),
        street varchar(60),
        streettype varchar(50) references pontotoc.type_tbl(type),
        sufdir varchar(9) references pontotoc.predir_tbl(predir),
        sufmod varchar(25),
        esn varchar(5),
        msagcomm varchar(30),
        postcomm varchar(40),
        zipcode varchar(7),
        zipcode4 varchar(4),
        bldgname varchar(75),
        floor varchar(75),
        bldgunit varchar(75),
        room varchar(75),
        seat varchar(75),
        landmkname varchar(150),
        addtnlloc varchar(225),
        placetype varchar(50) references pontotoc.placetype_tbl(placetype),
        longitude double precision,
        latitude double precision,
        elevation smallint,
        label varchar(50),
        milepost varchar(150),
        adddatauri varchar(254),
        uninccomm varchar(100),
        submit varchar(1) references pontotoc.yesno_tbl(yesno),
        comment varchar(100),
        rclmatch varchar(254),
        rclside varchar(1) references pontotoc.rclside_tbl(rclside),
        nbrhdcomm varchar(100),        grpquarter varchar(1) references pontotoc.yesno_tbl(yesno),
        occuptime varchar(50),
        strmsheltr varchar(25) references pontotoc.strmsheltr_tbl(strmsheltr),
        basement varchar(1) references pontotoc.yesno_tbl(yesno),
        lgcyadd varchar(100),
        lgcypredir varchar(2) references pontotoc.lgcypredir_tbl(lgcypredir),
        lgcystreet varchar(75),
        lgcytype varchar(4) references pontotoc.lgcytype_tbl(type),
        lgcysufdir varchar(2) references pontotoc.lgcypredir_tbl(lgcypredir),
        fulladdr varchar(100),
        fullname varchar(50),
        psap varchar(25),
        placement varchar(25) references pontotoc.placement_tbl(placement),
        initisrce varchar(75),
        initidate timestamp,
        agency_id varchar(100) references pontotoc.agencyid_tbl(agencyid)
        );

ALTER TABLE pontotoc.address_point ADD COLUMN structures BIGINT;
ALTER TABLE pontotoc.address_point ADD COLUMN road VARCHAR(20);
ALTER TABLE pontotoc.address_point ADD COLUMN name_road VARCHAR(30);
ALTER TABLE pontotoc.address_point ADD COLUMN z11_addres BIGINT;
ALTER TABLE pontotoc.address_point ADD COLUMN comments VARCHAR(100);
ALTER TABLE pontotoc.address_point ADD COLUMN apart_num VARCHAR(50);
ALTER TABLE pontotoc.address_point ADD COLUMN struc_sear VARCHAR(50);
ALTER TABLE pontotoc.address_point ADD COLUMN community VARCHAR(50);
ALTER TABLE pontotoc.address_point ADD COLUMN address VARCHAR(100);
ALTER TABLE pontotoc.address_point ADD COLUMN editor VARCHAR(25);
ALTER TABLE pontotoc.address_point ADD COLUMN zip_code VARCHAR(25);
ALTER TABLE pontotoc.address_point ADD COLUMN e911_addre VARCHAR(25);
ALTER TABLE pontotoc.address_point ADD COLUMN address_pr VARCHAR(5);
ALTER TABLE pontotoc.address_point ADD COLUMN problem_no VARCHAR(100);

