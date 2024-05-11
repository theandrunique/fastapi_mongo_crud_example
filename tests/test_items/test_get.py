from bson import ObjectId


async def test_get_item(async_client, prepare_test_element):
    response = await async_client.get(f"/items/{prepare_test_element.id}")
    assert response.status_code == 200, response.json()


async def test_get_list(async_client, prepare_test_element):
    response = await async_client.get("/items")
    assert response.status_code == 200, response.json()


async def test_item_not_found(async_client, prepare_test_element):
    response = await async_client.get(f"/items/{ObjectId()}")
    assert response.status_code == 404, response.json()
