#!/usr/bin/env python
__author__ = 'Chocolee'

import jenkins, time


class PythonJenkins(object):
    def __init__(self):
        self.username = 'admin'
        self.api_token = '117d9fd2686d588af05ba7a88c8891e7e0'
        self.url = 'http://192.168.31.100:8080/jenkins'
        self.server = self.connect()
        self.server.get_whoami()

    def connect(self):
        # init connect
        server = jenkins.Jenkins(url=self.url, username=self.username, password=self.api_token)
        return server

    def get_version(self):
        # get jenkins version
        version = self.server.get_version()
        print(version)

    def disable_job(self, job_name):
        # disable job
        self.server.disable_job(job_name)

    def enable_job(self, job_name):
        # enable job
        self.server.enable_job(job_name)

    def get_build_job_id(self, job_name):
        # build job
        ret = self.server.build_job(job_name)
        return ret

    def get_build_job_status(self, job_name, num):
        job_status = self.server.get_build_info(job_name, num)['result']
        print(job_status)


if __name__ == "__main__":

    PythonJenkins = PythonJenkins()
    # PythonJenkins.enable_job('test-jar')
    # PythonJenkins.get_version()
    # num = PythonJenkins.get_build_job_id('test-jar')
    # time.sleep(20)
    PythonJenkins.get_build_job_status('test-jar', 8)
