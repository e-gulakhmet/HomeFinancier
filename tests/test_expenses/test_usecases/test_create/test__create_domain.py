# pyright: reportPrivateUsage=false

from src.expenses.entities import Expense
from src.expenses.usecases import ExpenseCreateInput, ExpenseCreateUseCase
from src.storages.entities import Storage


async def test_domain_entity_is_created(
    usecase: ExpenseCreateUseCase,
    input_: ExpenseCreateInput,
    storage: Storage,
) -> None:
    expense = usecase._create_domain(input_=input_, storage=storage)

    assert isinstance(expense, Expense)
    assert expense.amount == input_.amount
    assert expense.category == input_.category
    assert expense.subcategory == input_.subcategory
    assert expense.user_id == input_.user_id
    assert expense.exepenses_storage_link == storage.expenses_table_link
    assert expense.created_at == input_.created_at
