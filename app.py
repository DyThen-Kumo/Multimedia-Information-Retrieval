from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
from BackEnd.ReRanking import *
import os

app = Flask(__name__)
upload_folder = os.path.join('static', 'uploads')
app.config['UPLOAD_FOLDER'] = upload_folder

delay_pic = os.path.join(github_path,'static','img','avatar.png') # 'D:\CLB-AI\AIC2024\static\img\avatar.png'

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

# Quick Answer
@app.route('/quick-answer', methods=['POST'])
def quick_answer():
    return
    submit_name = request.form.get('submit_name')
    video_name = request.form.get('video_name')
    number_start = int(request.form.get('number_start'))
    number_end = int(request.form.get('number_end'))
    
    add_quick_answer(submit_name, video_name, number_start, number_end)

    # Trả về phản hồi thành công cho front-end
    return jsonify("message: Form submitted successfully!")

# Search ảnh
@app.route('/get-retrieval-by-text', methods=['POST'])
def get_retrieval_by_text():
    image_files = []
    path = r'C:\Retrieval System\Multimedia-Information-Retrieval\static\img'
    for image in os.listdir(path):
        image_files.append(os.path.join(path, image))

    image_urls = [url for url in image_files]
    return jsonify(image_urls)

    num_images = request.form.get('num_images')
    language = request.form.get('language')
    input_text = request.form.get('input_text')

    input_data = (num_images, language, input_text)
    image_files = post_regular_images(input_data)
    image_urls = [url for url in image_files]
    return jsonify(image_urls)

@app.route('/get-retrieval-by-image', methods=['POST'])
def get_retrieval_by_image():
    # Xử lý dữ liệu và trả về danh sách đường dẫn ảnh
    image_folder = os.path.join(data_path, "eiffel")
    image_files = os.listdir(image_folder)
    image_urls = [os.path.join(image_folder, name) for name in  image_files]
    return jsonify(image_urls)

    image_files = []
    # Đọc dữ liệu từ form
    number_image = request.form.get('number_image')
    url = request.form.get('url')  # Đọc giá trị của InputURL
    if url:
        input_data = (number_image, url)
        image_files = post_relative_images(input_data)
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
        image_files = post_relative_images(input_data)
        image_urls = [url for url in image_files]
        return jsonify(image_urls)

# Generate ảnh
@app.route('/get-generative-text', methods=['POST'])
def get_generative_text():
    return
    language = request.form.get('language')
    input_text = request.form.get('input_text')
    if language == 'vi':
        input_text = trans(text_input=input_text)
    image_urls = [post_generative_text(input_text)]
    # image_urls = [url for url in image_files]
    return jsonify(image_urls)

@app.route('/get-generative-images', methods=['POST'])
def get_generative_images():
    return
        # Đọc file được upload
    file = request.files.get('image')  # Đọc file từ InputImage
    if file:
        # Lưu file vào thư mục uploads
        filename = file.filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        input_text = file_path
        image_urls = [post_generative_images(input_text)]
        return jsonify(image_urls)
    
    return jsonify(delay_pic)

# Tạo file nộp bài
@app.route('/confirm_selection', methods=['POST'])
def confirm_selection():
    return
    selected_images = request.form.getlist('selected_images[]')  # Lấy danh sách các đường dẫn hình ảnh đã chọn
    submit_file_name = request.form.getlist('submit_file_name')[0]
    print('Submit file name:',submit_file_name)
    try:
        # Xử lý danh sách các đường dẫn hình ảnh đã chọn
        print('Selected Images:', selected_images)
        submit(answer=selected_images, name=submit_file_name)
        # Thực hiện các hành động cần thiết với danh sách này
        return jsonify({'message': 'Selection received', 'submit_file_name': submit_file_name})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
