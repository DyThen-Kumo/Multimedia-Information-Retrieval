from .GeneralParameter import *

def normalize_data(data):
    # Kiểm tra nếu data là một vector 1 chiều
    if data.ndim == 1:
        normalized_data = data / np.linalg.norm(data)
    else:
        # Chuẩn hóa dữ liệu nếu là mảng 2 chiều
        normalized_data = data / np.linalg.norm(data, axis=1, keepdims=True)
    
    return normalized_data

def load_file_lines(file_path):
    """Đọc toàn bộ dòng từ một file và trả về danh sách các dòng."""
    try:
        with open(file_path, 'r') as f:
            return [line.strip() for line in f]
    except FileNotFoundError:
        print(f"File {file_path} không tồn tại!")
        return []
    
def get_path(list_image):
    results = []
    for name in list_image:
        folder = name.split('_')[1]
        image_path = os.path.join(data_path, folder, f'{name}.jpg')
        results.append(image_path)

    return results