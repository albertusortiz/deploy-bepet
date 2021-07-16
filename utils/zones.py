from shapely.geometry import Point, Polygon
from database.main_fuctions import fetch
import json

async def coords_to_polygons(poly_list: list):
    PolygonsList = list()
    # for row in range(len(poly_list)):
    for row in range(len(poly_list)):
        # Gets from the row obtained, a dictionary
        # that contains the json string in the
        # polygoneData key
        poly_str = poly_list[row]['polygoneData']
        
        # Converts the string into a dictionary
        poly_dict = json.loads(poly_str)
        
        # Gets the list of the coordinates
        polygons_list = poly_dict['coordinates']

        # Convert to tupple all the arrays
        # Is a requirement of Polygon object
        for polygon_list in polygons_list:
            for c in range(len(polygon_list)):
                point_tuple = tuple(polygon_list[c])
                polygon_list[c] = point_tuple

        poly = Polygon(polygon_list)
        PolygonsList.append(poly)

    return PolygonsList

async def get_polygoneData(table_name, accesszone_id:int = 1):
    query = f"SELECT polygoneData FROM {table_name}" #" WHERE acccessZone_id = {accesszone_id}"
    polygoneData = await fetch(query, False)
    
    poly_list = await coords_to_polygons(polygoneData)
    
    return poly_list

async def point_in_zone(point: Point, poly_list):
    zone_flag = False
    p = 0
    while p < len(poly_list) and zone_flag == False:
        zone_flag = point.within(poly_list[p])
        if zone_flag is False:
            p += 1
    
    if zone_flag:
        return p
    else:
        return None
    
async def accessible_zone(point: Point):
    AccessPolys = await get_polygoneData("AccessZoneCity")
    is_in = await point_in_zone(point, AccessPolys)
    
    return is_in 

async def interest_zone(point: Point):
    InterestPolys = await get_polygoneData("AccessZoneInterests")
    is_in = await point_in_zone(point, InterestPolys)
    
    return is_in 

async def forbidden_zone(point: Point):
    ForbiddenPolys = await get_polygoneData("AccessZoneForbidden")
    is_in = await point_in_zone(point, ForbiddenPolys)
    
    return is_in 

async def status_zone(lat, lon):
    point = Point((lat, lon))
    
    access = await accessible_zone(point)
    forbidden = await forbidden_zone(point)
    interest = await interest_zone(point)
    if access:
        if forbidden:
            status = 3

        elif interest:
            status = 2

        else:
            status = 1
    else:
        status = 0
    
    return status