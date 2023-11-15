import pandas as pd
from sklearn.model_selection import train_test_split
import shutil
import os
from sklearn.model_selection import train_test_split

df = pd.read_csv('./thumbnails/metadata.csv') 

df = df.sample(frac=1).reset_index(drop=True)

# split test into 0.10 and save slits 
train_df, test_df = train_test_split(df, test_size=0.10)

# include additional info from secondary dataset
additional_data_df = pd.read_csv('./thumbnails/videoInfo.csv') 
merge_columns = ['CC', 'URL', 'Released', 'Views', 'Category', 'Transcript', 'Length']
train_df = train_df.merge(additional_data_df[['Id'] + merge_columns], on='Id', how='left')
test_df = test_df.merge(additional_data_df[['Id'] + merge_columns], on='Id', how='left')

train_df.to_csv("train.csv", index=False)
test_df.to_csv("test.csv", index=False)

train_dir = './thumbnails/train_images'
test_dir = './thumbnails/test_images'
os.makedirs(train_dir, exist_ok=True)
os.makedirs(test_dir, exist_ok=True)

def copy_images(df, target_dir):
    for img_id in df['Id']:
        image_path = os.path.join('./thumbnails/all_images', f'{img_id}.jpg')  
        if os.path.isfile(image_path):
            shutil.copy(image_path, target_dir)

# save images in train/test directories
copy_images(train_df, train_dir)
copy_images(test_df, test_dir)