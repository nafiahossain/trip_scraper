import os
import scrapy
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from sqlalchemy import create_engine, Column, Integer, String, Float, ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

Base = declarative_base()

class Hotel(Base):
    __tablename__ = 'hotels'

    id = Column(Integer, primary_key=True)
    propertyTitle = Column(String)
    rating = Column(String)
    location = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    room_type = Column(ARRAY(String))
    price = Column(String)
    img = Column(String)
    

class PostgreSQLPipeline:
    def __init__(self):
        self.engine = create_engine(os.getenv('DATABASE_URL'))
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def process_item(self, item, spider):
        session = self.Session()
        
        # Remove 'image_urls' and 'images' if they exist in the item
        item.pop('image_urls', None)
        item.pop('images', None)
        
        hotel = Hotel(**item)
        session.add(hotel)
        session.commit()
        session.close()
        return item


class CustomImagesPipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None, *, item=None):
        return f'full/{os.path.basename(request.url)}'

    def get_media_requests(self, item, info):
        adapter = ItemAdapter(item)
        for image_url in adapter['image_urls']:
            yield scrapy.Request(image_url)

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        
        # If you want to store just the first image
        adapter = ItemAdapter(item)
        adapter['img'] = image_paths[0]  # or handle multiple images as needed
        
        return item
