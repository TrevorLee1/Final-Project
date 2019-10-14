/* Use the below query to grant a user admin access, replacing 'test' with
their username */

UPDATE "users" SET "admin" = 'true' WHERE "username" = 'test'
