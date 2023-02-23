# vaik-text-recognition-tflite-experiment

Create json file by text recognition model. Calc Levenshtein ratio.

## Install

```shell
pip install -r requirements.txt
```

## Docker Install

```shell
sudo apt-get update && sudo apt-get upgrade
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```

### aarch64(a1.medium) without coral

```shell
sudo docker build -t a1_medium_experiment -f ./Dockerfile.a1_medium .
sudo docker run --name a1_medium_experiment_container \
           --rm \
           -v ~/output_tflite_model:/workspace/output_tflite_model \
           -v $(pwd):/workspace/source \
           -it a1_medium_experiment /bin/bash
```

### armv7l(raspberry pi 4b) without coral

```shell
sudo docker build -t raspberry4b_experiment -f ./Dockerfile.raspberrypib4 .
sudo docker run --name raspberry4b_experiment_container \
           --rm \
           -v ~/output_tflite_model:/workspace/output_tflite_model \
           -v $(pwd):/workspace/source \
           -it raspberry4b_experiment /bin/bash
```

### armv7l(raspberry pi 4b) with coral

```shell
sudo docker build -t raspberry4b_experiment -f ./Dockerfile.raspberrypib4 .
sudo docker run --name raspberry4b_experiment_container \
           --rm \
           --privileged \
           -v ~/output_tflite_model:/workspace/output_tflite_model \
           -v $(pwd):/workspace/source \
           -v /dev/bus/usb:/dev/bus/usb \
           -it raspberry4b_experiment /bin/bash
```

---------

## Usage

### Create json file

```shell
python3 inference.py --input_tflite_model_path '/workspace/output_tflite_model/model.tflite' \
                --input_classes_json_path '/workspace/source/test_default_fonts_images/jpn_character.json' \
                --input_image_dir_path '/workspace/source/test_default_fonts_images' \
                --output_json_dir_path '/workspace/output_tflite_model/test_default_fonts_images_out'
```

- input_image_dir_path
    - example

```shell
.
├── なにわ_3932.png
├── 京都_0656.png
├── 倉敷_0488.png
・・・
```

#### Output
- output_json_dir_path
    - example

```json
{
  "answer": "いわき",
  "classes": [
    113,
    155,
    118
  ],
  "image_path": "/workspace/source/test_default_fonts_images/いわき_00122.jpg",
  "scores": 1.1269535508079428e-23,
  "text": "いわき"
}
```
-----

### Calc Levenshtein Ratio

```shell
python calc_levenshtein_ratio.py --input_json_dir_path '~/output_tflite_model/test_default_fonts_images_inference'
```

#### Output

``` text
ratio:1.0, answer:佐世保, predict:佐世保
ratio:1.0, answer:とちぎ, predict:とちぎ
ratio:1.0, answer:いわき, predict:いわき
ratio:1.0, answer:大分, predict:大分
ratio:1.0, answer:三重, predict:三重
ratio:1.0, answer:八王子, predict:八王子
ratio:1.0, answer:名古屋, predict:名古屋
ratio:1.0, answer:徳島, predict:徳島
ratio:1.0, answer:つくば, predict:つくば
ratio:1.0, answer:宮崎, predict:宮崎
ratio:1.0, answer:宇都宮, predict:宇都宮
ratio:1.0, answer:久留米, predict:久留米
ratio:1.0, answer:尾張小牧, predict:尾張小牧
ratio:1.0, answer:保劣跡幡, predict:保劣跡幡
ratio:1.0, answer:湘南, predict:湘南
ratio:1.0, answer:佐世保, predict:佐世保
ratio:0.6666666666666667, answer:術匹題, predict:術四題
ratio:1.0, answer:和泉, predict:和泉
ratio:1.0, answer:和歌山, predict:和歌山
ratio:1.0, answer:姫路, predict:姫路
ratio:1.0, answer:凄魂, predict:凄魂
ratio:1.0, answer:北九州, predict:北九州
Average Ratio: 0.9848484848484849
```