class ResourceUsage():

    def __init__(self, resource_usage={}):
        self.resource_usage = {
            "cpu_usage": 0,
            "ram": 0,
            "network": 0,
        }
        for key in resource_usage:
            self.resource_usage[key] = resource_usage[key]

    def __add__(self, other):
        result = self.resource_usage.copy()
        for key in other.resource_usage:
            if key not in result:
                result[key] = 0
            result[key] += other.resource_usage[key]
        return ResourceUsage(result)

    def __eq__(self, other):
        return self.resource_usage == other.resource_usage

    def __getitem__(self, key):
        return self.resource_usage[key]

    def __setitem__(self, key, value):
        self.resource_usage[key] = value

    def __repr__(self):
        return str(self.resource_usage)

