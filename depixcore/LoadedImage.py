#coding=utf-8
from PIL import Image

class LoadedImage():

	def __init__(self, path): # 构造函数

		self.path = path
		self.loadedImage = False
		self.imageData = False

		self.loadImageData()

	def getCopyOfLoadedPILImage(self):
		return self.loadedImage.copy() # 获取一份拷贝的像素阵列

	def loadImage(self):
		self.loadedImage = Image.open(self.path) # 从文件加载图像
		self.width = self.loadedImage.size[0] # 设置宽高
		self.height = self.loadedImage.size[1]

	def loadImageData(self):
		if self.loadedImage == False:
			self.loadImage()

		self.imageData = [[y for y in range(self.height)] for x in range(self.width)] # 载入图像原始数据

		rawData = self.loadedImage.getdata()
		rawDataCount = 0

		for y in range(self.height):
			for x in range(self.width):
				self.imageData[x][y] = rawData[rawDataCount][0:3]
				rawDataCount += 1
