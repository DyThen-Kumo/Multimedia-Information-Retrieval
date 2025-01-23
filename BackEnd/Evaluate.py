from .Retrieval import *

def precision(true_positives, retrieved):
  return true_positives / retrieved if retrieved != 0 else 0

def recall(true_positives, relevant):
  return true_positives / relevant if relevant != 0 else 0

def f1_score(precision, recall):
  return 2 * precision * recall / (precision + recall)

def average_precision(relevant_items, retrieved_items):
  '''
  relevant_items: list các ID mà thực sự là đúng
  retrieved_items: list các ID được truy vấn trả về
  '''
  relevant_items = set(relevant_items)
  retrieved = 0
  true_positives = 0
  ap = 0

  for i, item in enumerate(retrieved_items):
    retrieved += 1
    if item in relevant_items:
      true_positives += 1
      ap += precision(true_positives, retrieved)

  return ap / len(relevant_items) if relevant_items else 0

def mean_average_precision(queries):
  aps = [average_precision(q[0], q[1]) for q in queries]
  return np.mean(aps) if aps else 0

# Hàm vẽ Precision-Recall Curve
def plot_precision_recall_curve(queries, tittle='Precision-Recall Curve'):
    plt.figure(figsize=(10, 6))

    for idx, (relevant_items, retrieved_items) in enumerate(queries):
        relevant_items = set(relevant_items)
        precision_vals = []
        recall_vals = []
        true_positives = 0

        # Tính Precision và Recall cho từng ngưỡng
        for i, item in enumerate(retrieved_items):
            if item in relevant_items:
                true_positives += 1
            p = precision(true_positives, i + 1)
            r = recall(true_positives, len(relevant_items))
            precision_vals.append(p)
            recall_vals.append(r)

        auc_score = auc(recall_vals, precision_vals)

        # Vẽ đường Precision-Recall cho từng truy vấn
        plt.plot(recall_vals, precision_vals, label=f'AUC = {auc_score:.2f}')

    # Cấu hình biểu đồ
    plt.title(tittle)
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.legend()
    plt.grid()
    plt.show()

def get_ground_truth(map_qr):
    ground_truths = []
    for query_name in map_qr:
        file_ok = os.path.join(gt_path, f"{query_name}_ok.txt")
        file_good = os.path.join(gt_path, f"{query_name}_good.txt")

        # Đọc dòng từ từng file
        lines_ok = load_file_lines(file_ok)
        lines_good = load_file_lines(file_good)

        # Gộp nội dung 2 file thành 1 danh sách
        merged_list = lines_good + lines_ok

        ground_truths.append(merged_list)

    return ground_truths

def get_MAP(ground_truths, rank_lists):
    queries = []
    for i in range(len(rank_lists)):
        relevant_items = ground_truths[i]
        retrieved_items = rank_lists[i]
        queries.append((relevant_items, retrieved_items))

    map = mean_average_precision(queries=queries)
    return map