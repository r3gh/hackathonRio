CREATE SEQUENCE violence_data_seq
    INCREMENT 1
    MINVALUE 1
    MAXVALUE 9223372036854775807
    START 1
    CACHE 1;

CREATE TABLE violence_data(
  id integer NOT NULL DEFAULT nextval('violence_data_seq'),
  title varchar(255),
  description TEXT,
  latitude numeric,
  longitude numeric, 
  type_violence numeric,
  event_data timestamp,
  address varchar(255),
  icon varchar(255),
  county varchar(255),
  email varchar(255),
  name varchar(255),
  bulletin_occurrence varchar(255),
  damage_value numeric,
  neighborhood varchar(255),
  sex varchar(40),
  source varchar(40)
);