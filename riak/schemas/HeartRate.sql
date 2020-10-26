CREATE TABLE HeartRate
(
   user_id          VARCHAR   NOT NULL,
   time             TIMESTAMP NOT NULL,
   value            DOUBLE,
   PRIMARY KEY (
     (user_id, QUANTUM(time, 1, 'm')),
      user_id, time
   )
)
