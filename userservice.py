from xml.dom import minidom
import time
import sha

from connection import Connection
from xmlhelper import dict_to_xml
from response import *

class UserService(object):

    SERVICE_PATH = '/userService'
    
    def __init__(self, connection):
        self.connection = connection

    def login_and_get_status(self):
        namespaces = {'ns2':'urn:com:airbiquity:smartphone.userservices:v1'}
        d = {'SmartphoneLoginInfo':
                 { 'UserLoginInfo':
                       { 'userId': self.connection.username,
                         'userPassword': self.connection.password },
                   'DeviceToken': 'DUMMY%f' % time.time(),
                   'UUID': sha.sha("carwings_api:%s" % self.connection.username).hexdigest(),
                   'Locale': 'US',
                   'AppVersion': '1.40',
                   'SmartphoneType': 'IPHONE'},
             'SmartphoneOperationType': 'SmartphoneLatestBatteryStatusRequest'}

        xml = dict_to_xml(d, 
                          'ns2:SmartphoneLoginWithAdditionalOperationRequest', 
                          namespaces)

        result = self.connection.post_xml(self.SERVICE_PATH, xml)
        return LoginStatus(result)

if __name__ == "__main__":
    c = Connection('YOUR_USERNAME', 'YOUR_PASSWORD')
    u = UserService(c)
    d = u.login_and_get_status()
    import yaml
    print yaml.dump(d)
    
        