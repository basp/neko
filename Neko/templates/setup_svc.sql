BEGIN TRY
	BEGIN TRANSACTION;

	CREATE QUEUE [:initiator_q] 
		WITH STATUS = ON;
	
	CREATE QUEUE [:target_q] 
		WITH STATUS = ON;

	CREATE SERVICE [:initiator_svc] 
		ON QUEUE [:initiator_q] ([//neko/contract]);	
	
	CREATE SERVICE [:target_svc]
		ON QUEUE [:target_q] ([//neko/contract]);

	COMMIT;
END TRY
BEGIN CATCH
	ROLLBACK TRANSACTION;
	
	SELECT 
		ERROR_NUMBER() AS err_num, 
		ERROR_MESSAGE() AS err_msg
END CATCH