from .Evaluate import *

def merge_results_by_ranx(list_rank_list, list_similarity_matrix, method='rrf'): # Merge kết quả của từng query.
  # Chuyển đổi dữ liệu sang dạng dictionary
  runs = []
  for i, (res, sims) in enumerate(zip(list_rank_list, list_similarity_matrix)):
      query_id = f"query_0"
      run_data = {str(doc_id): score for doc_id, score in zip(res, sims)}
      run = Run({query_id: run_data})
      runs.append(run)
  # Hợp nhất kết quả
  fused_run = fuse(runs, method=method)  # Có thể điều chỉnh weights nếu cần

  fused_ranking_results = {}

  for query_id, docs in fused_run.to_dict().items():
      fused_ranking_results[query_id] = list(docs.keys())  # Lấy danh sách document IDs (không cần điểm số)

  return fused_ranking_results['query_0']

def get_new_ranklist_by_features(list_images, database, map_db, k):
    # new_rank_list = []

    new_query = np.array(get_image_features(get_path(list_images)))
    print('New query shape:', new_query.shape)
    print('Database shape: ', database.shape)
    list_rank_list, list_similarity_matrix = retrieval_top_k_by_features(query=new_query, database=database, map_db=map_db, k=k)
    new_rank_list = merge_results_by_ranx(list_rank_list, list_similarity_matrix, method='mnz')
    # new_rank_list.append(each_rank_list)

    return new_rank_list[:k]

def get_new_ranklist_by_index(list_images, index, map_index, k):
    # new_rank_list = []

    new_query = np.array(get_image_features(get_path(list_images)))
    print('New query shape:', new_query.shape)
    list_rank_list, list_similarity_matrix = retrieval_top_k_by_index(query=new_query, index=index, map_db=map_index, k=k)
    new_rank_list = merge_results_by_ranx(list_rank_list, list_similarity_matrix, method='mnz')
    # new_rank_list.append(each_rank_list)

    return new_rank_list[:k]