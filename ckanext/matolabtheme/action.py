import ckan.plugins.toolkit as toolkit

if toolkit.check_ckan_version("2.10"):
    from ckan.types import Context
else:

    class Context(dict):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)


from typing import Any
from sqlalchemy import Table, select, func, and_, false
import ckan.model as model


def table(name: str):
    return Table(name, model.meta.metadata, autoload_with=model.meta.engine)


# Function to serialize SQLAlchemy result
def serialize_row(row):
    return {column: getattr(row, column) for column in row._mapping}


@toolkit.side_effect_free
def theme_stats(context: Context, data_dict: dict[str, Any]) -> dict[str, Any]:
    package = table("package")
    resource = table("resource")
    session = model.Session
    s = (
        select(
            package.c["owner_org"],
            func.count(package.c["id"]).label("count"),
        )
        .group_by(package.c["owner_org"])
        .where(
            and_(
                package.c["owner_org"].isnot(None),
                package.c["private"] == false(),
                package.c["state"] == "active",
            )
        )
        .order_by(func.count(package.c["id"]).desc())
        # .limit(limit)
    )
    conn: Any = model.Session.connection()
    # cursor = conn.execute(q)

    org_rows = conn.execute(s).fetchall()
    s = select(
        func.count(resource.c["id"]),
    ).where(
        and_(
            resource.c["state"] != "deleted",
        )
    )
    res_rows = conn.execute(s).fetchall()
    orgs = [serialize_row(row) for row in org_rows]
    org_count = len(orgs)
    pkg_sum = sum([org.get("count", 0) for org in orgs])
    res = res_rows[0]["count_1"] if len(res_rows) > 0 else None
    # res_count = len(model.Package().resources)
    return {
        "orgs": orgs,
        "pkg_count": pkg_sum,
        "res_count": res,
        "org_count": org_count,
    }


def get_actions():
    actions = {"matolabtheme_stats": theme_stats}
    return actions
