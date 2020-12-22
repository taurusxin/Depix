#coding=utf-8
from depixcore.LoadedImage import *
from depixcore.Rectangle import *
from depixcore.functions import *

import argparse
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')


usage = '''
	马赛克化的字符图片必须被切割出来，保留的部分只能是每一个马赛克像素
	[搜索图像]必须是[德布勒恩]字符序列的截图
	[搜索图像]中，编辑器和字体及文字大小与被像素化的原始截图相同
'''

parser = argparse.ArgumentParser(description = usage)
parser.add_argument('-p', '--pixelimage', help = '马赛克图片的路径', required=True)
parser.add_argument('-s', '--searchimage', help = '搜索图像的路径', required=True)
parser.add_argument('-o', '--outputimage', help = '结果输出路径', nargs='?', default='output.png')
args = parser.parse_args()

pixelatedImagePath = args.pixelimage
searchImagePath = args.searchimage


logging.info("加载马赛克图片： %s" % pixelatedImagePath)
pixelatedImage = LoadedImage(pixelatedImagePath)
unpixelatedOutputImage = pixelatedImage.getCopyOfLoadedPILImage()

logging.info("加载搜索图片： %s" % searchImagePath)
searchImage = LoadedImage(searchImagePath)

logging.info("正在马赛克图片中寻找色彩矩阵...")
# fill coordinates here if not cut out
pixelatedRectange = Rectangle((0, 0), (pixelatedImage.width - 1, pixelatedImage.height - 1)) # 初始化图像矩阵

pixelatedSubRectanges = findSameColorSubRectangles(pixelatedImage, pixelatedRectange)
logging.info("找到了 %s 相同的色彩区块" % len(pixelatedSubRectanges))

pixelatedSubRectanges = removeMootColorRectangles(pixelatedSubRectanges)
logging.info("在进行了无效区块过滤之后，还剩 %s 个矩阵" % len(pixelatedSubRectanges))

rectangeSizeOccurences = findRectangleSizeOccurences(pixelatedSubRectanges)
logging.info("找到了 %s 不同的矩阵大小" % len(rectangeSizeOccurences))

logging.info("在搜索图像中寻找匹配...")
rectangleMatches = findRectangleMatches(rectangeSizeOccurences, pixelatedSubRectanges, searchImage)

logging.info("移除没有匹配到的区块")
pixelatedSubRectanges = dropEmptyRectangleMatches(rectangleMatches, pixelatedSubRectanges)

logging.info("分离单个及多个区块")
singleResults, pixelatedSubRectanges = splitSingleMatchAndMultipleMatches(pixelatedSubRectanges, rectangleMatches)

logging.info("[%s 直接匹配 | %s 多次匹配]" % (len(singleResults), len(pixelatedSubRectanges)))

logging.info("在单次匹配正方形上尝试几何匹配")
singleResults, pixelatedSubRectanges = findGeometricMatchesForSingleResults(singleResults, pixelatedSubRectanges, rectangleMatches)

logging.info("[%s 直接匹配 | %s 多次匹配]" % (len(singleResults), len(pixelatedSubRectanges)))

logging.info("尝试另一种几何匹配")
singleResults, pixelatedSubRectanges = findGeometricMatchesForSingleResults(singleResults, pixelatedSubRectanges, rectangleMatches)

logging.info("[%s 直接匹配 | %s 多次匹配]" % (len(singleResults), len(pixelatedSubRectanges)))

logging.info("写入单次匹配结果到输出文件中")
writeFirstMatchToImage(singleResults, rectangleMatches, searchImage, unpixelatedOutputImage)

logging.info("写入多次匹配的平均结果到文件中")
writeAverageMatchToImage(pixelatedSubRectanges, rectangleMatches, searchImage, unpixelatedOutputImage)

logging.info("结果正在保存到: %s" % args.outputimage)
unpixelatedOutputImage.save(args.outputimage)