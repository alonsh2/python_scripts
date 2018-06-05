import sys
from pexpect import pxssh
import pickle
import getpass



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
        self.init_iptables_rules()
        self.init_packages()

    def get_hostname(self):
        return self.hostname
    def get_ip(self):
        return self.ip
    def init_packages(self):
        s = pxssh.pxssh()
        try:
            if not s.login(self.ip, self.login, self.password):
                print("SSH session failed on login.")
                print(str(s))
            else:
                s.sendline('rpm -qa')
                s.prompt(10)  # match the prompt
                #print(s.before)  # print everything before the prompt.
                self.packages = s.before.splitlines()
                s.logout()
                self.packages.pop(0)
        except pxssh.ExceptionPxssh as e:
            print("pxssh failed on login.")
            print(e)
        #for p in self.packages:
        #    print(p)
    def add_package(self, package):
        s = pxssh.pxssh()
        try:
            if not s.login(self.ip, self.login, self.password):
                print("SSH session failed on login.")
                print(str(s))
            else:
                s.sendline("yum install " + package + " -y")
                s.prompt()  # match the prompt
                s.logout()
        except pxssh.ExceptionPxssh as e:
            print("pxssh failed on login.")
            print(e)
        self.init_packages()
    def remove_package(self, package):
        s = pxssh.pxssh()
        try:
            if not s.login(self.ip, self.login, self.password):
                print("SSH session failed on login.")
                print(str(s))
            else:
                s.sendline("yum remove " + package + " -y")
                s.prompt()  # match the prompt
                s.logout()
        except pxssh.ExceptionPxssh as e:
            print("pxssh failed on login.")
            print(e)
        self.init_packages()
    def print_package(self):
        for p in self.packages:
            print(p)

    def init_iptables_rules(self):
        s = pxssh.pxssh()
        try:
            if not s.login(self.ip, self.login, self.password):
                print("SSH session failed on login.")
                print(str(s))
            else:
                s.sendline('iptables-save | egrep -e "-A OUTPUT |-A INPUT "')
                s.prompt(600)  # match the prompt
                # print(s.before)  # print everything before the prompt.
                self.iptables_rules = s.before.splitlines()
                s.logout()
        except pxssh.ExceptionPxssh as e:
            print("pxssh failed on login.")
            print(e)

    def print_iptables_rules(self):
        for p in self.iptables_rules:
            print(p)

    def add_iptables_rules(self, rule):
        s = pxssh.pxssh()
        try:
            if not s.login(self.ip, self.login, self.password):
                print("SSH session failed on login.")
                print(str(s))
            else:
                s.sendline("iptables -A "+ rule)
                s.prompt(600)  # match the prompt
                s.logout()
        except pxssh.ExceptionPxssh as e:
            print("pxssh failed on login.")
            print(e)
        self.init_iptables_rules()
    def remove_iptables_rules(self, rule):
        s = pxssh.pxssh()
        try:
            if not s.login(self.ip, self.login, self.password):
                print("SSH session failed on login.")
                print(str(s))
            else:
                s.sendline("iptables -D "+ rule)
                s.prompt(600)  # match the prompt
                s.logout()
        except pxssh.ExceptionPxssh as e:
            print("pxssh failed on login.")
            print(e)
        self.init_iptables_rules()

    def present_yourself(self):
        print ("My name is " + self.hostname + ".")
        print("My ip is " + self.ip + ".")
        print("My iptables rules configuration for INPUT and OUTPUT chains only:")
        self.print_iptables_rules()
        print("The following packages are installed within me:")
        #self.print_package()

class MyDataCenter:
    MyServers = []
    def __init__(self, MyServers):
        self.MyServers = MyServers
        pass
    def generate_report(self):
        for p in self.MyServers:
            p.present_yourself()
            print('-' * 100)
    def add_server(self):
        ip = input('Enter your ip:\n')
        hostname = input('Enter your hostname:\n')
        login = input('Enter your login:\n')
        password = getpass.getpass('password:\n')
        group = input('Enter your group:\n')
        NewServer = MyServer(ip, hostname,login,password,group)
        #NewServer.present_yourself()
        self.MyServers = self.MyServers + [NewServer]
        #self.MyServers[0].present_yourself()
    def remove_server(self):
        hostnameorip = input("Please, enter the hostname or ip to remove:\n")
        j = 0
        for p in self.MyServers:
            if (p.hostname == hostnameorip) or (p.ip == hostnameorip):
                self.MyServers.pop(j)
                break
            j = j + 1
#packages
    def add_package_hostnameip(self, hostnameorip, package):
        for p in self.MyServers:
            if (p.hostname == hostnameorip) or (p.ip == hostnameorip):
                p.add_package(package)
    def remove_package_hostnameip(self, hostnameorip, package):
        for p in self.MyServers:
            if (p.hostname == hostnameorip) or (p.ip == hostnameorip):
                p.remove_package(package)
    def add_package_by_group(self, group, package):
        for p in self.MyServers:
            if (p.group == group ):
                p.add_package(package)
    def remove_package_by_group(self, group, package):
        for p in self.MyServers:
            if (p.group == group):
                p.remove_package(package)
#iptables rules

    def add_iptables_rules_hostnameip(self, hostnameorip, rule):
        for p in self.MyServers:
            if (p.hostname == hostnameorip) or (p.ip == hostnameorip):
                p.add_iptables_rules(rule)
    def remove_iptables_rules_hostnameip(self, hostnameorip, rule):
        for p in self.MyServers:
            if (p.hostname == hostnameorip) or (p.ip == hostnameorip):
                p.remove_iptables_rules(rule)
    def add_iptables_rules_by_group(self, group, rule):
        for p in self.MyServers:
            if (p.group == group ):
                p.add_iptables_rules(rule)
    def remove_iptables_rules_by_group(self, group, rule):
        for p in self.MyServers:
            if (p.group == group):
                p.remove_iptables_rules(rule)
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

x = MyServer("52.15.149.88","ec2-52-15-149-88.us-east-2.compute.amazonaws.com", 'root', '***SECRET***')
x2 = MyServer("18.221.161.250","ec2-18-221-161-250.us-east-2.compute.amazonaws.com", 'root', '***SECRET***')

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


with open('MyServers.pkl', 'rb') as SavedServers:
    MyServers2= pickle.load(SavedServers)

m  = MyDataCenter(MyServers)
#m.add_server()
#m.remove_package_by_group("default", "screen")
m.remove_iptables_rules_by_group("default","INPUT -i eth0 -p tcp --dport 441 -j DROP")
m.remove_iptables_rules_by_group("default","INPUT -i eth0 -p tcp --dport 441 -j DROP")
m.remove_iptables_rules_hostnameip("52.15.149.88","INPUT -i eth0 -p tcp --dport 441 -j DROP")
m.generate_report()
m.add_iptables_rules_hostnameip("52.15.149.88","INPUT -i eth0 -p tcp --dport 441 -j DROP")
#m.add_package_hostnameip("52.15.149.88","screen")
#m.remove_package_hostnameip("52.15.149.88","screen")
#m.add_package_by_group("default", "screen")
#m.remove_server()
m.generate_report()

m.add_iptables_rules_by_group("default","INPUT -i eth0 -p tcp --dport 441 -j DROP")

m.generate_report()
