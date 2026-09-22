-- One-time seed for the admin accounts. Run with:
--   npx wrangler d1 execute timetracker --remote --file=seed-admins.sql
-- Existing rows (same email) keep their id and data; password/role/verified are updated.
-- Hashes are PBKDF2-SHA256, 100k iterations — the same format worker.js produces.

INSERT INTO users (id, email, name, password, role, created_at, verified)
VALUES
  (lower(hex(randomblob(16))), 'eddie.wdr@gmail.com', 'Eddie',
   'pbkdf2$100000$MAIAjJgoSkBEpPqtyJBdWA==$CJKcnwl8XxPKkz60dxypweaayZb+FrYXtaQK+o4W1mk=',
   'admin', strftime('%Y-%m-%dT%H:%M:%SZ','now'), 1),
  (lower(hex(randomblob(16))), 'artush22@icloud.com', 'Artush',
   'pbkdf2$100000$Uirruwez4m9sQIOOP+gMog==$ciaqtJdGNLlfqOy/cgw/9tE5hut3nBaxk+50UjHvs08=',
   'admin', strftime('%Y-%m-%dT%H:%M:%SZ','now'), 1),
  (lower(hex(randomblob(16))), 'elliot@westrosdigitalretail.se', 'Elliot',
   'pbkdf2$100000$6RF8Ra2J8Qaly/iXWwcqMQ==$IgnV3KipYtAwYX8s1dIPcPUnhwY2VHQQLyXK9wkLFBQ=',
   'admin', strftime('%Y-%m-%dT%H:%M:%SZ','now'), 1)
ON CONFLICT(email) DO UPDATE SET
  password = excluded.password,
  role = 'admin',
  verified = 1,
  verify_code = NULL,
  code_expires = NULL;

-- Everyone else is a regular member.
UPDATE users SET role = 'user'
WHERE email NOT IN ('eddie.wdr@gmail.com', 'artush22@icloud.com', 'elliot@westrosdigitalretail.se');
