from task import Task

class CompetitionTask(Task):
	"""
	High level competition level task, contains a list of tasks for each competition task.
	"""

	def _on_task_run(self):
		self.finish()