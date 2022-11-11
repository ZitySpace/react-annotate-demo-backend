from enum import Enum
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import json

app = FastAPI()
anno_router = r = APIRouter()


instances = json.load(open('./data/instance_coco_val2017_zity_fmt_mini.json', 'rb'))
keypoints = json.load(open('./data/keypoints_coco_val2017_zity_fmt_mini.json', 'rb'))


class Task(str, Enum):
    detection = 'detection'
    segmentation = 'segmentation'
    keypoints = 'keypoints'
    detection_segmentation = 'detection+segmentation'
    keypoints_segmentation = 'keypoints+segmentation'


@r.get('/{task}')
def get_annotations(task: Task):

    anno = []
    if task == Task.detection:

        anno = [
            {
                k
                if k != 'file_name'
                else 'name': v
                if k != 'annotations'
                else [
                    {
                        'category': instance_anno['category'],
                        **dict(zip(['x', 'y', 'w', 'h'], instance_anno['bbox'])),
                    }
                    for instance_anno in v
                ]
                for k, v in img_anno.items()
            }
            for img_anno in instances
        ]

    if task == Task.segmentation:
        pass

    if task == Task.keypoints:
        pass

    if task == Task.detection_segmentation:
        pass

    if task == Task.keypoints_segmentation:
        pass

    return anno


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


app.include_router(anno_router, prefix='/annotations')


if __name__ == '__main__':
    uvicorn.run('serv:app', host='0.0.0.0', port=8080, reload=True)
