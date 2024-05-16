import os
import re
import speech_recognition as sr
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image as KivyImage

# Словарь для сопоставления карт и изображений
cards = {
    'двойка червей': 'dvoyka-chervey.png',
    'тройка червей': 'troyka-chervey.png',
    'четвёрка червей': 'chetyre-chervey.png',
    'пятёрка червей': 'pjat-chervey.png',
    # Добавьте остальные карты всех мастей
}

class WallpaperApp(App):
    def build(self):
        self.title = 'Card Wallpaper App'
        layout = BoxLayout(orientation='vertical')
        self.label = Label(text="Скажите карту", font_size='20sp')
        layout.add_widget(self.label)
        self.button = Button(text='Начать прослушивание', font_size='20sp', on_press=self.listen_for_card)
        layout.add_widget(self.button)
        self.image = KivyImage()
        layout.add_widget(self.image)
        return layout

    def listen_for_card(self, instance):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            self.label.text = "Прослушивание..."
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)
        try:
            card_name = recognizer.recognize_google(audio, language='ru-RU').lower()
            self.label.text = f"Вы сказали: {card_name}"
            self.change_wallpaper(card_name)
        except sr.UnknownValueError:
            self.label.text = "Не удалось распознать голос"
        except sr.RequestError:
            self.label.text = "Ошибка сервиса распознавания речи"

    def extract_card_name(self, card_name):
        pattern = re.compile(r'\b(' + '|'.join(cards.keys()) + r')\b')
        match = pattern.search(card_name)
        if match:
            return match.group(0)
        return None

    def change_wallpaper(self, card_name):
        extracted_card_name = self.extract_card_name(card_name)
        if extracted_card_name and extracted_card_name in cards:
            images_folder = os.path.abspath('images')
            image_path = os.path.join(images_folder, cards[extracted_card_name])
            if os.path.exists(image_path):
                self.label.text = f"Смена обоев на {extracted_card_name}"
                wallpaper_path = os.path.abspath(image_path)
                self.image.source = wallpaper_path
                self.set_wallpaper(wallpaper_path)
                self.label.text = f"Обои изменены на {extracted_card_name}"
            else:
                self.label.text = f"Изображение для карты {extracted_card_name} не найдено"
        else:
            self.label.text = "Карта не распознана или не поддерживается"

    def set_wallpaper(self, image_path):
        # Добавьте здесь код для изменения обоев на устройстве Android
        # Например, можно использовать Android API или другие методы
        print("Обои успешно изменены")

if __name__ == '__main__':
    WallpaperApp().run()





