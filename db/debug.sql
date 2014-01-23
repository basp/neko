use [sandbox];
go

select * from [test_target_q];
select * from [test_initiator_q];
select * from sys.conversation_endpoints