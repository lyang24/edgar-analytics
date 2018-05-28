class Session(object):
    '''
    class to hold and retrive necessary session values
    '''
    def __init__(self, ip, first_session_time):
        self.ip = ip
        self.first_session_time = first_session_time
        self.last_session_time = first_session_time
        self.docs = 1

    def set_last_session_time(self, last_session_time):
        self.last_session_time = last_session_time

    def get_last_session_time(self):
        return self.last_session_time

    def get_ip(self):
        return self.ip

    def increment_doc(self):
        self.docs += 1

    def output_session(self):
        temp_list = [self.ip, self.first_session_time, self.last_session_time, self.docs]
        return temp_list