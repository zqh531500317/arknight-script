from module.base.decorator import singleton


@singleton
class State:
    is_config_edit = False
    lizhi = {"time": "0", "lizhi": "0", "maxlizhi": "0"}
    is_fight = "stop"  # stop or running or task(标记不能同时运行的任务)
    running_task_num = 0
    debug_run = False
    running_task_name = ""
    running_job_num = 0
    running_job = {"id": "", "name": ""}
    # 队列 [job]
    blocking_jobs = []
    retry_time = 0

    @classmethod
    def if_continue(cls, max_retry_time=3):
        if cls.retry_time < max_retry_time:
            cls.retry_time += 1
            return True
        else:
            cls.retry_time = 0
            return False

    @classmethod
    def job_start(cls, job):
        if cls.running_job_num == 0:
            cls.running_job['id'] = job.id
            cls.running_job['name'] = job.name
            cls.running_job_num += 1
        else:
            cls.blocking_jobs.append(job)

    @classmethod
    def job_finish(cls):
        if len(cls.blocking_jobs) != 0:
            job = cls.blocking_jobs.pop(0)
            cls.running_job['id'] = job.id
            cls.running_job['name'] = job.name
        else:
            cls.running_job_num -= 1
            cls.running_job['id'] = ""
            cls.running_job['name'] = ""
