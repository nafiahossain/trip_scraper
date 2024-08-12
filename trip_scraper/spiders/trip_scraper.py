import json
import random
from pathlib import Path
import re
import scrapy
from itemadapter import ItemAdapter
from trip_scraper.items import HotelItem

class HotelSpider(scrapy.Spider):
    name = "trip_scraper"

    def start_requests(self):
        start_url = "https://uk.trip.com/hotels/?locale=en-GB&curr=GBP"
        headers = {
            'Accept': 'application/json',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
        }
        
        yield scrapy.Request(start_url, headers=headers, callback=self.parse_locations)

    def parse_locations(self, response):
        script_text = response.xpath('//script[contains(text(), "window.IBU_HOTEL")]/text()').get()
        try:
            json_data = re.search(r'window\.IBU_HOTEL\s*=\s*(\{.*?\});', script_text, re.DOTALL).group(1)
            data = json.loads(json_data)
        except (AttributeError, json.JSONDecodeError) as e:
            self.log(f"Error parsing JSON data: {e}")
            return

        locations = []
        hotels = []

        for city_group in ['inboundCities', 'outboundCities']:
            if city_group in data['initData']['htlsData']:
                for city in data['initData']['htlsData'][city_group]:
                    if city['type'] == "City":
                        location_item = {
                            "id": city['id'],
                            "name": city['name'],
                            "cityUrl": city['cityUrl'],
                            "imgUrl": city['imgUrl'],
                        }
                        locations.append(location_item)

                        # Extract hotel data for each city
                        if 'recommendHotels' in city:
                            for hotel in city['recommendHotels']:
                                hotel_item = HotelItem(
                                    propertyTitle=hotel['hotelName'],
                                    rating=hotel.get('rating', 'N/A'),
                                    location=city['cityUrl'],
                                    latitude=hotel.get('lat', 'N/A'),
                                    longitude=hotel.get('lon', 'N/A'),
                                    room_type=[amenities['name'] for amenities in hotel.get('hotelFacilityList', [])],
                                    price=hotel.get('displayPrice', {}).get('price', 'N/A'),
                                    img=f"https://ak-d.tripcdn.com/images{hotel.get('imgUrl', '')}",
                                    image_urls=[f"https://ak-d.tripcdn.com/images{hotel.get('imgUrl', '')}"]
                                )
                                yield hotel_item
                                
                                # Convert the hotel_item to a dictionary
                                hotel_dict = ItemAdapter(hotel_item).asdict()
                                hotels.append(hotel_dict)

        # Save the locations to a JSON file
        Path('Scraped_locations.json').write_text(json.dumps(locations, indent=4))
        self.log(f'Saved locations to Scraped_locations.json')

        # Save the hotels to a JSON file
        Path('Scraped_hotels.json').write_text(json.dumps(hotels, indent=4))
        self.log(f'Saved hotels to Scraped_hotels.json')
