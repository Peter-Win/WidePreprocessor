import unittest
from Taxon import Taxon
from core.ErrorTaxon import ErrorTaxon

class TaskTest(Taxon):
	queue = []
	testSum = 0
	def _getQueue(self):
		return TaskTest.queue
	@staticmethod
	def clr():
		TaskTest.queue = []
		TaskTest.testSum = 0
class Always:
	def check(self):
		return True
	def exec(self):
		TaskTest.testSum += 1
class Never:
	def check(self):
		return False
	def exec(self):
		pass

class TestQueue(unittest.TestCase):
	def testAlways(self):
		TaskTest.clr()
		p1 = TaskTest()
		# Добавление задачи, которая выполняется сразу
		p1.addTask(Always())
		self.assertEqual(len(TaskTest.queue), 0)
		self.assertEqual(TaskTest.testSum, 1)

	def testNever(self):
		TaskTest.clr()
		p1 = TaskTest()
		p1.addTask(Never())
		self.assertEqual(len(TaskTest.queue), 1)
		# Проверка зацикливания
		with self.assertRaises(ErrorTaxon):
			p1.resolveQueue(TaskTest.queue)

	def testSecond(self):
		class Second(Always): # Задание срабатывает со второго раза
			def __init__(self):
				super().__init__()
				self.ready = False
			def check(self):
				return self.ready
		# Проверка срабатывания со второго раза
		TaskTest.clr()
		p1 = TaskTest()
		self.assertEqual(TaskTest.testSum, 0)
		task = Second()
		self.assertEqual(task.check(), False)
		p1.addTask(task)
		self.assertEqual(TaskTest.testSum, 0)
		self.assertEqual(len(TaskTest.queue), 1)
		task.ready = True
		self.assertEqual(task.check(), True)
		p1.resolveQueue(TaskTest.queue)
		self.assertEqual(TaskTest.testSum, 1)
		self.assertEqual(len(TaskTest.queue), 0)

	def testId(self):
		# Предотвращение повторного выполнения задачи с taskId
		TaskTest.clr()
		p1 = TaskTest()
		p1.addTask(Always())	# Срабатывает в любом случае
		self.assertEqual(TaskTest.testSum, 1)		
		p1.addTask(Always(), 'myId')	# Срабатывает, т.к. первый вызов
		self.assertEqual(TaskTest.testSum, 2)
		p1.addTask(Always(), 'myId')	# Не срабатывает, т.к. myId уже есть
		self.assertEqual(TaskTest.testSum, 2)
		p1.addTask(Always(), 'another')	# срабатывает, т.к. новый id
		self.assertEqual(TaskTest.testSum, 3)

	def testDepend(self):
		# Условное срабатывание
		class Depend:
			def __init__(self, next, ready):
				self.next = next
				self.ready = ready
			def check(self):
				return self.ready
			def exec(self):
				if (self.next):
					self.next.ready = True
		TaskTest.clr()
		p1 = TaskTest()
		task3 = Depend(None, False)
		task2 = Depend(task3, False)
		task1 = Depend(task2, True)
		p1.addTask(task3)	# Задание должно встать в очередь
		self.assertEqual(len(TaskTest.queue), 1)
		p1.addTask(task2)	# Задание должно встать в очередь
		self.assertEqual(len(TaskTest.queue), 2)
		self.assertFalse(task2.ready)
		p1.addTask(task1)	# Задание не должно встать в очередь, а при выполнении ставит task2.ready
		self.assertEqual(len(TaskTest.queue), 2)
		self.assertTrue(task2.ready)
		TaskTest.resolveQueue(TaskTest.queue)
		self.assertEqual(len(TaskTest.queue), 0)
		self.assertTrue(task3.ready)
