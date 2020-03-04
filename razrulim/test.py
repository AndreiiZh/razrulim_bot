import re

location = str('Location[lat=47.81325276106863, lon=35.188798617470724]')
lat = re.search('(?:lat=)(.................)', location)
lon = re.search('(?:lon=)(.................)', location)

location_user = {'lat': '', 'lon': ''}

if lat:
    location_user['lat'] = lat[1]

if lon:
    location_user['lon'] = lon[1]

print(location_user)
