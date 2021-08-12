class Progress(object):

    def __init__(self, result):
        """
        result:
            an AsyncResult or an object that mimics it to a degree
        """
        self.result = result

    def get_info(self):
        if self.result.state == 'FAILURE':
            meta = {'description': 'ETL job has failed. Please review all the ETL inputs to ensure they are correct.', 'responce': 'Load Failed'}
            return {'job_state': self.result.state, 'etl_info': meta}
        elif self.result.state == 'PENDING':
            meta = {"description": "ETL job is pending. Looking for open workers.", "responce": "None"}
            return {'job_state': self.result.state, 'etl_info': meta}
        else:
            return {'job_state': self.result.state, 'etl_info': self.result.info}
