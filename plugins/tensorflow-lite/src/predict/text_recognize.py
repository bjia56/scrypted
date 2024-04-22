from __future__ import annotations

import asyncio
import concurrent.futures
from typing import Any, List, Tuple

import numpy as np
import scrypted_sdk
from PIL import Image

from predict import Prediction, PredictPlugin
from predict.craft_utils import normalizeMeanVariance
from predict.rectangle import Rectangle

from .craft_utils import adjustResultCoordinates, getDetBoxes

predictExecutor = concurrent.futures.ThreadPoolExecutor(1, "TextDetect")

class TextRecognition(PredictPlugin):
    def __init__(self, nativeId: str | None = None):
        super().__init__(nativeId=nativeId)

        self.inputheight = 640
        self.inputwidth = 640

        self.labels = {
            0: "text",
        }
        self.loop = asyncio.get_event_loop()
        self.minThreshold = 0.1

        self.detectModel = self.downloadModel("craft")


    def downloadModel(self, model: str):
        pass

    def predictDetectModel(self, input):
        pass

    async def detect_once(self, input: Image.Image, settings: Any, src_size, cvss) -> scrypted_sdk.ObjectsDetected:
        image_tensor = normalizeMeanVariance(np.array(input))
        # reshape to c w h
        image_tensor = image_tensor.transpose([2, 0, 1])
        # add extra dimension to tensor
        image_tensor = np.expand_dims(image_tensor, axis=0)

        y = await asyncio.get_event_loop().run_in_executor(
            predictExecutor, lambda: self.predictDetectModel(image_tensor)
        )

        estimate_num_chars = False
        ratio_h = ratio_w = 1
        text_threshold = .7
        link_threshold = .7
        low_text = .4
        poly = False

        boxes_list, polys_list = [], []
        for out in y:
            # make score and link map
            score_text = out[:, :, 0]
            score_link = out[:, :, 1]

            # Post-processing
            boxes, polys, mapper = getDetBoxes(
                score_text, score_link, text_threshold, link_threshold, low_text, poly, estimate_num_chars)
            if not len(boxes):
                continue

            # coordinate adjustment
            boxes = adjustResultCoordinates(boxes, ratio_w, ratio_h)
            polys = adjustResultCoordinates(polys, ratio_w, ratio_h)
            if estimate_num_chars:
                boxes = list(boxes)
                polys = list(polys)
            for k in range(len(polys)):
                if estimate_num_chars:
                    boxes[k] = (boxes[k], mapper[k])
                if polys[k] is None:
                    polys[k] = boxes[k]
            boxes_list.append(boxes)
            polys_list.append(polys)

        preds: List[Prediction] = []
        for boxes in boxes_list:
            for box in boxes:
                tl, tr, br, bl = box
                l = tl[0]
                t = tl[1]
                r = br[0]
                b = br[1]

                pred = Prediction(0, 1, Rectangle(l, t, r, b))
                preds.append(pred)
            
        return self.create_detection_result(preds, src_size, cvss)

    # width, height, channels
    def get_input_details(self) -> Tuple[int, int, int]:
        return (self.inputwidth, self.inputheight, 3)

    def get_input_size(self) -> Tuple[float, float]:
        return (self.inputwidth, self.inputheight)

    def get_input_format(self) -> str:
        return "rgb"