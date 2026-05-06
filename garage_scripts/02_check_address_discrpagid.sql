select
  nguid_add,
  discrpagid   
from
  ok911.address_point
where
  submit = 'Y' and discrpagid is NULL;
