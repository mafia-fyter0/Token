import requests

def get_pages_tokens(fb_id_token):
    """ Get a list of pages and their corresponding access tokens """
    endpoint = "https://graph.facebook.com/v13.0/me/accounts"
    headers = {
        "Authorization": f"Bearer {fb_id_token}",
        "Content-Type": "application/json"
    }
    try:
        response = requests.get(endpoint, headers=headers)
        response.raise_for_status()
        data = response.json()
        pages_tokens = {}
        for page in data["data"]:
            page_id = page["id"]
            page_name = page["name"]
            page_token_endpoint = "https://graph.facebook.com/v13.0"
            page_token_response = requests.get(page_token_endpoint, headers=headers)
            page_token_response.raise_for_status()
            page_token_data = page_token_response.json()
            if "access_token" in page_token_data:
                page_token = page_token_data["access_token"]
                pages_tokens[page_id] = {"name": page_name, "token": page_token}
            else:
                print(f"Warning: No access token found for page {page_name} (ID: {page_id})")
        return pages_tokens
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return {}

def main():
    fb_id_token = input("Enter your Facebook ID token: ")
    pages_tokens = get_pages_tokens(fb_id_token)
    for page_id, page_info in pages_tokens.items():
        print(f"Page ID: {page_id}, Name: {page_info['name']}, Token: {page_info['token']}")

if __name__ == "__main__":
    main()
