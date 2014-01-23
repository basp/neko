use [sandbox];
go

declare @ch uniqueidentifier;
declare @mb xml
declare @mt sysname;

begin transaction;

receive top(1)
	@ch = conversation_handle,
	@mb = cast(message_body as xml),
	@mt = message_type_name
from [test_target_q];

if @mt = N'//neko/request'
begin
	declare @ack nvarchar(max) = '<response>ack</response>';
	send on conversation @ch message type [//neko/response] (@ack);
	end conversation @ch;
end

commit;
