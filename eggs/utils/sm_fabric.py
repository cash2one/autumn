from fabric.api import env, hosts, get, cd

# env.passwords = {'root@192.168.250.207': 'chinascope!@#$'}

env.hosts = ['192.168.250.207']
env.user = 'root'
env.password = "chinascope!@#$"


def my_get():
    get('/home/xutaoding/npl_news/push.py', '/home/xutaoding/')


def test_get():
    keys = env.keys()
    print keys
    print 'passwords' in keys
    print 'hosts' in keys


if __name__ == '__main__':
    test_get()
