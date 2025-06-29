from .Import import *

current_file_path = os.path.abspath(__file__)
github_path = os.path.dirname(os.path.dirname(current_file_path)) # c:\Retrieval System\Multimedia-Information-Retrieval
project_path = os.path.dirname(github_path) # c:\Retrieval System\
gt_path = os.path.join(project_path, 'data', 'paris_120310_gt')
data_path = os.path.join(github_path, 'static', 'data', 'paris')
# data_path = os.path.join(github_path, 'static', 'paris')

def set_parameter(_use_index = False, 
                  _index_path=os.path.join(github_path, 'index', 'feature_clip.pkl'), 
                  _retrain = False, 
                  ):
    global use_index
    global retrain
    global index_path
    global features_path
    global model

    if _use_index:
        index_path = _index_path
    if _retrain:
        features_path = os.path.join(project_path, 'features', 'features_paris_clip_3')
        print('Model đã re train!!')
        model = torch.load(r'C:\Retrieval System\model\paris_clip_3.pth', map_location=torch.device('cpu'))
    else:
        features_path = os.path.join(project_path, 'features', 'features_clip')
        model = CLIPModel.from_pretrained('openai/clip-vit-base-patch32')
    model.eval()
    print('Thay đổi thành công')
    return

use_index, retrain = True, True
# set_parameter()

print(use_index, retrain)
index_path = os.path.join(github_path, 'index', 'IndexIVFFlat_paris_clip.pkl')

if retrain:
    features_path = os.path.join(project_path, 'features', 'features_paris_clip_3')
else:
    features_path = os.path.join(project_path, 'features', 'features_clip')


processor = CLIPProcessor.from_pretrained('openai/clip-vit-base-patch32')

model = None
if retrain:
    print('Model đã re train!!')
    print('Feature path:',features_path)
    model = torch.load(r'C:\Retrieval System\model\paris_clip_3.pth', map_location=torch.device('cpu'))
else:
    print('Feature path:',features_path)
    model = CLIPModel.from_pretrained('openai/clip-vit-base-patch32')

model.eval()

transform = Compose([
    Resize((224, 224)),
    ToTensor(),
    Normalize((0.48145466, 0.4578275, 0.40821073), (0.26862954, 0.26130258, 0.27577711))
])