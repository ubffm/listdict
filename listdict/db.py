import sqlalchemy as sa


def mktable(
    name: str, metadata: sa.MetaData, parent: str = None, valuetype: type = None
) -> sa.Table:
    columns = [
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("key", sa.String),
    ]
    if valuetype:
        columns.append(sa.Column("value", valuetype))
    if parent:
        columns.append(sa.Column("parent", None, sa.ForeignKey(parent + ".id")))
    return sa.Table(name, metadata, *columns)


class ListDictDB:
    __slots__ = "tables", "metadata", "_conn"

    def __init__(self, tablenames, valuetype=sa.String):
        md = sa.MetaData()
        self.tables = [mktable(tablenames[0], md)]
        for name in tablenames[1:-1]:
            self.tables.append(mktable(name, md, self.tables[-1].name))
        self.tables.append(mktable(name, md, self.tables[-1].name, valuetype))
        self.metadata = md

    def __getitem__(self, key):
        prev = self.tables[0]
        query = sa.sql.select(self.tables).where(prev.c.key == key)
        for t in self.tables[1:]:
            query = query.join(t, t.c.parent == prev.id)
        self.conn
