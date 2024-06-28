from flask import Flask, request, jsonify  
import os  
from ultralytics import YOLO
import json

model = YOLO("models/best.pt")
def class_name_convert(class_name):
    converted_class_name = class_name
    if class_name == "mouse_bite":
        converted_class_name = "Mouse_bite"
    elif class_name == "open_circuit":
        converted_class_name = "Open_circuit"
    elif class_name == "short":
        converted_class_name = "Short"
    elif class_name == "spur":
        converted_class_name = "Spur"
    elif class_name == "spurious_copper":
        converted_class_name = "Spurious_copper"
    elif class_name == "missing_hole":
        converted_class_name = "Missing_hole"
    return converted_class_name
  
app = Flask(__name__)  
UPLOAD_FOLDER = '/tmp'  # 指定上传文件保存的路径  
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER  
  
@app.route('/', methods=['POST'])  
def upload_file():  
    if 'images' not in request.files:  
        return jsonify({'error': 'No file part in the request'}), 400  
  
    files = request.files.getlist('images')  
  
    uploaded_files = []  
    for file in files:  
        if file.filename == '':  
            continue  # 跳过空文件  
  
        filename = file.filename  
        # 为了安全起见，你可以使用secure_filename来避免潜在的文件名冲突或安全问题  
        # filename = secure_filename(file.filename)  
  
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)  
        file.save(file_path)  
        uploaded_files.append(file_path)  

    
    results = model(uploaded_files)

    detect_results = {
        "detection_classes": [],
        "detection_boxes": [],
        "detection_scores": []
    }
      
    for result in results:
        json_results = json.loads(result.tojson())
        for box_result in json_results:
           class_name = box_result["name"]
           if class_name != "mouse_bite" and class_name != "open_circuit" and class_name != "short" and class_name != "spur" and class_name != "spurious_copper":
                continue
           converted_class_name = class_name_convert(class_name)
           detect_results["detection_classes"].append(converted_class_name)
           detect_results["detection_boxes"].append([box_result["box"]["y1"],box_result["box"]["x1"],box_result["box"]["y2"],box_result["box"]["x2"]])
           detect_results["detection_scores"].append(box_result["confidence"])

  
    return jsonify(detect_results), 200  
  
if __name__ == '__main__':  
    # 确保上传文件夹存在  
    if not os.path.exists(UPLOAD_FOLDER):  
        os.makedirs(UPLOAD_FOLDER)  
  
    # 运行应用，指定端口为8080  
    app.run(host='0.0.0.0', port=8080, debug=True)
