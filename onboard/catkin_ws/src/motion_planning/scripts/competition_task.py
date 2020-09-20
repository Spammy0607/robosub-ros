from combination_tasks import ListTask
from move_tasks import MoveToPoseGlobalTask
<<<<<<< HEAD
from task import Task
from prequal_tasks import PreQualGlobalTask

=======
from move_tasks import MoveToPoseLocalTask
from move_tasks import HoldPositionTask
from log_task import LogTask
from prequal_tasks import PreQualGlobalTask, PreQualLocalTask
>>>>>>> 63a38d726a101fd30c47c60da0fbcf1ba1fdf04f

class CompetitionTask(Task):
    """
    High level competition level task, contains a list of tasks for each competition task.
    """

    def __init__(self, *args, **kwargs):
        super(CompetitionTask, self).__init__(*args, **kwargs)

        self.list_task = ListTask([MoveToPoseGlobalTask(-7, 0, 0, 0, 0, 0)])
        # self.list_task = ListTask([MoveToPoseLocalTask(2, 0, 0, 0, 0, 0)])
        # self.list_task = ListTask([HoldPositionTask()])
        # self.list_task = ListTask([LogTask("FATAL", "This is falal")])
        # self.list_task = ListTask([SimulTask([LogTask("WARN", "Warning"), MoveToPoseGlobalTask(30,0,0,0,0,0)])])
        # self.prequal_task = PreQualGlobalTask()

    def _on_task_run(self):
        self.list_task.run()

        if self.list_task.finished:
            self.finish()