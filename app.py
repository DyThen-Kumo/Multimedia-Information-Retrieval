from flask import Flask, request, jsonify, render_template, url_for
from BackEnd.SearchEngine import *
import os

app = Flask(__name__)
upload_folder = os.path.join(github_path, 'static', 'uploads')
app.config['UPLOAD_FOLDER'] = upload_folder

delay_pic = os.path.join(github_path, 'static','img','avatar.png') # 'D:\CLB-AI\AIC2024\static\img\avatar.png'

# Folder chứa ảnh
IMAGE_FOLDERS = {}
for folder in os.listdir(data_path):
    IMAGE_FOLDERS[folder] = os.path.join(data_path, folder)

# Bình thường cần có
@app.route('/')
def render_root():
    return render_template('root.html')

@app.route('/home')
def render_home():
    return render_template('home.html')

@app.route('/about')
def render_about():
    return render_template('about.html')

# Tab Search
@app.route('/Retrieval_By_Text')
def render_Retrieval_By_Text():
    return render_template('Retrieval-By-Text.html')

@app.route('/Retrieval_By_Image')
def render_Retrieval_By_Image():
    return render_template('Retrieval-By-Image.html')

# Tab Generate
@app.route('/generative-text')
def render_generative_text():
    return render_template('Generative-Text.html')

@app.route('/generative-image')
def render_generative_image():
    return render_template('Generative-Image.html')

@app.route('/upload-image', methods=['POST'])
def upload_image():
    if 'InputImage' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['InputImage']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    # Save the file
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    # Return the URL of the uploaded file
    file_url = url_for('static', filename=f'uploads/{file.filename}')
    return jsonify({'url': file_url})

# Quick Answer
@app.route('/change-parameter', methods=['POST'])
def change_parameter():
    global use_index
    global retrain
    global index_path
    global features_path
    global model

    _use_Index = request.form.get('useIndex') == 'true'
    _linkIndex = request.form.get('linkIndex')
    _retrain = request.form.get('retrain') == 'true'
    set_parameter(_use_index = _use_Index, 
                  _index_path=_linkIndex, 
                  _retrain = _retrain)
    
    # if use_index:
    #     index_path = _linkIndex

    # if retrain:
    #     features_path = os.path.join(project_path, 'features', 'features_paris_clip_3')
    #     print('Model đã retrain!!')
    #     model = torch.load(r'C:\Retrieval System\model\paris_clip_3.pth', map_location=torch.device('cpu'))
    # else:
    #     features_path = os.path.join(project_path, 'features', 'features_clip')
    #     model = CLIPModel.from_pretrained('openai/clip-vit-base-patch32')
    # model.eval()

    # Trả về phản hồi thành công cho front-end
    return jsonify("message: Form submitted successfully!")

# Search ảnh
@app.route('/get-retrieval-by-text', methods=['POST'])
def get_retrieval_by_text():
    num_images = request.form.get('num_images')
    language = request.form.get('language')
    input_text = request.form.get('input_text')

    input_data = (num_images, language, input_text)
    image_files, similarity_matrix = post_retrieval_by_text(input_data)
    image_urls = [url for url in image_files]
    return jsonify(image_urls)

@app.route('/get-retrieval-by-image', methods=['POST'])
def get_retrieval_by_image():
    image_files = []
    # Đọc dữ liệu từ form
    number_image = request.form.get('number_image')
    url = request.form.get('url')  # Đọc giá trị của InputURL
    if url:
        input_data = (number_image, url)
        image_files, similarity_matrix = post_retrieval_by_image(input_data)
        image_urls = [url for url in image_files]
        return jsonify(image_urls)
    # Đọc file được upload
    file = request.files.get('image')  # Đọc file từ InputImage
    if file:
        # Lưu file vào thư mục uploads
        filename = file.filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        input_data = (number_image,file_path)
        image_files, similarity_matrix= post_retrieval_by_image(input_data)
        image_urls = [url for url in image_files]
        return jsonify(image_urls)

# Reranking
@app.route('/confirm_selection', methods=['POST'])
def confirm_selection():
    selected_images = request.form.getlist('selected_images[]')  # Lấy danh sách các đường dẫn hình ảnh đã chọn
    number_images = int(request.form.getlist('number_images')[0])

    print(selected_images, number_images)
    image_files = post_rerank(list_images=selected_images, k=number_images)
    image_urls = [url for url in image_files]
    return jsonify(image_urls)

if __name__ == '__main__':
    app.run(debug=True)
