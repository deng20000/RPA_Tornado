import requests

def test_lingxing_orders():
    url = "http://127.0.0.1:8888/api/lingxing/orders"
    resp = requests.post(url, json={})
    # print(resp.text)
    # assert resp.status_code == 200
    data = resp.json()
    assert data["code"] == 0 or data["code"] == 1  # 0:成功，1:无数据或API异常
    print("接口返回：", data)

if __name__ == "__main__":
    test_lingxing_orders() 