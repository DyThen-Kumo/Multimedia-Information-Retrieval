from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
from BackEnd.post_images import *
import os

app = Flask(__name__)
upload_folder = os.path.join('static', 'uploads')
app.config['UPLOAD_FOLDER'] = upload_folder
delay_pic = os.path.join(AIC2024_dir,'static','img','avatar.png') # 'D:\CLB-AI\AIC2024\static\img\avatar.png'
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
@app.route('/regular-search')
def render_regular_search():
    return render_template('Regular-Search.html')

@app.route('/relative-search')
def render_relative_search():
    return render_template('Relative-Search.html')

@app.route('/sequence-search')
def render_sequence_search():
    return render_template('Sequence-Search.html')

# Tab Generate
@app.route('/generative-text')
def render_generative_text():
    return render_template('Generative-Text.html')

@app.route('/generative-image')
def render_generative_image():
    return render_template('Generative-Image.html')

@app.route('/read-keyframes')
def render_read_keyframes():
    return render_template('Read-Keyframes.html')

# Đọc data
@app.route('/get-read-keyframes', methods=['POST'])
def get_read_keyframes():
    video_name = request.form.get('video_name')
    print(video_name)

    image_files = read_keyframes(video_name=video_name)
    image_urls = [url for url in image_files]
    return jsonify(image_urls)

# Quick Answer
@app.route('/quick-answer', methods=['POST'])
def quick_answer():
    submit_name = request.form.get('submit_name')
    video_name = request.form.get('video_name')
    number_start = int(request.form.get('number_start'))
    number_end = int(request.form.get('number_end'))
    
    add_quick_answer(submit_name, video_name, number_start, number_end)

    # Trả về phản hồi thành công cho front-end
    return jsonify("message: Form submitted successfully!")

# Search ảnh
@app.route('/get-regular-images', methods=['POST'])
def get_regular_images():
    num_images = request.form.get('num_images')
    language = request.form.get('language')
    input_text = request.form.get('input_text')

    input_data = (num_images, language, input_text)
    image_files = post_regular_images(input_data)
    image_urls = [url for url in image_files]
    return jsonify(image_urls)

@app.route('/get-relative-images', methods=['POST'])
def get_relative_images():
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

@app.route('/get-sequence-images', methods=['POST'])
def get_sequence_images():
    num_images = request.form.get('num_images')
    num_querry = request.form.get('num_querry')
    language = request.form.get('language')
    input_text = request.form.get('input_text')

    input_data = (num_querry, num_images, language, input_text)
    print(input_data)
    image_files = post_sequence_images(input_data)
    image_urls = [url for url in image_files]
    return jsonify(image_urls)


# Generate ảnh
@app.route('/get-generative-text', methods=['POST'])
def get_generative_text():
    language = request.form.get('language')
    input_text = request.form.get('input_text')
    if language == 'vi':
        input_text = trans(text_input=input_text)
    image_urls = [post_generative_text(input_text)]
    # image_urls = [url for url in image_files]
    return jsonify(image_urls)

@app.route('/get-generative-images', methods=['POST'])
def get_generative_images():
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
