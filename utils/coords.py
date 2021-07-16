from datetime import datetime
from utils.zipcodes import zipcode_in_address
from database.main_fuctions import fetch, update_mirror
from .zones import status_zone
from .google_api import async_google_data

async def mirrorData(lat, lon):
    
    query_coords = f"""
    SELECT 
        latitude AS lat,
        longitude AS lon,
        formattedAddress
    FROM MirrorAddress
    WHERE
        latitude = :lat AND
        longitude = :lon
    """
    
    coords = {
        'lat': lat,
        'lon': lon
    }
    
    table_data = await fetch(query_coords, False, coords)
    
    if len(table_data) == 1:
        table_response = table_data[0]
        table_response['in_base'] = 1
    
    elif len(table_data) == 0:
        table_response = dict()
        table_response['in_base'] = 0
    
    else:
        table_response = dict()
        table_response['in_base'] = len(table_data)
        
    return table_response

def mirror_dict(name, lat, lon, components, address, created_at, status):
    values = {
        "name": name,
        "latitude": str(lat),
        "longitude": str(lon),
        "googleAddress": str(components),
        "formattedAddress": address,
        "zipcode": zipcode_in_address(address),
        "status": str(status),
        "created_at": created_at,
        "updated_at": datetime.now(),
    }
    
    return values
    
async def coords_data(lat, lon, name=None):
    created_at = datetime.now()
    mirror_data = await mirrorData(lat, lon)
    
    # If the point is not in DB:
    if mirror_data['in_base'] != 1:
        # Get lat and lon 
        status = await status_zone(lat, lon)
        address, components = await async_google_data(lat, lon)
        DataToMirror = mirror_dict(name, lat, lon, components, address, created_at, status)
        status = await update_mirror(DataToMirror)
        
        return DataToMirror

    return mirror_data