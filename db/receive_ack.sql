use [sandbox];
go

declare @ch uniqueidentifier;
declare @mb xml;
declare @mt sysname;

begin transaction;

receive top(1)
	@ch = conversation_handle,
	@mb = message_body,
	@mt = message_type_name
from [test_initiator_q];

end conversation @ch;

select @mb as [ack]

commit;
