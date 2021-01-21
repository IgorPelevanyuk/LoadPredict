from ResourceUsage import ResourceUsage

x = ResourceUsage({
    'cpu_usage': 10,
    "ram": 1000,
    "network": 1000
})
y = ResourceUsage({
    'cpu_usage': 15,
    "ram": 500,
})
z = ResourceUsage({
    'cpu_usage': 15,
    "ram": 500,
    "network": 1000
})


def test_resource_usage_sum_1():
    z = x + y
    assert z.resource_usage['cpu_usage'] == 25
    assert z.resource_usage['ram'] == 1500
    assert z.resource_usage['network'] == 1000

def test_resource_usage_sum_2():
    z = y + x
    assert z.resource_usage['cpu_usage'] == 25
    assert z.resource_usage['ram'] == 1500
    assert z.resource_usage['network'] == 1000

def test_resource_usage_eq_1():
    assert y != z

def test_resource_usage_eq_2():
    temp1 = ResourceUsage({
        'cpu_usage': 15,
        "ram": 500,
        "network": 1000
    })
    temp2 = ResourceUsage({
        'cpu_usage': 15,
        "ram": 500,
        "network": 1000
    })
    assert temp1 == temp2