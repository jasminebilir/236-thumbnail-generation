# -*- coding: utf-8 -*-
"""B2_frame_captioning.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/19ecUGSjdOcKbkuFmkvW3UHctB_IVZ4Rr
"""

import requests
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration

processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")


from google.colab import drive
drive.mount('/content/drive', force_remount=True)

import pandas as pd
import os

csv_file_path = '/content/drive/MyDrive/236/test.csv'
image_folder_path =  '/content/drive/MyDrive/236/frames2_test'

df = pd.read_csv(csv_file_path)

image_files = set(f for f in os.listdir(image_folder_path) if f.endswith('.jpg'))

df['BlipCaption'] = ''

for index, row in df.iterrows():
    expected_image_file = f'frame_{row.iloc[0]}.jpg'
    if expected_image_file in image_files:
      with Image.open('/content/drive/MyDrive/236/frames2_test/'+expected_image_file) as img:
        raw_image = img.convert('RGB')
        inputs = processor(raw_image, return_tensors="pt")
        out = model.generate(**inputs, max_length=200)
        caption = processor.decode(out[0], skip_special_tokens=True)
        df.at[index, 'BlipCaption'] = caption
    else:
        df.drop(index, inplace=True)

df.to_csv('/content/drive/MyDrive/236/test_images_exp1_blip.csv', index=False)
