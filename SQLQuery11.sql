SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
-- =============================================
-- Author:		Bas Pennings
-- Create date: 21-01-2014
-- Description:	Creates a Neko event queue.
-- =============================================
CREATE PROCEDURE dbo.create_event_queue
	@name NVARCHAR(MAX)
AS
BEGIN
	-- SET NOCOUNT ON added to prevent extra result sets from
	-- interfering with SELECT statements.
	SET NOCOUNT ON;

    -- Insert statements for procedure here
	CREATE QUEUE @name WITH STATUS = ON
END
GO
