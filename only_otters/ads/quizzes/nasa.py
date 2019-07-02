from ad_resource import Resource
import json


FETCH_QUIZZES_TEMPLATE = Resource(
    source='https://climate.nasa.gov/climate_resource_center/interactives/quizzes',
    container='//ul[@class="item_list"]/li/div[@class="list_content"]',
    query={
        'img': 'div[@class="list_image"]/a/img/@src',
        'link': 'div[@class="list_image"]/a/@href',
        'content': 'div[@class="list_text"]/p/text()',
        'title': 'div[@class="list_text"]/h3/a/text()'
    }
)

print(*FETCH_QUIZZES_TEMPLATE())

QUIZ_TEMPLATE = Resource(
    source='https://climate.nasa.gov/quizzes/water-cycle/',
    container='',
    query={
        'questions': {

            'container': '//div[@class="interface-wrapper"]/article'
            'query': {

                'img': '',
                'counter': 'header[class="interface-top"]/div[class="count"]/div/text()',
                'name': 'header[class="interface-top"]/h2[class="question_short"]/text() {TAIL}',   # Might need a tail on first child
                'content': 'header[class="interface-top"]/div[class="question"]/p[class="question_long"]/text()',

                'options': {
                    'container': 'div[class="interface-middle"]/div[class="answer_column"]/div[class="answers"]/ul/li/label',
                    'query': {
                        'index': ''
                        'text': 
                    }
                }


            }
        }
    }
)

