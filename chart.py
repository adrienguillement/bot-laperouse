import matplotlib.pyplot as plt

from weather import get_temperature, get_humidity

def generate_temp_chart_image():

    data = get_temperature()

    names = list(data.keys())
    values = list(data.values())

    plt.plot(names, values, 'r') # Set data and set red color.
    plt.suptitle("Temperature")

    plt.savefig('./temp.png')
    plt.close()

    return True

def generate_humidity_chart_image():

    data = get_humidity()

    names = list(data.keys())
    values = list(data.values())

    plt.plot(names, values, 'b') # Set data and set blue color.
    plt.suptitle("Humidité")

    plt.savefig('./humidity.png')
    plt.close()

    return True
