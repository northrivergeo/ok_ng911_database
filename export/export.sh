#!/bin/bash 
gdal vector -f OpenFileGDB -append /mnt/local_projects/tn_duncan/esri_geodatabase/ok_ng911.gdb -nln "ADDRESS_POINT" PG:"host=134.199.193.53 port=5432 user='rjhale' password='9wikufi6' dbname='duncan'" -sql "select * from ok911.address_point where submit = 'Y'"

gdal vector -f OpenFileGDB -append /mnt/local_projects/tn_duncan/esri_geodatabase/ok_ng911.gdb -nln "ROAD_CENTELINE" PG:"host=134.199.193.53 port=5432 user='rjhale' password='9wikufi6' dbname='duncan'" -sql "select * from ok911.road_centerline where submit = 'Y'"

gdal vector -f OpenFileGDB -append /mnt/local_projects/tn_duncan/esri_geodatabase/ok_ng911.gdb -nln "DISCREPANCYAGENCY_BOUNDARY" PG:"host=134.199.193.53 port=5432 user='rjhale' password='9wikufi6' dbname='duncan'" -sql "select * from ok911.discrepancyagency_boundary where submit = 'Y'"

gdal vector -f OpenFileGDB -append /mnt/local_projects/tn_duncan/esri_geodatabase/ok_ng911.gdb -nln "PSAP_BOUNDARY" PG:"host=134.199.193.53 port=5432 user='rjhale' password='9wikufi6' dbname='duncan'" -sql "select * from ok911.psap_boundary where submit = 'Y'"

gdal vector -f OpenFileGDB -append /mnt/local_projects/tn_duncan/esri_geodatabase/ok_ng911.gdb -nln "ESZ_BOUNDARY" PG:"host=134.199.193.53 port=5432 user='rjhale' password='9wikufi6' dbname='duncan'" -sql "select * from ok911.esz_boundary where submit = 'Y'"

gdal vector -f OpenFileGDB -append /mnt/local_projects/tn_duncan/esri_geodatabase/ok_ng911.gdb -nln "ESB_EMS_BOUNDARY" PG:"host=134.199.193.53 port=5432 user='rjhale' password='9wikufi6' dbname='duncan'" -sql "select * from ok911.esb_ems_boundary where submit = 'Y'"

gdal vector -f OpenFileGDB -append /mnt/local_projects/tn_duncan/esri_geodatabase/ok_ng911.gdb -nln "ESB_FIRE_BOUNDARY" PG:"host=134.199.193.53 port=5432 user='rjhale' password='9wikufi6' dbname='duncan'" -sql "select * from ok911.esb_fire_boundary where submit = 'Y'"

gdal vector -f OpenFileGDB -append /mnt/local_projects/tn_duncan/esri_geodatabase/ok_ng911.gdb -nln "ESB_LAW_BOUNDARY" PG:"host=134.199.193.53 port=5432 user='rjhale' password='9wikufi6' dbname='duncan'" -sql "select * from ok911.esb_law_boundary where submit = 'Y'"
