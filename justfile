test-all:
  pytest tests

create-migration NAME:
  dotenv -f databases/postgresql/migrations/.env run -- dbmate new {{NAME}}

migrate:
  dotenv -f databases/postgresql/migrations/.env run -- dbmate up

rollback-migration:
  dotenv -f databases/postgresql/migrations/.env run -- dbmate down

up-test-env:
   dotenv -f envs/test.env run -- dbmate --env-file ".dbmate.env" up

drop-test-env:
   dotenv -f envs/test.env run -- dbmate --env-file ".dbmate.env" drop
