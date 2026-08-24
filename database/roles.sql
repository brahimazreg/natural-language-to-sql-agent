-- ============================================
-- Read-only role for the NL2SQL application
-- ============================================

CREATE ROLE nl2sql_agent
WITH LOGIN
PASSWORD 'nl2sql_agent_password';

GRANT CONNECT ON DATABASE nl2sql TO nl2sql_agent;

GRANT USAGE ON SCHEMA public TO nl2sql_agent;

GRANT SELECT ON ALL TABLES IN SCHEMA public
TO nl2sql_agent;

ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT SELECT ON TABLES TO nl2sql_agent;