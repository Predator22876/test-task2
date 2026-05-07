def create_wallet(client):
    response = client.post(
        "/api/v1/wallets"
    )
    assert response.status_code == 200

    return response.json()["uuid"]


def test_create_wallet(client):
    response = client.post(
        "/api/v1/wallets"
    )
    assert response.status_code == 200

    data = response.json()

    assert "uuid" in data
    assert data["balance"] == 0


def test_get_balance(client):
    wallet_id = create_wallet(client)
    response = client.get(
        f"/api/v1/wallets/{wallet_id}/balance"
    )
    assert response.status_code == 200
    data = response.json()
    assert data["balance"] == 0


def test_deposit(client):
    wallet_id = create_wallet(client)
    response = client.post(
        f"/api/v1/wallets/{wallet_id}/operation",
        json={
            "operation_type": "DEPOSIT",
            "amount": 1000,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["balance"] == 1000


def test_withdraw(client):
    wallet_id = create_wallet(client)
    client.post(
        f"/api/v1/wallets/{wallet_id}/operation",
        json={
            "operation_type": "DEPOSIT",
            "amount": 1000,
        },
    )
    response = client.post(
        f"/api/v1/wallets/{wallet_id}/operation",
        json={
            "operation_type": "WITHDRAW",
            "amount": 300,
        },
    )

    assert response.status_code == 200
    data = response.json()

    assert data["balance"] == 700


def test_insufficient_funds(client):
    wallet_id = create_wallet(client)

    response = client.post(
        f"/api/v1/wallets/{wallet_id}/operation",
        json={
            "operation_type": "WITHDRAW",
            "amount": 1000,
        },
    )
    assert response.status_code == 400

    assert (
        response.json()["detail"]
        == "Количество средств на кошельке меньше запрашиваемого для снятия"
    )


def test_wallet_not_found(client):
    response = client.get(
        "/api/v1/wallets/123/balance"
    )

    assert response.status_code == 404


def test_concurrent_withdrawals(client):
    wallet_id = create_wallet(client)

    client.post(
        f"/api/v1/wallets/{wallet_id}/operation",
        json={
            "operation_type": "DEPOSIT",
            "amount": 1000,
        },
    )

    responses = [
        client.post(
            f"/api/v1/wallets/{wallet_id}/operation",
            json={
                "operation_type": "WITHDRAW",
                "amount": 10,
            },
        )
        for _ in range(100)
    ]
    success_count = sum(
        1 for r in responses if r.status_code == 200
    )
    assert success_count == 100

    response = client.get(
        f"/api/v1/wallets/{wallet_id}/balance"
    )
    balance = response.json()["balance"]
    assert balance == 0
