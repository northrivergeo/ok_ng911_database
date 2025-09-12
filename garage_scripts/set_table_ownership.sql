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

