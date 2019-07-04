import cv2
import numpy as np
from datetime import datetime, timedelta

def get_black_background():
    return np.zeros((500, 500))

start_time = datetime.strptime("2019-01-01", "%Y-%m-%d")  # Можете выбрать любую дату
end_time = start_time + timedelta(days=1)

def convert_time_to_string(dt):
    return f"{dt.hour}:{dt.minute:02}" if dt.hour > 9 else f"0{dt.hour}:{dt.minute:02}"

def generate_image_with_text(text):
    image = get_black_background()
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(image, "TIME", (int(image.shape[0]*0.225), int(image.shape[1]*0.4)), font, 4, (255, 255, 0), 2, cv2.LINE_AA)
    cv2.putText(image, text, (int(image.shape[0]*0.15), int(image.shape[1]*0.7)), font, 4, (255, 255, 0), 2, cv2.LINE_AA)
    return image


while start_time < end_time:
    text = convert_time_to_string(start_time)
    image = generate_image_with_text(text)
    cv2.imwrite(f"time_images/1.jpg".replace(':', ''), image)
    start_time += timedelta(minutes=1)
