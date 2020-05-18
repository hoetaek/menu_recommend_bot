import requests
import json

def recommend_menu(message):
    # if machine learning accuracy is below 50 recommend from weather
    label, confidence = get_menu_from_machine_learning(message)
    return label


def get_menu_from_machine_learning(text):
    # This function will pass your text to the machine learning model
    # and return the top result with the highest confidence
    def classify(text):
        with open("secret.json", "r") as json_file:
            secret_data = json.load(json_file)
        key = secret_data['api']
        url = "https://machinelearningforkids.co.uk/api/scratch/" + key + "/classify"

        response = requests.get(url, params={"data": text})

        if response.ok:
            responseData = response.json()
            topMatch = responseData[0]
            return topMatch
        else:
            response.raise_for_status()

    # CHANGE THIS to something you want your machine learning model to classify
    demo = classify(text)

    label = demo["class_name"]
    confidence = demo["confidence"]

    # CHANGE THIS to do something different with the result
    return label, confidence


def get_menu_from_weather():
    api = "a560986489f334e6f7d370b85431e387"
    res = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q=Seoul&appid={api}&lang=kr&units=metric")
    weather_json = res.json()
    print(weather_json)
    print(weather_json.keys())
    clouds = weather_json['clouds']
    feels_like = weather_json['main']['feels_like']
    humidity = weather_json['main']['humidity']

    return '행복'


if __name__ == "__main__":
    get_menu_from_weather()
