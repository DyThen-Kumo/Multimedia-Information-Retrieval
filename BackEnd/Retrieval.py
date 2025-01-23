from .LoadDatabase import *

def retrieval_top_k_by_index(query, index, map_db, k=5):
    os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
    top_k_similarities, top_k_indices = index.search(query, k)
    os.environ["KMP_DUPLICATE_LIB_OK"] = "FALSE"

    top_k = []
    for i in range(top_k_indices.shape[0]):
        top_k.append([map_db[j] for j in top_k_indices[i]])

    return top_k, top_k_similarities.tolist()

def retrieval_top_k_by_features(query, database, map_db, k=5):
    similarity_matrix = cosine_similarity(query, database)

    sorted_similarity_indices = np.argsort(similarity_matrix, axis=1)[:, ::-1] # Sắp xếp giảm dần

    top_k = []
    top_k_similarities = []

    for i in range(sorted_similarity_indices.shape[0]):
        top_k_indices = sorted_similarity_indices[i][:k]
        top_k.append([map_db[j] for j in top_k_indices])  # Lấy các đối tượng tương ứng
        top_k_similarities.append(similarity_matrix[i][top_k_indices])  # Lấy cosine similarity

    return top_k, top_k_similarities

def retrieval_threshold_by_features(query, database, map_db, threshold=0.8):
    # Tính toán ma trận cosine similarity
    similarity_matrix = cosine_similarity(query, database)

    # Sắp xếp các chỉ số giảm dần của cosine similarity
    sorted_similarity_indices = np.argsort(similarity_matrix, axis=1)[:, ::-1]

    # Khởi tạo danh sách trả về
    filtered_map_db = []
    filtered_similarities = []

    # Duyệt qua từng query và lọc các kết quả có cosine similarity > threshold
    for i in range(similarity_matrix.shape[0]):
        # Lấy các chỉ số có độ tương đồng lớn hơn threshold
        valid_indices = sorted_similarity_indices[i][similarity_matrix[i, sorted_similarity_indices[i]] > threshold]
        filtered_map_db.append([map_db[j] for j in valid_indices])  # Lấy các đối tượng tương ứng
        filtered_similarities.append(similarity_matrix[i, valid_indices])  # Lấy cosine similarity

    return filtered_map_db, filtered_similarities
