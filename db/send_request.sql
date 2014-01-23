use [sandbox];
go

declare @ch uniqueidentifier;

begin transaction;

begin dialog @ch 
	from service [test_initiator_svc]
	to service 'test_target_svc'
	on contract [//neko/contract]
	with encryption = off;

declare @msg nvarchar(max) = '<request>sample request</request>';
send on conversation @ch message type [//neko/request] (@msg);

commit;