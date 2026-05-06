select
  nguid_add
from
  ok911.address_point
where
  submit = 'Y' and nguid_add is NULL;
