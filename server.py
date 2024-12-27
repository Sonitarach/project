import http.server
import socketserver
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

PORT = 8000


# Генерация данных о температуре
def generate_temperature_data():
    dates = pd.date_range(start='2013-01-01', end='2023-12-31', freq='D')
    temperatures = np.random.normal(loc=15, scale=10, size=len(dates))  # Средняя температура
    return pd.DataFrame({'Date': dates, 'Temperature': temperatures})


# Сохранение графиков
def save_plot(data, method):
    plt.figure(figsize=(10, 5))
    plt.plot(data['Date'], data['Temperature'], label=f'{method} Temperature')
    plt.title(f'Average Temperature ({method})')
    plt.xlabel('Date')
    plt.ylabel('Temperature (°C)')
    plt.legend()
    plt.grid()
    plt.savefig(f'static/{method.lower()}_temperature.png')
    plt.close()


# Создание графиков для всех методов
def create_plots():
    data = generate_temperature_data()

    save_plot(data, 'Asyncio')
    save_plot(data, 'Threading')
    save_plot(data, 'Multiprocessing')


# HTTP обработчик
class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            create_plots()  # Генерация графиков при первом запросе
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            # HTML-контент
            html_content = '''
            <!DOCTYPE html>
            <html lang="ru">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Сравнение методов синхронного программирования</title>
            </head>
            <body>
                <h1>Сравнение методов синхронного программирования</h1>

                <h2>Графики средних температур</h2>

                <h3>Asyncio</h3>
                <img src="static/asyncio_temperature.png" alt="Asyncio Temperature">

                <h3>Threading</h3>
                <img src="static/threading_temperature.png" alt="Threading Temperature">

                <h3>Multiprocessing</h3>
                <img src="static/multiprocessing_temperature.png" alt="Multiprocessing Temperature">

            </body>
            </html>
            '''
            self.wfile.write(html_content.encode('utf-8'))
        else:
            super().do_GET()


# Запуск сервера
if __name__ == "__main__":
    if not os.path.exists('static'):
        os.makedirs('static')  # Создание каталога для сохранения изображений

    with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
        print(f"Сервер запущен на порту {PORT}")
        httpd.serve_forever()