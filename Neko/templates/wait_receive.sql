USE [:database];

DECLARE @ch UNIQUEIDENTIFIER
DECLARE @bd XML;

BEGIN TRY
	BEGIN TRANSACTION;

	WAITFOR (
		RECEIVE TOP(:n) 
			@ch = conversation_handle,
			@bd = CAST(message_body AS XML)
		FROM [:queue]
	)

	IF (@@ROWCOUNT > 0) 
		SELECT @bd;

	COMMIT;
END TRY
BEGIN CATCH
	ROLLBACK TRANSACTION;

	SELECT 
		ERROR_NUMBER() AS err_num, 
		ERROR_MESSAGE() AS err_msg
END CATCH