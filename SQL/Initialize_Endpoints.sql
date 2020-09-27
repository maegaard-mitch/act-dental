-- initialize endpoints table
insert into endpoints (endpoint_nme, start_nbr, insert_dtm, update_dtm) values
	('deals', 0, current_timestamp, current_timestamp),
	('users', 0, current_timestamp, current_timestamp),
	('organizations', 0, current_timestamp, current_timestamp),
	('persons', 0, current_timestamp, current_timestamp),
	('pipelines', 0, current_timestamp, current_timestamp),
	('stages', 0, current_timestamp, current_timestamp)
;

select * from endpoints;