from BackEnd.ReRanking import *
from googletrans import Translator

# Khởi tạo mô hình dịch
translator = Translator()
print('Khởi tạo mô hình dịch thành công')
# Hàm đổi input sang tiếng Anh
def trans(text_input):
    result = translator.translate(str(text_input), src='vi', dest='en')
    return result.text

def post_retrieval_by_text(input_data):
    text_query = input_data[2] # input text
    topk = int(input_data[0]) # number images
    language = input_data[1]
    if language == 'vi':
        text_query = trans(text_input=text_query)
    print(text_query)

    return

def post_retrieval_by_image(input_data):
    topk = int(input_data[0])
    file_path = input_data[1]

    query = np.array(get_image_features([file_path]))
    print('Query shape:',query.shape)

    if load_index:
        index, map_index = load_index(index_path=index_path)
        rank_list, similarity_matrix - retrieval_top_k_by_index(query=query, index=index, map_db=map_index, k=topk)
    else:
        database, map_db = load_features()
        rank_list, similarity_matrix = retrieval_top_k_by_features(query=query, database=database, map_db=map_db, k=topk)

    results = []
    for image in rank_list[0]:
        image_name = f'{image}.jpg'
        folder = image.split('_')[-2]
        results.append(os.path.join(data_path, folder, image_name))

    return results, similarity_matrix

def post_retrieval_by_text(input_data):
    text_query = input_data[2] # input text
    topk = int(input_data[0]) # number images
    language = input_data[1]
    if language == 'vi':
        text_query = trans(text_input=text_query)

    query = np.array([get_text_features([text_query])])
    print('Query shape:',query.shape)

    if load_index:
        index, map_index = load_index(index_path=index_path)
        rank_list, similarity_matrix - retrieval_top_k_by_index(query=query, index=index, map_db=map_index, k=topk)
    else:
        database, map_db = load_features()
        rank_list, similarity_matrix = retrieval_top_k_by_features(query=query, database=database, map_db=map_db, k=topk)

    results = []
    for image in rank_list[0]:
        image_name = f'{image}.jpg'
        folder = image.split('_')[-2]
        results.append(os.path.join(data_path, folder, image_name))

    return results, similarity_matrix


