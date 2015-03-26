CREATE TABLE ratings
(
recordid serial primary key,
userid int ,
movieid int,
rate numeric(1,1),
ratingtime int
)
