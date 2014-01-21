USE master;
GO

CREATE DATABASE neko;
GO

-- If this takes forever to finish, some connection to the database
-- is still active. The SET ENABLE_BROKER needs exclusive access to
-- the database so any active connections will block it.
ALTER DATABASE neko SET ENABLE_BROKER;
GO