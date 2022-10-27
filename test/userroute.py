import json

def test_create_user(client):
    data = {"email" : "sheersh@gkmit.co" , "password" : "SHEERSH"}
    response = client.post("/users" , json.dumps(data))
    assert response.status_code==200
    assert response.json()["email"] == "sheersh@gkmit.co"
    assert response.json()["is_active"] == True

    
