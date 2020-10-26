CREATE TABLE HeartRate
(
   id           SINT64    NOT NULL,
   time         TIMESTAMP NOT NULL,
   value  DOUBLE,
   PRIMARY KEY (
     (id, QUANTUM(time, 1, 'm')),
      id, time
   )
)
