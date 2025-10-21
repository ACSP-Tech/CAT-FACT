import requests
from requests.exceptions import RequestException, Timeout, ConnectionError

CAT_FACT_API_URL = f"https://catfact.ninja/fact"
API_TIMEOUT = 10 
FALLBACK_FACT = "Cats are amazing creatures! (Fun fact temporarily unavailable)"

async def fetch_cat_fact():
    """
    Fetch a cat fact from external API with proper error handling.
    
    Returns:
        str: Cat fact or fallback message
    """
    try:
        response = requests.get(
            CAT_FACT_API_URL,
            timeout=API_TIMEOUT,
            headers={'Accept': 'application/json'}
        )
        
        # Check if request was successful
        response.raise_for_status()
        
        # Parse JSON response
        data = response.json()
        
        # Validate response structure
        if "fact" not in data:
            return FALLBACK_FACT
        
        return data["fact"]
    
    except Timeout:
        return FALLBACK_FACT
    
    except ConnectionError:
        return FALLBACK_FACT
    
    except requests.exceptions.HTTPError as e:
        return FALLBACK_FACT
    
    except requests.exceptions.JSONDecodeError:
        return FALLBACK_FACT
    
    except RequestException as e:
        return FALLBACK_FACT
    
    except Exception as e:
        return FALLBACK_FACT