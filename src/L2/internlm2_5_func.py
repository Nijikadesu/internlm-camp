from openai import OpenAI
import requests
import os


api_key = os.environ.get('api_key')


def add(a: int, b: int):
    return a + b


def mul(a: int, b: int):
    return a * b


def get_weather(location: str):
    # 如果 location 不是坐标格式（例如 "116.41,39.92"），则调用 GeoAPI 获取 LocationID
    if not ("," in location and location.replace(",", "").replace(".", "").isdigit()):
        # 使用 GeoAPI 获取 LocationID
        geo_url = f"https://geoapi.qweather.com/v2/city/lookup?location={location}&key={api_key}"
        geo_response = requests.get(geo_url)
        geo_data = geo_response.json()

        if geo_data.get("code") != "200" or not geo_data.get("location"):
            raise Exception(f"GeoAPI 返回错误码：{geo_data.get('code')} 或未找到位置")

        location = geo_data["location"][0]["id"]

    # 构建天气查询的 API 请求 URL
    weather_url = f"https://devapi.qweather.com/v7/weather/now?location={location}&key={api_key}"
    response = requests.get(weather_url)
    data = response.json()

    # 检查 API 响应码
    if data.get("code") != "200":
        raise Exception(f"Weather API 返回错误码：{data.get('code')}")

    # 解析和组织天气信息
    weather_info = {
        "location": location,
        "weather": data["now"]["text"],
        "temperature": data["now"]["temp"] + "°C", 
        "wind_direction": data["now"]["windDir"],
        "wind_speed": data["now"]["windSpeed"] + " km/h",  
        "humidity": data["now"]["humidity"] + "%",
        "report_time": data["updateTime"]
    }

    return {"result": weather_info}


tools = [{
    'type': 'function',
    'function': {
        'name': 'add',
        'description': 'Compute the sum of two numbers',
        'parameters': {
            'type': 'object',
            'properties': {
                'a': {
                    'type': 'int',
                    'description': 'A number',
                },
                'b': {
                    'type': 'int',
                    'description': 'A number',
                },
            },
            'required': ['a', 'b'],
        },
    }
}, {
    'type': 'function',
    'function': {
        'name': 'mul',
        'description': 'Calculate the product of two numbers',
        'parameters': {
            'type': 'object',
            'properties': {
                'a': {
                    'type': 'int',
                    'description': 'A number',
                },
                'b': {
                    'type': 'int',
                    'description': 'A number',
                },
            },
            'required': ['a', 'b'],
        },
    }
}, {
    'type': 'function',
    'function': {
        'name': 'get_weather',
        'description': 'Inquiry the weather of a certain location.',
        'parameters': {
            'type': 'object',
            'properties': {
                'location': {
                    'type': 'str',
                    'description': 'name of a certain place',
                }
            },
            'required': ['location'],
        }
    }
}]
messages = [{'role': 'user', 'content': '今天西安的天气怎么样.'}]


client = OpenAI(api_key='YOUR_API_KEY', base_url='http://0.0.0.0:23333/v1')
model_name = client.models.list().data[0].id
response = client.chat.completions.create(
    model=model_name,
    messages=messages,
    temperature=0.8,
    top_p=0.8,
    stream=False,
    tools=tools)
print(response)
func1_name = response.choices[0].message.tool_calls[0].function.name
func1_args = response.choices[0].message.tool_calls[0].function.arguments
func1_out = eval(f'{func1_name}(**{func1_args})')
print(func1_out)

messages.append({
    'role': 'assistant',
    'content': response.choices[0].message.content
})
messages.append({
    'role': 'environment',
    'content': f'3+5={func1_out}',
    'name': 'plugin'
})
response = client.chat.completions.create(
    model=model_name,
    messages=messages,
    temperature=0.8,
    top_p=0.8,
    stream=False,
    tools=tools)
print(response)
func2_name = response.choices[0].message.tool_calls[0].function.name
func2_args = response.choices[0].message.tool_calls[0].function.arguments
func2_out = eval(f'{func2_name}(**{func2_args})')
print(func2_out)