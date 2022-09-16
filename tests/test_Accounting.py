from Accounting import Accounting


def test_delete_databases():
    accounting = Accounting()
    databases = accounting.list_databases()
    databases = [x for x in databases if "test" in x]
    #accounting.drop_databases(databases)


