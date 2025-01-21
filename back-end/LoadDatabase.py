from GetInputFeatures import *

def load_features():
    database = []
    map_db = []
    for file in os.listdir(features_path):
        file_path = os.path.join(features_path, file)

        with open(file_path, "rb") as f:
            image_features_data = pickle.load(f) # 1 list, các phần tử là dict với image_name và features

            for item in image_features_data:
                database.append(item['features'])
                map_db.append(item['image_name'].replace('.jpg',''))

    database = np.array(database)

    return database, map_db

def load_index(index_path):
    # if retrain:
    #     index_path = os.path.join(github_path, 'index', 'feature_paris_clip_3.pkl')
    # else:
    #     index_path = os.path.join(github_path, 'index', 'feature_clip.pkl')
        
    with open(index_path, 'rb') as f:
        database = pickle.load(f)
        index = database["index"]
        map_index = database["map_index"]

    map_index = [filename.replace('.jpg', '') for filename in map_index]
    return index, map_index