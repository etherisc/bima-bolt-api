import logging

logging.getLogger(__name__).addHandler(logging.NullHandler())

def latitude_longitude_to_pixel(latitude, longitude):
    lat = int(round(latitude * 10.0, 1) + 401)
    lng = int(round(longitude * 10.0, 1) + 201)

    return 'Pixel{:03d}{:03d}'.format(lat, lng)

def pixel_to_latitude_longitude(pixel):
    if not pixel or pixel == 'PixelNaN':
        logging.warning("bad pixel location format for '{}'. returing lat/long = 0/0 as coordinates".format(pixel))
        return (0, 0)

    lat_idx = float(pixel[5:8])
    lng_idx = float(pixel[8:11])

    latitude = (lat_idx - 401) / 10.0
    longitude = (lng_idx - 201) / 10.0

    return (latitude, longitude)