import os
import logging
import pyautogui
from paddleocr import PaddleOCR
from PIL import Image, ImageDraw
from ERP_PO.Website.test_case.model.DataManage import Data

# 设置日志
logging.basicConfig(level=logging.INFO)
# 定义缓存字典
_csv_cache = {}

# 动态路径设置
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../.."))
OCR_SCREENSHOT_DIR = os.path.join(PROJECT_ROOT, "ERP_PO", "Website", "test_report", "screenshot", "ocr")
os.makedirs(OCR_SCREENSHOT_DIR, exist_ok=True)


def read_csv(temp_path: Data, l: int):
    """
    从 CSV 文件中读取指定行数据，并使用缓存机制避免重复打开文件
    :param temp_path: 数据路径对象，包含 .path 属性
    :param l: 行号（从0开始）
    :return: 指定行的数据列表
    """
    file_path = temp_path.path

    # 如果文件路径不在缓存中，则读取并缓存全部内容
    if file_path not in _csv_cache:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                # 一次性读取所有行并缓存
                _csv_cache[file_path] = [line.strip().split(',') for line in f.readlines()]
        except Exception as e:
            raise IOError(f"读取 CSV 文件失败: {file_path}, 错误: {e}")

    # 获取缓存中的数据
    cached_data = _csv_cache[file_path]

    # 检查索引是否越界
    if l >= len(cached_data) or l < 0:
        raise IndexError(f"CSV 文件行号越界: 请求第 {l} 行，但文件只有 {len(cached_data)} 行")

    return cached_data[l]



def screenshot(driver, name):
    driver.get_screenshot_as_file(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "..", "..", "..", "test_report", "screenshot", name
        )
    )


def init_ocr():
    """按需初始化 OCR 模型"""
    return PaddleOCR(
        lang='ch',
        show_log=True,
        use_angle_cls=True,  # 启用角度分类器
        det=True,  # 开启检测
        rec=True,  # 开启识别
        cls=True,  # 开启分类
        use_gpu=True,  # 是否使用 GPU（根据环境选择）
        drop_score=0.7  # 降低置信度阈值，识别更多内容
    )


def process_and_recognize(image_path, ocr_instance, output_dir=None):
    """
    使用传入的 OCR 实例进行识别
    :param image_path: 图像路径
    :param ocr_instance: 已初始化的 OCR 引擎（如 PaddleOCR）
    :param output_dir: 输出目录
    """
    result = ocr_instance.ocr(image_path, cls=True)
    if isinstance(result, list) and len(result) > 0 and isinstance(result[0], list):
        result = result[0]

    boxes = [line[0] for line in result]
    texts = [line[1][0] for line in result]
    scores = [line[1][1] for line in result]

    print("OCR识别结果:", texts)

    # 绘制边界框用于调试
    img = Image.open(image_path).convert("RGB")
    draw = ImageDraw.Draw(img)

    for box in boxes:
        flat_box = []
        for point in box:
            # 确保每个点是可迭代的坐标
            if isinstance(point, (list, tuple)) and len(point) >= 2:
                x, y = point[0], point[1]
            else:
                x, y = 0, 0  # 默认为 0 坐标
            # 强制转换为整数
            try:
                x = int(float(x))
                y = int(float(y))
            except (ValueError, TypeError):
                x, y = 0, 0
            flat_box.extend([x, y])

        draw.polygon(flat_box, outline="red", width=2)

    bounding_box_path = os.path.join(output_dir or OCR_SCREENSHOT_DIR, "ocr_bounding_boxes.png")
    img.save(bounding_box_path)

    return {
        'text': texts,
        'boxes': boxes,
        'scores': scores
    }



def click_element_by_text(content, offset=(0, 0), roi=None, timeout=10):
    """
    自动截图 → OCR 识别 → 查找关键词 → 点击该位置
    :param content: 要查找的关键词
    :param offset: 点击偏移量 (x_offset, y_offset)
    :param roi: 屏幕截图区域 (x, y, width, height)
    :param timeout: 最大等待时间（秒）
    :return: 是否成功点击
    """
    import time

    start_time = time.time()
    # 初始化 OCR 实例
    ocr_engine = init_ocr()  # 确保 det=True 和 rec=True
    print(f"OCR模型参数: {ocr_engine.args}")

    while time.time() - start_time < timeout:
        try:
            # 截图
            screen = pyautogui.screenshot(region=roi) if roi else pyautogui.screenshot()
            screenshot_path = os.path.join(OCR_SCREENSHOT_DIR, "ocr_screenshot.png")
            screen.save(screenshot_path)

            print(f"已保存截图至: {screenshot_path}")

            # 使用 OCR 识别
            result = process_and_recognize(screenshot_path, ocr_engine, OCR_SCREENSHOT_DIR)
            texts = result.get('text', [])
            boxes = result.get('boxes', [])

            print("OCR原始输出结构:", result)
            print("OCR识别文本列表:", texts)

            if not texts:
                print("⚠️ OCR 未识别到任何文本，重新尝试...")
                time.sleep(1)
                continue

            found_index = None
            found_text = None
            for i, text in enumerate(texts):
                if content in str(text):
                    found_index = i
                    found_text = str(text)
                    break

            if found_index is not None:
                box = boxes[found_index]
                # 估算关键词在整行中的位置
                text = found_text
                start_idx = text.index(content)
                end_idx = start_idx + len(content)
                total_len = len(text)
                # 计算相对位置
                rel_start = start_idx / total_len
                rel_end = end_idx / total_len
                # box: [左上, 右上, 右下, 左下]
                x1, y1 = box[0]
                x2, y2 = box[1]
                # 估算关键词中心的 x 坐标
                click_x = int(x1 + (x2 - x1) * (rel_start + rel_end) / 2) + offset[0]
                click_y = int((y1 + y2) / 2) + offset[1]

                print(f"找到 '{content}'，点击估算坐标: ({click_x}, {click_y})")
                pyautogui.click(click_x, click_y)
                return True

            time.sleep(1)

        except Exception as e:
            logging.exception(f"OCR定位出错: {e}")
            time.sleep(1)

    print(f"❌ 超时：未能在 {timeout} 秒内找到关键词 '{content}'")
    return False





if __name__ == '__main__':
    print(read_csv(Data.BRAND_DATA,1))
    # click_element_by_text("driver", offset=(10, 0), timeout=3)