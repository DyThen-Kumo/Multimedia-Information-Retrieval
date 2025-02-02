from BackEnd.ReRanking import *
from googletrans import Translator

# Khởi tạo mô hình dịch
translator = Translator()
print('Khởi tạo mô hình dịch thành công')
# Hàm đổi input sang tiếng Anh
def trans(text_input):
    result = translator.translate(str(text_input), src='vi', dest='en')
    return result.text

def post_retrieval_by_image(input_data):
    topk = int(input_data[0])
    file_path = input_data[1]

    print(file_path)

    query = np.array(get_image_features([file_path]))
    print('Query shape:',query.shape)

    rank_list, similarity_matrix = None, None
    if use_index:
        print('Searching by Index')
        index, map_index = load_index(index_path=index_path)
        rank_list, similarity_matrix = retrieval_top_k_by_index(query=query, index=index, map_db=map_index, k=topk)
    else:
        print('Searching by Features')
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

    print(text_query)
    query = np.array([get_text_features([text_query])]) if get_text_features([text_query]).shape == (512,) else np.array(get_text_features([text_query]))
    print('Query shape:',query.shape)

    rank_list, similarity_matrix = None, None
    if use_index:
        index, map_index = load_index(index_path=index_path)
        rank_list, similarity_matrix = retrieval_top_k_by_index(query=query, index=index, map_db=map_index, k=topk)
    else:
        database, map_db = load_features()
        rank_list, similarity_matrix = retrieval_top_k_by_features(query=query, database=database, map_db=map_db, k=topk)

    results = []
    for image in rank_list[0]:
        image_name = f'{image}.jpg'
        folder = image.split('_')[-2]
        results.append(os.path.join(data_path, folder, image_name))

    return results, similarity_matrix

def post_rerank(list_images, k):
    if use_index:
        index, map_index = load_index(index_path=index_path)
        rank_list = get_new_ranklist_by_index(list_images=list_images, index=index, map_index=map_index, k=k)
    else:
        database, map_db = load_features()
        rank_list = get_new_ranklist_by_features(list_images=list_images, database=database, map_db=map_db, k=k)

    print(rank_list)
    results = []
    for image in rank_list:
        image_name = f'{image}.jpg'
        folder = image.split('_')[-2]
        results.append(os.path.join(data_path, folder, image_name))

    return results
