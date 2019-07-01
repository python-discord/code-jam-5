from ad_resource import Resource
import json


FETCH_QUIZZES_TEMPLATE = Resource(
    source='https://climate.nasa.gov/climate_resource_center/interactives/quizzes',
    container='//ul[@class="item_list"]'
)

QUIZ_TEMPLATE = Resource(

)

