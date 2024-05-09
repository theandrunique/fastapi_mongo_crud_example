async def test_patch_all_fields_item(async_client, prepare_test_element):
    response = await async_client.patch(
        f"/items/{prepare_test_element.id}",
        json={"price": 35.3, "count": 200, "name": "Bar"},
    )
    assert response.status_code == 200, response.json()

    response = await async_client.get(f"/items/{prepare_test_element.id}")

    patched_item = response.json()

    assert response.status_code == 200, patched_item

    assert patched_item["price"] == 35.3
    assert patched_item["count"] == 200
    assert patched_item["name"] == "Bar"



async def test_patch_item(async_client, prepare_test_element):
    response = await async_client.patch(
        f"/items/{prepare_test_element.id}", json={"count": 200}
    )

    response = await async_client.get(f"/items/{prepare_test_element.id}")
    patched_item = response.json()
    assert response.status_code == 200, patched_item

    assert patched_item["price"] == prepare_test_element.price
    assert patched_item["count"] == 200
    assert patched_item["name"] == prepare_test_element.name
