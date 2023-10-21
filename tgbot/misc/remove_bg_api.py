import requests


def removal_bg(image_url: str):
    url = "https://picsart-remove-background2.p.rapidapi.com/removebg"

    payload = {
        "image_url": image_url,
        "bg_blur": "0",
        "format": "PNG"
    }
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "X-RapidAPI-Key": "69bc405e5bmsh2f4565ba236cd4bp1ea962jsne4eb459bbc5c",
        "X-RapidAPI-Host": "picsart-remove-background2.p.rapidapi.com"
    }

    response = requests.post(url, data=payload, headers=headers)

    print(response.json())
    return response.json()['data']['url'].split('?')[0]