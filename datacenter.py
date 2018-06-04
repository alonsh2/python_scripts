import sys
from pexpect import pxssh
import pickle

print (sys.version)
class MyServer:
    hostname = ''
    ip = ''
    packages = []
    iptables_rules = []
    password = ''
    login = ''

    def __init__(self, ip, hostname, login, password, group = 'default'):
        self.ip  = ip
        self.hostname = hostname
        self.login = login
        self.password = password
        self.group = group
        self.init_packages()
        self.init_iptables_rules()

    def get_hostname(self):
        return self.hostname
    def get_ip(self):
        return self.ip
    def init_packages(self):
        s = pxssh.pxssh()
        if not s.login(self.ip, self.login, self.password):
            print("SSH session failed on login.")
            print(str(s))
        else:
            s.sendline('rpm -qa')
            s.prompt(600)  # match the prompt
            #print(s.before)  # print everything before the prompt.
            self.packages = s.before.splitlines()
            s.logout()
        #print (self.packages)
        #print (len(self.packages))
            self.packages.pop(0)
        #for p in self.packages:
        #    print(p)
    def add_package(self, package):
        s = pxssh.pxssh()
        if not s.login(self.ip, self.login, self.password):
            print("SSH session failed on login.")
            print(str(s))
        else:
            s.sendline("yum install " + package + " -y")
            s.prompt(600)  # match the prompt
            s.logout()
    def remove_package(self, package):
        s = pxssh.pxssh()
        if not s.login(self.ip, self.login, self.password):
            print("SSH session failed on login.")
            print(str(s))
        else:
            s.sendline("yum remove " + package + "-y")
            s.prompt(600)  # match the prompt
            s.logout()

    def print_package(self):
        for p in self.packages:
            print(p)

    def init_iptables_rules(self):
        s = pxssh.pxssh()
        if not s.login(self.ip, self.login, self.password):
            print("SSH session failed on login.")
            print(str(s))
        else:
            s.sendline('iptables-save | egrep -e "-A OUTPUT |-A INPUT "')
            s.prompt(600)  # match the prompt
            # print(s.before)  # print everything before the prompt.
            self.iptables_rules = s.before.splitlines()
            s.logout()
            #print (self.iptables_rules)
            #print (len(self.iptables_rules))
            #for p in self.iptables_rules:
            #    print(p)

    def print_iptables_rules(self):
        for p in self.iptables_rules:
            print(p)

    def add_iptables_rules(self, rule):
        s = pxssh.pxssh()
        if not s.login(self.ip, self.login, self.password):
            print("SSH session failed on login.")
            print(str(s))
        else:
            s.sendline("iptables -A "+ rule)
            s.prompt(600)  # match the prompt
            s.logout()
    def remove_iptables_rules(self, rule):
        s = pxssh.pxssh()
        if not s.login(self.ip, self.login, self.password):
            print("SSH session failed on login.")
            print(str(s))
        else:
            s.sendline("iptables -D "+ rule)
            s.prompt(600)  # match the prompt
            s.logout()
    def present_yourself(self):
        print ("My name is " + self.hostname + ".")
        print("My ip is " + self.ip + ".")
        print("My iptables rules configuration for INPUT and OUTPUT chains only:")
        self.print_iptables_rules()
        print("The following packages are installed within me:")
        self.print_package()

class MyDataCenter:
    MyServers = []
    def __init__(self, MyServers):
        self.MyServers = MyServers

    def add_server(self):


class MyIpTableRule:
    ip = ''
    port = 0
    IsInput = False
    def __init__(self, ip, port, IsInput):
        self.ip  = ip
        self.port = port
        self.IsInput = IsInput


class MyPackage:
    name = 'tmux'
    arch = 'x86_64'
    version = '1.8'
    release = '4.el7'

# Serializng objects
def save_object(obj, filename):
    with open(filename, 'wb') as output:  # Overwrites any existing file.
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)

x = MyServer("52.15.149.88","ec2-52-15-149-88.us-east-2.compute.amazonaws.com", 'root', '****SECRET*****')
x2 = MyServer("18.221.161.250","ec2-18-221-161-250.us-east-2.compute.amazonaws.com", 'root', '****SECRET***')
'''
print (x.get_hostname())
print (x2.get_hostname())
x.init_packages()
x.add_package ("tmux")
x.print_package()
x.remove_package("tmux")
x.init_iptables_rules()
x.print_iptables_rules()
x.add_iptables_rules("INPUT -i eth0 -p tcp --dport 441 -j DROP")
x.init_iptables_rules()
x.print_iptables_rules()
x.add_iptables_rules("INPUT -i eth0 -s '10.0.0.0' -j DROP")
x.init_iptables_rules()
x.print_iptables_rules()
x.remove_iptables_rules("INPUT -i eth0 -p tcp --dport 441 -j DROP")
x.init_iptables_rules()
x.print_iptables_rules()
x.remove_iptables_rules("INPUT -i eth0 -s '10.0.0.0' -j DROP")
x.init_iptables_rules()
x.print_iptables_rules()
'''

MyServers = [x, x2]
save_object(MyServers, 'MyServers.pkl')


with open('MyServers.pkl', 'rb') as input:
    MyServers2= pickle.load(input)

print(MyServers2[0].get_ip())

#MyServers2[0].present_yourself()
print(MyServers2[0].group)

m  = MyDataCenter(MyServers2)
'''
s = pxssh.pxssh()
if not s.login(MyServers2[0].get_ip(), 'root', '***SECRET*****'):
    print ("SSH session failed on login.")
    print (str(s))
else:
    print ("SSH session login successful")
    s.sendline('uptime')
    s.prompt()  # match the prompt
    print (s.before) # print everything before the prompt.
    s.sendline('yum info tmux')
    s.prompt()  # match the prompt
    print (s.before) # print everything before the prompt.
    s.sendline('rpm -qa')
    s.prompt()  # match the prompt
    print (s.before) # print everything before the prompt.
    s.logout()

'''
