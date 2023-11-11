# pyright: reportPrivateUsage=false

import pytest
from pytest_mock import MockerFixture

from src.exceptions import ValidationError
from src.storages.usecases import StorageCreateUseCase


@pytest.fixture(autouse=True)
def necessary_mocks(mocker: MockerFixture, usecase: StorageCreateUseCase) -> None:
    mocker.patch.object(usecase, "_is_correct_storage_link_format", return_value=True)
    mocker.patch.object(usecase._storage_repo, "is_accessable", return_value=True)


class TestValidatingStorageLinkFormat:
    async def test__is_correct_storage_link_format_called(
        self,
        usecase: StorageCreateUseCase,
        mocker: MockerFixture,
    ) -> None:
        link = "https://www.fake_storage.com/123456789"
        spy = mocker.spy(usecase, "_is_correct_storage_link_format")

        await usecase._validate_expenses_table_link(link=link)

        spy.assert_called_once_with(link=link)

    async def test_error_if_storage_link_is_invalid(self, usecase: StorageCreateUseCase, mocker: MockerFixture) -> None:
        mocker.patch.object(usecase, "_is_correct_storage_link_format", return_value=False)

        with pytest.raises(ValidationError, match="expenses_table_link: Invalid link to Expenses table") as exc:
            await usecase._validate_expenses_table_link(link="https://www.fake_storage.com/123456789")
        assert exc.value.field == "expenses_table_link"
        assert exc.value.error == "Invalid link to Expenses table"

    async def test_no_error_if_storage_link_is_valid(
        self,
        usecase: StorageCreateUseCase,
        mocker: MockerFixture,
    ) -> None:
        mocker.patch.object(usecase, "_is_correct_storage_link_format", return_value=True)

        try:
            await usecase._validate_expenses_table_link(link="https://www.fake_storage.com/123456789")
        except Exception as e:
            pytest.fail(f"Unexpected exception raised: {e}")


class TestCheckingTableAccessabilityByLink:
    async def test_storage_repo_exists_called(self, usecase: StorageCreateUseCase, mocker: MockerFixture) -> None:
        link = "https://www.fake_storage.com/123456789"
        spy = mocker.spy(usecase._storage_repo, "is_accessable")

        await usecase._validate_expenses_table_link(link=link)

        spy.assert_called_once_with(link=link)

    async def test_error_if_link_is_not_accessable(self, usecase: StorageCreateUseCase, mocker: MockerFixture) -> None:
        mocker.patch.object(usecase._storage_repo, "is_accessable", return_value=False)

        with pytest.raises(ValidationError, match="expenses_table_link: Expenses table is not accessable") as exc:
            await usecase._validate_expenses_table_link(link="https://www.fake_storage.com/123456789")
        assert exc.value.field == "expenses_table_link"
        assert exc.value.error == "Expenses table is not accessable"

    async def test_no_error_if_link_is_accessable(self, usecase: StorageCreateUseCase, mocker: MockerFixture) -> None:
        mocker.patch.object(usecase._storage_repo, "is_accessable", return_value=True)

        try:
            await usecase._validate_expenses_table_link(link="https://www.fake_storage.com/123456789")
        except Exception as e:
            pytest.fail(f"Unexpected exception raised: {e}")
