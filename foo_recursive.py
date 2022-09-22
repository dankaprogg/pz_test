from sqlalchemy import literal
from sqlalchemy import null
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Query
from sqlalchemy.orm import aliased
from sqlalchemy.sql.schema import Column

from db.models import Foo


async def foo_recursive(
    session: AsyncSession,
    depth: int,
    sort_fld: Column,
    root_id: str = None,
):
    hierarchy = Query(Foo).add_columns(literal(0).label('level'))

    if root_id:
        hierarchy = hierarchy.filter(Foo.parent_id == root_id)
    else:
        hierarchy = hierarchy.filter(Foo.parent_id == null())

    hierarchy = hierarchy.cte(name="hierarchy", recursive=True)

    parent = aliased(hierarchy, name="p")
    children = aliased(Foo, name="c")
    hierarchy = hierarchy.union_all(
        Query(children).add_columns((parent.c.level + 1).label("level"))
            .filter(children.parent_id == parent.c.id)
            .filter(parent.c.level < depth)
    )

    stmt = Query(
        Foo,
        hierarchy.c.level
    ).select_entity_from(hierarchy)

    async with session as transaction:
        result = await transaction.execute(stmt)

    result = result.all()

    return result
