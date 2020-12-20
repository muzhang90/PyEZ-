from jnpr.junos import Device
from jnpr.junos.utils.start_shell import StartShell
from lxml import etree
from pprint import pprint
from jnpr.junos.factory import loadyaml
from jnpr.junos.op.fpc import FpcInfoTable

import warnings
warnings.filterwarnings('ignore',category=RuntimeWarning)



def get_fpc_cli(dev):
    fpcs=dev.cli('show chassis fpc',warning=False)
    print(fpcs)
    fpc_list=fpcs.strip().split('\n')
    #print(*[fpc for fpc in fpc_list],sep='\n')



def get_fpc_shell(dev):
    ss=StartShell(dev)
    ss.open()
    fpcs=ss.run('cli -c "show chassis fpc"')
    print(fpcs)
    for fpc in fpcs[1].strip().split('\n')[1:]:
        print(fpc)
    ss.close()

def get_fpc_xpath(dev):
    fpcs_xpath=dev.rpc.get_fpc_information()
    pprint(etree.dump(fpcs_xpath))
    fpcs=fpcs_xpath.iter()
    for fpc in fpcs:
        if fpc.tag=='fpc':
            print(fpc.findtext('slot'), fpc.findtext('state'),fpc.findtext('temperature'),fpc.findtext('cpu-total'))


def get_fpc_json(dev):
    fpcs_json=dev.rpc.get_fpc_information({'format':'json'})
    pprint(fpcs_json)
    for fpc in fpcs_json['fpc-information'][0]['fpc']:
        print(fpc)

def get_fpc_yml(dev):
    user_defs=loadyaml('UserFPCTable.yml')
    globals().update(user_defs)

    user_table=UserFPCTable(dev)
    user_table.get()
    pprint(user_table.items())

def get_fpc_table(dev):
    fpc_table=FpcInfoTable(dev)
    fpc_table.get()
    pprint(fpc_table.items())


def use_textfsm(dev):
    pass

if __name__ == '__main__':

    with Device(host='10.85.160.211',user='labroot',password='lab123') as dev:
        '''
        '{:^10}'.format('test')
        '''
        '''
        print('{:*^50}'.format(' Get fpc info -- cli '))
        
        '''
        get_fpc_cli(dev)
        #print('{:*^50}'.format(' Get fpc info -- shell '))
        #get_fpc_shell(dev)

        #print('{:*^50}'.format(' Get fpc info -- xpath '))
        get_fpc_xpath(dev)

        #print('{:*^50}'.format(' Get fpc info -- json '))
        #get_fpc_json(dev)
        #print('{:*^50}'.format(' Get fpc info -- yml '))
        get_fpc_yml(dev)
        print('{:*^50}'.format(' Get fpc info -- table '))
        #get_fpc_table(dev)
