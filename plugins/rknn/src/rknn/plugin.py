import asyncio
import concurrent.futures
import os
import platform
import threading
import traceback
from typing import Any, Coroutine, List, Tuple
import urllib.request

import numpy as np
from PIL.Image import Image
from rknnlite.api import RKNNLite

from common.yolo import parse_yolov9
from predict import PredictPlugin, Prediction
from predict.rectangle import Rectangle

import scrypted_sdk
from scrypted_sdk import DeviceProvider, ScryptedDeviceType, ScryptedInterface

# for Rockchip-optimized models, the postprocessing is slightly different from the original models
from .optimized.yolo import post_process, IMG_SIZE, CLASSES

from .text_recognition import TEXT_RECOGNITION_NATIVE_ID, RKNNTextRecognition


rknn_verbose = False
lib_download = 'https://github.com/airockchip/rknn-toolkit2/raw/v2.0.0-beta0/rknpu2/runtime/Linux/librknn_api/aarch64/librknnrt.so'
model_download_tmpl = 'https://github.com/bjia56/scrypted-rknn/raw/main/models/{}_{}_optimized.rknn'
lib_path = '/usr/lib/librknnrt.so'


def ensure_compatibility_and_get_cpu():
    err_msg = 'RKNN plugin is only supported on Linux/ARM64 platform with a Rockchip CPU'
    if platform.machine() != 'aarch64':
        raise RuntimeError(err_msg)

    if platform.system() != 'Linux':
        raise RuntimeError(err_msg)

    try:
        with open('/proc/device-tree/compatible') as f:
            device_compatible_str = f.read()
            if 'rk3562' in device_compatible_str:
                return 'rk3562'
            elif 'rk3566' in device_compatible_str:
                return 'rk3566'
            elif 'rk3568' in device_compatible_str:
                return 'rk3568'
            elif 'rk3576' in device_compatible_str:
                return 'rk3576'
            elif 'rk3588' in device_compatible_str:
                return 'rk3588'
            else:
                raise RuntimeError(err_msg)
    except IOError as e:
        print('Failed to read /proc/device-tree/compatible: {}'.format(e))
        print('If you are running this via Docker, ensure you are launching the container with --privileged option')
        raise


class RKNNPlugin(PredictPlugin, DeviceProvider):
    labels = {0: "person", 1: "vehicle", 2: "animal"}#{i: CLASSES[i] for i in range(len(CLASSES))}
    rknn_runtimes: dict
    executor: concurrent.futures.ThreadPoolExecutor
    text_recognition: RKNNTextRecognition = None
    cpu: str

    def __init__(self, nativeId=None):
        super().__init__(nativeId)
        self.cpu = ensure_compatibility_and_get_cpu()
        self.modelName = 'yolov6n'

        self.rknn_runtimes = {}

        if not os.path.exists(lib_path):
            installation = os.environ.get('SCRYPTED_INSTALL_ENVIRONMENT')
            if installation in ('docker', 'lxc'):
                print('Downloading librknnrt.so from {}'.format(lib_download))
                urllib.request.urlretrieve(lib_download, lib_path)
            else:
                raise RuntimeError('librknnrt.so not found. Please download it from {} and place it at {}'.format(lib_download, lib_path))

        model_download = "https://github.com/bjia56/actions-experiments/releases/download/test/scrypted_yolov9t_relu_320_RK3588_320x320.rknn"#model_download_tmpl.format(self.modelName, self.cpu)
        model_file = os.path.basename(model_download)
        model_path = self.downloadFile(model_download, model_file)
        print('Using model {}'.format(model_path))

        test_rknn = RKNNLite(verbose=rknn_verbose)
        ret = test_rknn.load_rknn(model_path)
        if ret != 0:
            raise RuntimeError('Failed to load model: {}'.format(ret))

        ret = test_rknn.init_runtime()
        if ret != 0:
            raise RuntimeError('Failed to init runtime: {}'.format(ret))
        test_rknn.release()

        def executor_initializer():
            thread_name = threading.current_thread().name
            rknn = RKNNLite(verbose=rknn_verbose)
            ret = rknn.load_rknn(model_path)
            if ret != 0:
                raise RuntimeError('Failed to load model: {}'.format(ret))

            ret = rknn.init_runtime()
            if ret != 0:
                raise RuntimeError('Failed to init runtime: {}'.format(ret))

            self.rknn_runtimes[thread_name] = rknn
            print('RKNNLite runtime initialized on thread {}'.format(thread_name))

        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=3, thread_name_prefix=type(self).__name__, initializer=executor_initializer)

        asyncio.create_task(self.discoverRecognitionModels())

    async def discoverRecognitionModels(self) -> None:
        devices = [
            {
                "nativeId": TEXT_RECOGNITION_NATIVE_ID,
                "name": "Rockchip NPU Text Recognition",
                "type": ScryptedDeviceType.API.value,
                "interfaces": [
                    ScryptedInterface.ObjectDetection.value,
                ],
            }
        ]
        await scrypted_sdk.deviceManager.onDevicesChanged({
            "devices": devices,
        })

    async def getDevice(self, nativeId: str) -> RKNNTextRecognition:
        try:
            if nativeId == TEXT_RECOGNITION_NATIVE_ID:
                self.text_recognition = self.text_recognition or RKNNTextRecognition(self, nativeId, self.cpu)
                return self.text_recognition
        except:
            traceback.print_exc()
            raise

    def get_input_details(self) -> Tuple[int]:
        return (320, 320, 3)

    def get_input_size(self) -> Tuple[int, int]:
        return (320, 320)

    async def detect_once(self, input: Image, settings: Any, src_size, cvss) -> Coroutine[Any, Any, Any]:
        def inference(input_tensor):
            rknn = self.rknn_runtimes[threading.current_thread().name]
            outputs = rknn.inference(inputs=[input_tensor])
            return outputs

        async def predict(input_tensor):
            fut = asyncio.wrap_future(self.executor.submit(inference, input_tensor))
            outputs = np.array(await fut)
            outputs = outputs.squeeze()
            print(f"outputs shape: {outputs.shape}")
            predictions = parse_yolov9(outputs)
            """
            boxes, classes, scores = post_process(outputs)


            predictions: List[Prediction] = []
            for i in range(len(classes)):
                #print(CLASSES[classes[i]], scores[i])
                predictions.append(Prediction(
                    classes[i],
                    float(scores[i]),
                    Rectangle(float(boxes[i][0]), float(boxes[i][1]), float(boxes[i][2]), float(boxes[i][3]))
                ))
            """
            print(predictions)
            return self.create_detection_result(predictions, src_size, cvss)
        input_tensor = np.expand_dims(np.asarray(input), axis=0)
        input_tensor = input_tensor.transpose((0, 3, 1, 2))
        input_tensor = input_tensor.astype(np.float32) / 255.0
        input_tensor = np.ascontiguousarray(input_tensor)
        return await predict(input_tensor)
