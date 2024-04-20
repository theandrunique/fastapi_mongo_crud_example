from bson import ObjectId


async def test_delete(async_client, prepare_test_element):
    response = await async_client.delete(
        f"/items/{prepare_test_element.id}",
    )
    assert response.status_code == 200, response.json()
    response = await async_client.get(f"/items/{prepare_test_element.id}")
    assert response.status_code == 404, response.json()


async def test_delete_not_found(async_client):
    response = await async_client.delete(f"/items/{ObjectId()}")
    assert response.status_code == 404
