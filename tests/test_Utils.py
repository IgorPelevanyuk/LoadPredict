from Utils import Distributor


def test_response_equal():
    distributor = Distributor(10)

    requests = [5, 5, 5, 5, 5]
    reference_response = [2, 2, 2, 2, 2]

    for i in range(5):
        distributor.add_request(i, requests[i])

    response = distributor.calculate_responses()
    for i in range(len(response)):
        assert response[i] == reference_response[i]


def test_response_fair():
    distributor = Distributor(10)

    requests = [1, 1, 2, 3, 5]
    reference_response = [1, 1, 2, 3, 3]

    for i in range(5):
        distributor.add_request(i, requests[i])

    response = distributor.calculate_responses()
    for i in range(len(response)):
        assert response[i] == reference_response[i]


def test_response_zeros():
    distributor = Distributor(10)

    requests = [0, 0, 1, 1, 2, 3, 5, 0]
    reference_response = [0, 0, 1, 1, 2, 3, 3, 0]

    for i in range(len(requests)):
        distributor.add_request(i, requests[i])

    response = distributor.calculate_responses()
    for i in range(len(response)):
        assert response[i] == reference_response[i]