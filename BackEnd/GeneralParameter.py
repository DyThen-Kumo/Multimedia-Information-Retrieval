from .Import import *

def set_parameter(_k = 6392, _retrain = True, _top_rerank = 10):
    k = _k
    retrain = _retrain
    top_rerank = _top_rerank

    return k, retrain, top_rerank

k, retrain, top_rerank = set_parameter()

current_file_path = os.path.abspath(__file__)
github_path = os.path.dirname(os.path.dirname(current_file_path)) # c:\Retrieval System\Multimedia-Information-Retrieval
project_path = os.path.dirname(github_path) # c:\Retrieval System\
gt_path = os.path.join(project_path, 'data', 'paris_120310_gt')
data_path = os.path.join(github_path, 'static', 'data', 'paris')

if retrain:
    features_path = os.path.join(project_path, 'features', 'features_paris_clip_3')
else:
    features_path = os.path.join(project_path, 'features', 'features_clip')


processor = CLIPProcessor.from_pretrained('openai/clip-vit-base-patch32')

if retrain:
    model = torch.load(r'C:\Retrieval System\model\paris_clip_3.pth', map_location=torch.device('cpu'))
else:
    model = CLIPModel.from_pretrained('openai/clip-vit-base-patch32')

model.eval()

transform = Compose([
    Resize((224, 224)),
    ToTensor(),
    Normalize((0.48145466, 0.4578275, 0.40821073), (0.26862954, 0.26130258, 0.27577711))
])