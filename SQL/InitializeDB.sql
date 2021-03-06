drop table if exists endpoints;
drop table if exists pipelines cascade;
drop table if exists stages cascade;
drop table if exists employees cascade;
drop table if exists organizations cascade;
drop table if exists persons cascade;
drop table if exists deals cascade;


create table if not exists endpoints (
	endpoint_id serial primary key,
	endpoint_nme varchar(100) not null,
	start_nbr int,
	insert_dtm timestamp,
	update_dtm timestamp
);

-- endpoint = pipelines
create table if not exists pipelines (
	pipeline_id int primary  key, -- id
	pipeline_nme varchar(100) not null, -- name
	order_nbr int, -- order_nr
	active_ind boolean, -- active
	insert_dtm timestamp, -- add_time
	update_dtm timestamp -- update_time
);

-- endpoint = stages
create table if not exists stages (
	stage_id int primary key, -- id
	order_nbr int, -- order_nr
	stage_nme varchar(100), -- name
	pipeline_id int references pipelines (pipeline_id), -- pipeline_id
	rotten_ind boolean, -- rotten_flag
	rotten_nbr int, -- rotten_days
	active_ind boolean, -- active_flag
	insert_dtm timestamp, -- add_time
	update_dtm timestamp -- update_time
);

-- endpoint = users
create table if not exists employees (
	employee_id int primary key, -- id
	full_nme varchar(100) not null, -- name
	email_addr varchar(100), -- email
	active_ind boolean, -- active_flag
	insert_dtm timestamp, -- created
	update_dtm timestamp -- modified
);

-- endpoint = organizations
create table if not exists organizations (
	organization_id int primary key, -- id
	organization_nme varchar(100), -- name
	owner_id int references employees (employee_id), -- owner_id.id
	organization_addr varchar(100), -- address
	active_ind boolean, -- active_flag
	insert_dtm timestamp, -- add_time
	update_dtm timestamp -- update_time
);

-- endpoint = persons
create table if not exists persons (
	person_id int primary key, -- id
	owner_id int references employees (employee_id), -- owner_id.id
	organization_id int references organizations (organization_id), -- org_id
	first_nme varchar(100), -- first_name
	last_nme varchar(100), -- last_name
	active_ind boolean, -- active_flag
	insert_dtm timestamp, -- add_time
	update_dtm timestamp -- update_time
);

-- endpoint = deals
create table if not exists deals (
	deal_id int primary key, -- id
	creator_id int references employees (employee_id), -- creator_user_id.id
	owner_id int references employees (employee_id), -- user_id.id
	organization_id int references organizations (organization_id), -- org_id.value
	stage_id int references stages (stage_id), -- stage_id
	deal_nme varchar(250), -- title
	deal_amt numeric(9,2), -- value
	stagechange_dtm timestamp, -- stage_change_time
	status_dsc varchar(100), -- status
	close_dtm timestamp, -- close_time
	lost_dsc varchar(250), -- lost_reason
	email_cnt int, -- email_messages_count
	activity_cnt int, -- activities_count
	active_ind boolean, -- active
	insert_dtm timestamp, -- add_time
	update_dtm timestamp -- update_time
);

-- create stub records to satisfy foreign key constraints
insert into employees values (-1,'Stub Record','',True,current_timestamp,current_timestamp);
insert into organizations values (-1,'',-1,'',True,current_timestamp,current_timestamp);
insert into pipelines values (-1,'Stub Record',-1,true,current_timestamp,current_timestamp);
insert into stages values (0,-1,'Stub Record',-1,false,-1,true,current_timestamp,current_timestamp);

-- initialize endpoints table
insert into endpoints (endpoint_nme, start_nbr, insert_dtm, update_dtm) values
	('deals', 0, current_timestamp, current_timestamp),
	('users', 0, current_timestamp, current_timestamp),
	('organizations', 0, current_timestamp, current_timestamp),
	('persons', 0, current_timestamp, current_timestamp),
	('pipelines', 0, current_timestamp, current_timestamp),
	('stages', 0, current_timestamp, current_timestamp)
;