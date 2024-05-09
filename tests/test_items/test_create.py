async def test_create_item(async_client):
    new_item = {
        "name": "Foo",
        "price": 35.4,
        "count": 100,
    }

    response = await async_client.post("/items/", json=new_item)
    created_item = response.json()
    assert response.status_code == 200, created_item
    assert "id" in created_item
