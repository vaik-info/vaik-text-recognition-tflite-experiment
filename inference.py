import argparse
import os
import glob
import json

from vaik_text_recognition_tflite_inference.tflite_model import TfliteModel
from PIL import Image
import numpy as np


def main(input_tflite_model_path, input_classes_json_path, input_image_dir_path, output_json_dir_path,
         softmax_threshold):
    os.makedirs(output_json_dir_path, exist_ok=True)
    classes = TfliteModel.char_json_read(input_classes_json_path)
    model = TfliteModel(input_tflite_model_path, classes, softmax_threshold=softmax_threshold)

    types = ('*.jpg', '*.jpeg', '*.png', '*.JPG', '*.JPEG', '*.PNG')
    image_path_list = []
    for files in types:
        image_path_list.extend(glob.glob(os.path.join(input_image_dir_path, '**', files), recursive=True))
    image_list = []
    for image_path in image_path_list:
        image = np.asarray(Image.open(image_path).convert('RGB'))
        image_list.append(image)

    output, raw_pred = model.inference(image_list[6])

    output_list = []
    time_list = []
    import time
    for image in image_list:
        start = time.time()
        output, raw_pred = model.inference(image)
        end = time.time()
        output_list.append(output)
        time_list.append(end - start)

    for image_path, output in zip(image_path_list, output_list):
        output_json_path = os.path.join(output_json_dir_path,
                                        os.path.splitext(os.path.basename(image_path))[0] + '.json')
        output['answer'] = os.path.basename(image_path).split('_')[0]
        output['image_path'] = image_path
        with open(output_json_path, 'w') as f:
            json.dump(output, f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))
    print(f'{np.average(time_list)}[images/sec]')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='inference')
    parser.add_argument('--input_tflite_model_path', type=str,
                        default='~/.vaik_text_recognition_pb_exporter/model.tflite')
    parser.add_argument('--input_classes_json_path', type=str,
                        default=os.path.join(os.path.dirname(__file__), 'test_default_fonts_images/jpn_character.json'))
    parser.add_argument('--input_image_dir_path', type=str,
                        default=os.path.join(os.path.dirname(__file__), 'test_default_fonts_images'))
    parser.add_argument('--output_json_dir_path', type=str,
                        default='~/.vaik_text_recognition_tflite_experiment/test_default_fonts_images_inference')
    parser.add_argument('--softmax_threshold', type=float, default=0.00)
    args = parser.parse_args()

    args.input_tflite_model_path = os.path.expanduser(args.input_tflite_model_path)
    args.input_classes_json_path = os.path.expanduser(args.input_classes_json_path)
    args.input_image_dir_path = os.path.expanduser(args.input_image_dir_path)
    args.output_json_dir_path = os.path.expanduser(args.output_json_dir_path)

    main(**args.__dict__)
