import argparse
import os
import glob
import json
import Levenshtein


def calc_levenshtein_ratio(json_dict_list):
    ratio_list = []
    for json_dict in json_dict_list:
        ratio = Levenshtein.ratio(json_dict['answer'], json_dict['text'][0])
        print(f'ratio:{ratio}, answer:{json_dict["answer"]}, predict:{json_dict["text"][0]}')
        ratio_list.append(ratio)
    print(f'Average Ratio: {sum(ratio_list)/len(ratio_list)}')


def main(input_json_dir_path):
    json_path_list = glob.glob(os.path.join(input_json_dir_path, '*.json'))
    json_dict_list = []
    for json_path in json_path_list:
        with open(json_path, 'r') as f:
            json_dict = json.load(f)
            json_dict_list.append(json_dict)
    calc_levenshtein_ratio(json_dict_list)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='expeirment')
    parser.add_argument('--input_json_dir_path', type=str,
                        default='~/.vaik_text_recognition_tflite_experiment/test_default_fonts_images_inference')
    args = parser.parse_args()

    args.input_json_dir_path = os.path.expanduser(args.input_json_dir_path)

    main(**args.__dict__)
