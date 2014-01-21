USE neko;
GO

CREATE MESSAGE TYPE [http://github.com/basp/neko/Request]
	VALIDATION = NONE;
CREATE MESSAGE TYPE [http://github.com/basp/neko/Response]
	VALIDATION = NONE;
GO

CREATE CONTRACT [http://github.com/basp/neko/HelloWorldContract]
(
	[http://github.com/basp/neko/Request] SENT BY INITIATOR,
	[http://github.com/basp/neko/Response] SENT BY TARGET
);
GO

CREATE QUEUE InitiatorQueue WITH STATUS = ON;
CREATE QUEUE TargetQueue WITH STATUS = ON;
GO

CREATE SERVICE InitiatorService ON QUEUE InitiatorQueue 
(
	[http://github.com/basp/neko/HelloWorldContract]
);
GO

CREATE SERVICE TargetService ON QUEUE TargetQueue 
(
	[http://github.com/basp/neko/HelloWorldContract]
);
GO

DECLARE @ch UNIQUEIDENTIFIER
DECLARE @msg NVARCHAR(128)

BEGIN DIALOG CONVERSATION @ch
	FROM SERVICE InitiatorService TO SERVICE 'TargetService'
	ON CONTRACT [http://github.com/basp/neko/HelloWorldContract]
	WITH ENCRYPTION = OFF;

SET @msg = N'foo bar quux';

SEND ON CONVERSATION @ch 
MESSAGE TYPE [http://github.com/basp/neko/Request] (@msg);
GO