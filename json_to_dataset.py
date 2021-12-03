import argparse
import base64
import json
import os
import os.path as osp

import imgviz
import PIL.Image

from labelme.logger import logger
from labelme import utils


def main():
    logger.warning(
        "This script is aimed to demonstrate how to convert the "
        "JSON file to a single image dataset."
    )
    logger.warning(
        "It won't handle multiple JSON files to generate a "
        "real-use dataset."
    )

    parser = argparse.ArgumentParser()
    parser.add_argument("json_file")
    parser.add_argument("-o", "--out", default=None)
    args = parser.parse_args()

    json_file = args.json_file

    if args.out is None:
        out_dir = osp.basename(json_file).replace(".", "_")
        out_dir = osp.join(osp.dirname(json_file), out_dir)
    else:
        out_dir = args.out
    if not osp.exists(out_dir):
        os.mkdir(out_dir)

    # 为了批量处理的改动1，获得目录下所有的.json后缀文件
    path = []
    file_name = []
    for root, dirs, files in os.walk(json_file):  # 获取所有文件
        for file in files:  # 遍历所有文件名
            if os.path.splitext(file)[1] == '.json':  # 指定尾缀
                file_name.append(file.split('.')[0])   # 为了获取**.json中的**
                path.append(os.path.join(root, file))  # 拼接绝对路径并放入列表
    print('总文件数目：', len(path))

    # 为了批量处理改动2，都放入循环中
    for i in range(len(path)):
        data = json.load(open(path[i], encoding='UTF-8-sig'))
        imageData = data.get("imageData")

        if not imageData:
            imagePath = os.path.join(os.path.dirname(json_file), data["imagePath"])
            with open(imagePath, "rb") as f:
                imageData = f.read()
                imageData = base64.b64encode(imageData).decode("utf-8")
        img = utils.img_b64_to_arr(imageData)

        label_name_to_value = {"_background_": 0}
        for shape in sorted(data["shapes"], key=lambda x: x["label"]):
            label_name = shape["label"]
            if label_name in label_name_to_value:
                label_value = label_name_to_value[label_name]
            else:
                label_value = len(label_name_to_value)
                label_name_to_value[label_name] = label_value
        lbl, _ = utils.shapes_to_label(
            img.shape, data["shapes"], label_name_to_value
        )

        label_names = [None] * (max(label_name_to_value.values()) + 1)
        for name, value in label_name_to_value.items():
            label_names[value] = name

        lbl_viz = imgviz.label2rgb(
            label=lbl, img=imgviz.asgray(img), label_names=label_names, loc="rb"
        )

        # 改动3：下面加了四个filename,1和2都是为了输出的时候名字改变
        PIL.Image.fromarray(img).save(osp.join(out_dir, file_name[i]+".png"))
        utils.lblsave(osp.join(out_dir, file_name[i]+"_label.png"), lbl)
        PIL.Image.fromarray(lbl_viz).save(osp.join(out_dir, file_name[i]+"_label_viz.png"))

        with open(osp.join(out_dir, file_name[i]+"label_names.txt"), "w") as f:
            for lbl_name in label_names:
                f.write(lbl_name + "\n")

        logger.info("Saved to: {}".format(out_dir))



if __name__ == "__main__":
    main()
