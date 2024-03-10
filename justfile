test-all:
  pytest tests

create-migration NAME:
  dotenv -f envs/dev.env run -- dbmate --env-file ".dbmate.env" new {{NAME}}

migrate:
  dotenv -f envs/dev.env run -- dbmate --env-file ".dbmate.env" up

rollback-migration:
  dotenv -f envs/dev.env run -- dbmate --env-file ".dbmate.env" down

up-test-env:
  dotenv -f envs/test.env run -- dbmate --env-file ".dbmate.env" up

drop-test-env:
  dotenv -f envs/test.env run -- dbmate --env-file ".dbmate.env" drop
