import asyncio
from database.object import db

async def execute(query, is_many, values=None):

    if is_many:
        await db.execute_many(query=query, values=values)
    else:
        await db.execute(query=query, values=values)

async def fetch(query, is_one,  values=None):
    
    if is_one:
        result = await db.fetch_one(query=query, values=values)
        if result is None:
            out = None
        else:
            out = dict(result)
    else:
        result = await db.fetch_all(query=query, values=values)
        if result is None:
            out = None
        else:
            out = list()
            for row in result:
                out.append(dict(row))

    return out
async def update_mirror(values):
    query = "INSERT INTO MirrorAddress"
    query += "(name, latitude, longitude, googleAddress, formattedAddress, zipcode, status, created_at, updated_at)"
    query += "VALUES (:name, :latitude, :longitude, :googleAddress, :formattedAddress, :zipcode, :status, :created_at, :updated_at)"
    
    await execute(query, is_many=False, values=values)
    
    return 200

async def mirrorData(lat, lon):
    print(lat, lon)
    
    query_coords = f"""
    SELECT 
        latitude AS lat,
        longitude AS lon,
        formattedAddress
    FROM MirrorAddress
    WHERE
        latitude = {lat} AND
        longitude = {lon}
    """
    
    table_data = await fetch(query_coords, False)
    print(table_data)
    
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
    
if __name__ == "__main__":
    query = "SELECT * FROM accesszone"
    loop = asyncio.get_event_loop()
    print(loop.run_until_complete((fetch(query, True))))
    
