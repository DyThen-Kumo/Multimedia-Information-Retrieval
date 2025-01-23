from .GeneralFunction import *

def process_queries(query_file, device='cpu'):
    """
    Đọc file query, cắt ảnh theo bounding box và extract feature theo từng bb.
    
    :param query_file: Đường dẫn đến file query.txt
    :param image_folder: Thư mục chứa ảnh
    """
    with open(query_file, 'r') as file:
        features = []
        for line in file:
            # Tách dòng query thành các phần tử
            parts = line.strip().split()
            if len(parts) != 5:
                continue
            
            image_name = parts[0] + '.jpg'  # Tên file ảnh
            x1, y1, x2, y2 = map(float, parts[1:])  # Bounding box
            
            # Đường dẫn đầy đủ đến ảnh
            image_path = os.path.join(data_path, image_name.split('_')[1], image_name)
            
            # Kiểm tra ảnh tồn tại
            if not os.path.exists(image_path):
                print(f"Ảnh {image_name} không tồn tại trong thư mục {os.path.join(data_path, image_name.split('_')[1])}.")
                continue
            
            # Mở ảnh và cắt theo bounding box
            with Image.open(image_path).convert('RGB') as img:
                cropped_img = img.crop((x1, y1, x2, y2))  # Cắt ảnh
                # Extract feature của ảnh crop
                cropped_img = transform(cropped_img).unsqueeze(0).to(device)
                with torch.no_grad():
                    feature = model.get_image_features(cropped_img)
                feature = feature.squeeze().cpu().numpy()
                features.append(feature)
        
        return features
    
def get_clip_features(image_paths, device='cpu'):
    features = []
    for image_path in image_paths:
        if not os.path.exists(image_path):
            print(f"Ảnh  không tồn tại trong thư mục.")
            continue

        with Image.open(image_path).convert('RGB') as img:
            # Extract feature của ảnh crop
            img = transform(img).unsqueeze(0).to(device)
            with torch.no_grad():
                feature = model.get_image_features(img)
            feature = feature.squeeze().cpu().numpy()
            features.append(feature)
        
    return features

def get_query():
    query = []
    map_qr = []
    for file in os.listdir(gt_path):
        if 'query' in file:
            # print(file)
            map_qr.append(file.split('.')[0])
            query_file = os.path.join(gt_path, file)
            features = process_queries(query_file=query_file)
            if len(features) == 1:
                query.append(features[0])

    query = np.array(query)
    map_qr = [name[:-6] if name.endswith("_query") else name for name in map_qr]

    return query, map_qr