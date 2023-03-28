def pytest_itemcollected(item):
    node = item.obj
    if node.__doc__:
        test_title_parts = item._nodeid.split("::")
        test_title_parts[-1] = node.__doc__.strip()
        item._nodeid = "::".join(test_title_parts)
