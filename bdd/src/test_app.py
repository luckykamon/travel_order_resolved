import requests

def test_app():
    """Test the app"""  
    
    result = requests.get("http://localhost:3000")
    assert result.status_code == 200