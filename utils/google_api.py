import aiohttp
from utils.const import GEOCODING_KEY

async def async_google_data(lat, lon):
    async with aiohttp.ClientSession() as session:
        url = "https://maps.googleapis.com/maps/api/geocode/"
        url += f"json?latlng={lat},{lon}&key={GEOCODING_KEY}"
        
        async with session.get(url) as resp:
            data = await resp.json()
            first_result = data['results'][0]
            formated_address = first_result['formatted_address']
            address_data = first_result['address_components']
            
            return formated_address, address_data

# address, components = await async_google_data(TEST_LAT, TEST_LON)
# print(components)
# address