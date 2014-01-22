USE [:database];

DECLARE @ch UNIQUEIDENTIFIER
DECLARE @message_body XML;

BEGIN TRY
	BEGIN TRANSACTION;

	RECEIVE TOP(:n) 
		@ch = conversation_handle,
		@message_body = CAST(message_body AS XML)
	FROM [:queue];

	IF (@@ROWCOUNT > 0) 
		SELECT @message_body;

	COMMIT;
END TRY
BEGIN CATCH
	ROLLBACK TRANSACTION;
	
	SELECT 
		ERROR_NUMBER() AS err_num, 
		ERROR_MESSAGE() AS err_msg
END CATCH