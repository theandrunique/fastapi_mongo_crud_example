async def test_patch_all_fields_item(async_client, prepare_test_element):
    response = await async_client.patch(
        f"/items/{prepare_test_element.id}",
        json={"price": 35.3, "count": 200, "name": "Bar"},
    )
    assert response.status_code == 200, response.json()
    assert response.json()["price"] == 35.3
    assert response.json()["count"] == 200
    assert response.json()["name"] == "Bar"


async def test_patch_item(async_client, prepare_test_element):
    response = await async_client.patch(
        f"/items/{prepare_test_element.id}", json={"count": 200}
    )
    assert response.status_code == 200, response.json()
    assert response.json()["price"] == prepare_test_element.price
    assert response.json()["count"] == 200
    assert response.json()["name"] == prepare_test_element.name
