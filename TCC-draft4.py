#Improvements to be done:
#   In line  print which resources are missing
import random

class cpu:
    def __init__(self, clock, n_cores):
        self.n_cores = n_cores
        self.core = clock
        self.threads = 2
 
class interface:
    def __init__(self, mac_addr, net_addr, net_mask, ip_addr, ip_mask):
        self.mac_addr = mac_addr
        self.net_addr = net_addr
        self.net_mask = net_mask
        self.ip_addr = ip_addr
        self.ip_mask = ip_mask
 
class blade:
    def __init__(self, n_cpu, ram, n_ssd, n_interfaces, hostname):
        self.hostname = hostname
        self.n_cpu = n_cpu
        self.n_interfaces = n_interfaces
        self.ram = ram
        self.n_ssd = n_ssd
        self.cpus = []
        self.ssds = []
        self.interfaces = []
        self.active_vms = []
        self.resource = {'ram': 0, 'cpu': 0, 'ssd': 0}
        self.available_resources()
 
    def cpu_setup(self, clock, cores):
        if len(self.cpus) < self.n_cpu:
            self.cpus.append(cpu(clock, cores))
            self.available_resources()
        else:
            print("You cannot add more CPUs")
 
    def ssd_setup(self, capacity):
        if len(self.ssds) < self.n_ssd:
            self.ssds.append(capacity)
        else:
            print("You cannot add more SSDs")
 
    def interface_setup(self, mac_addr, net_addr, net_mask, ip_addr, ip_mask):
        if len(self.interfaces) < self.n_interfaces:
            self.interfaces.append(interface(mac_addr, net_addr, net_mask, ip_addr, ip_mask))
        else:
            print("You cannot add more interfaces")
 
    def lst_blade(self):
        print("\nHostname: "+self.hostname+"\n-----------------------------------\n")
        print("Memory RAM\t"+str(self.ram))
        print("CPU\tNumber of Cores\t\tClock")
        i=1
        for element in self.cpus:
            print("CPU#"+str(i)+"\t"+str(element.n_cores)+"\t\t\t"+str(element.core))
            i=i+1
        print("SSD\tCapacity")
        i=1
        for element in self.ssds:
            print("SSD#"+str(i)+"\t"+str(element))
            i=i+1
        print("Interface\tMAC Address\t\t\tNetwork Address\t\tMask                   IP Address       Mask")
        i=1
        for element in self.interfaces:
            print("Interface#"+str(i)+"\t"+str(element.mac_addr)+"\t\t\t"+str(element.net_addr)+"\t\t"+str(element.net_mask)+"          "+str(element.ip_addr)+"         "+str(element.ip_mask))
            i=i+1
    def available_resources(self):
        sum_cpu = 0
        sum_ssd = 0
        for cpu in self.cpus:
            sum_cpu = sum_cpu + cpu.n_cores
        for ssd in self.ssds:
            sum_ssd = sum_ssd + ssd
        self.resource['ram'] = self.ram
        self.resource['cpu'] = sum_cpu
        self.resource['ssd'] = sum_ssd
    def resources_clock(self):
        sum_cpu = 0
        sum_ssd = 0
        for cpu in self.cpus:
            sum_cpu = sum_cpu + cpu.n_cores
        for ssd in self.ssds:
            sum_ssd = sum_ssd + ssd
        return [self.ram, sum_cpu, sum_ssd]
 
class hypervisor:
    def __init__(self):
        self.vms = {}
        self.datacenter = {}
        self.best_resource = {'ram': 0, 'cpu': 0, 'ssd': 0}
    def add_datacenter(self, name):
        self.datacenter[name] = {}
        self.vms[name] = {}
    def add_server(self, datacenter, host):
        if self.datacenter.get(datacenter) == None:
            print("Insert an existent datacenter name!")
        else:
            self.datacenter[datacenter][host.hostname] = host
            self.vms[datacenter][host.hostname] = {}
            new_vm_resources = host.resource
            if new_vm_resources['ram'] > self.best_resource['ram']:
                self.best_resource['ram'] = new_vm_resources['ram']
            if new_vm_resources['cpu'] > self.best_resource['cpu']:
                self.best_resource['cpu'] = new_vm_resources['cpu']
            if new_vm_resources['ssd'] > self.best_resource['ssd']:
                self.best_resource['ssd'] = new_vm_resources['ssd']
    def list_datacenter(self):
        for key, value in self.datacenter.items():
            print("Datacenter: ", key,"\n##########################")
            for k, host in value.items():
                print(host.lst_blade())

    def check_host(self, hostname, datacenter):
        if datacenter in self.datacenter:
            if hostname in self.datacenter[datacenter]:
                return 1
        return 0
    def check_vm(self, guestname, hostname, datacenter):
        if datacenter in self.vms:
            if hostname in self.vms[datacenter]:
                if guestname in self.vms[datacenter][hostname]:
                    return 1
        return 0
            
    def list_vms(self, datacenter, hostname):

        if self.datacenter.get(datacenter) == None:
            print("Insert an existent datacenter name!")
            return 0
        else:
            if self.check_host(hostname, datacenter) == 0:
                print("Insert an existent hostname!")
                return 0
        print("Datacenter: "+datacenter+" Host: "+hostname+"\n")
        for vm in self.vms[datacenter][hostname]:
            self.vms[datacenter][hostname][vm].lst_vm()

    def add_vm(self, n_cpu, core, clock, ram, storage, n_interfaces, guestname, hostname, datacenter):
        if self.datacenter.get(datacenter) == None:
            print("Insert an existent datacenter name!")
            return 0
        else:
            if not self.check_host(hostname, datacenter):
                print("Insert an existent hostname!")
                return 0
        vmm = self.datacenter[datacenter][hostname]
        if n_cpu > vmm.n_cpu:
            print("Guest cannot have more CPUs than host")
            exit(1)
        if ram > vmm.ram:
            print("Guest cannot have more RAM than host")
            exit(1)
        for i in range(0,n_cpu):
            if core > vmm.cpus[i].n_cores:
                print("Number of cores of virtual processor cannot be bigger than the number of cores from host's processor")
                exit(1)
        for i in range(0,n_cpu):
            if clock > vmm.cpus[i].core:
                print("Clock of virtual processor cannot be bigger than clock of host's processor")
                exit(1)
        new_vm = vm(n_cpu, ram, 1, 1, guestname, hostname, datacenter)
        for i in range(0, n_cpu):
            new_vm.cpu_setup(clock, core)
        new_vm.ssd_setup(storage)
        self.vms[datacenter][hostname][guestname] = new_vm
        #new_vm_resources = new_vm.resources_clock()
        #if new_vm_resources[0] > self.best_resource['ram']:
        #    self.best_resource['ram'] = new_vm_resources[0]
        #if new_vm_resources[1] > self.best_resource['cpu']:
        #    self.best_resource['cpu'] = new_vm_resources[1]
        #if new_vm_resources[2] > self.best_resource['ssd']:
        #    self.best_resource['ssd'] = new_vm_resources[2]

    def best_VM(self, weight_cpu, weight_ram, weight_ssd):
        vmnames = []
        vmweights = []
        for key, value in self.vms.items():
            print(key)
            for key2, value2 in value.items():
                print(key2)
                for key3, value3 in value2.items():
                    temp = value3.resources_clock()
                    vmweights.append((temp[0]/self.best_resource['ram'])*weight_ram+(temp[1]/self.best_resource['cpu'])*weight_cpu+(temp[2]/self.best_resource['ssd'])*weight_ssd)
                    #vmweights.append((temp[0])*weight_ram+(temp[1])*weight_cpu+(temp[2])*weight_ssd)
                    vmnames.append([key3,key2,key])
        min_value = max(vmweights)
        vm_min = vmweights.index(min_value)
        print(vmweights)
        return vmnames[vm_min]
    def best_blade(self, weight_cpu, weight_ram, weight_ssd):
        vmnames = []
        vmweights = []
        for key, value in self.datacenter.items():
            for key2, value2 in value.items():
                #print("->",key2,value2.resource)
                temp = value2.resource
                vmweights.append((temp['ram']/self.best_resource['ram'])*weight_ram+(temp['ssd']/self.best_resource['cpu'])*weight_cpu)
                #vmweights.append((temp[0])*weight_ram+(temp[1])*weight_cpu+(temp[2])*weight_ssd)
                vmnames.append([key2,key])
        min_value = max(vmweights)
        vm_min = vmweights.index(min_value)
        return vmnames[vm_min]

    def powerOnVM(self, guestname, hostname, datacenter):
        if not self.check_host(hostname, datacenter):
            print("Enter with a valid datacenter or hostname!")
            return 0
        #self.vms[datacenter][hostname][guestname].state = 1
        resources = self.vms[datacenter][hostname][guestname].resources().copy()
        if self.datacenter[datacenter][hostname].resource['ram'] - resources[0] >= 0 and self.datacenter[datacenter][hostname].resource['cpu'] - resources[1] >= 0:
            self.vms[datacenter][hostname][guestname].state = 1
            self.datacenter[datacenter][hostname].resource['ram'] = self.datacenter[datacenter][hostname].resource['ram'] - resources[0]
            self.datacenter[datacenter][hostname].resource['cpu'] = self.datacenter[datacenter][hostname].resource['cpu'] - resources[1]
            self.datacenter[datacenter][hostname].active_vms.append([guestname, hostname, datacenter])
        else:
            print("You don't have enough available resources")
            #print which resources are missing

    def powerOffVM(self, guestname, hostname, datacenter):
        if not self.check_host(hostname, datacenter):
            print("Enter with a valid datacenter or hostname!")
            return 0
        self.vms[datacenter][hostname][guestname].state = 0
        resources = self.vms[datacenter][hostname][guestname].resources().copy()
        self.datacenter[datacenter][hostname].resource['ram'] = self.datacenter[datacenter][hostname].resource['ram'] + resources[0]
        self.datacenter[datacenter][hostname].resource['cpu'] = self.datacenter[datacenter][hostname].resource['cpu'] + resources[1]
    def rr_affinity_list(self, type, affinity):
        list = []
        for key, value in self.datacenter.items():
            for k, host in value.items():
                affinity_var = 0
                for s in host.active_vms:
                    if self.vms[s[2]][s[1]][s[0]].type == type:
                        affinity_var = affinity_var+1
                if affinity_var < affinity:
                    list.append([k, key])
        return list
    
    def affinity_check(self, type, affinity, dc, host):
        affinity_var = 0
        for s in self.datacenter[dc][host].active_vms:
            if self.vms[s[2]][s[1]][s[0]].type == type:
                affinity_var = affinity_var+1
        if affinity_var < affinity:
            return 1
        return 0
    
    def check_blade_resources(self, vcpus, ram, ssd, host, dc):
        resource_vector = self.datacenter[dc][host].resource
        if(ram > resource_vector['ram']):
            #print("Insufficient free RAM")
            return 0
        if(vcpus > resource_vector['cpu']):
            #print("Insufficient vCPUs available")
            return 0
        #print("The blade has available resources")
        return 1
    
class vm:
    def __init__(self, n_cpu, ram, n_ssd, n_interfaces, guestname, hostname, datacenter):
        self.datacenter = datacenter
        self.hostname = hostname
        self.guestname = guestname
        self.n_cpu = n_cpu
        self.n_interfaces = n_interfaces
        self.ram = ram
        self.n_ssd = n_ssd
        self.cpus = []
        self.ssds = []
        self.interfaces = []
        self.state = 0
        self.type = ""
 
    def cpu_setup(self, clock, cores):
        if len(self.cpus) < self.n_cpu:
            self.cpus.append(cpu(clock, cores))
        else:
            print("You cannot add more CPUs")
 
    def ssd_setup(self, capacity):
        if len(self.ssds) < self.n_ssd:
            self.ssds.append(capacity)
        else:
            print("You cannot add more SSDs")
 
    def interface_setup(self, mac_addr, net_addr, net_mask, ip_addr, ip_mask):
        if len(self.interfaces) < self.n_interfaces:
            self.interfaces.append(interface(mac_addr, net_addr, net_mask, ip_addr, ip_mask))
        else:
            print("You cannot add more interfaces")
 
    def lst_vm(self):
        print("Hostname: "+self.hostname)
        print("Guestname: "+self.guestname)
        print("State: "+str(self.state))
        print("Memory RAM\t"+str(self.ram))
        print("CPU\tNumber of Cores\t\tClock")
        i=1
        for element in self.cpus:
            print("CPU#"+str(i)+"\t"+str(element.n_cores)+"\t\t\t"+str(element.core))
            i=i+1
        print("SSD\tCapacity")
        i=1
        for element in self.ssds:
            print("SSD#"+str(i)+"\t"+str(element))
            i=i+1
        print("Interface\tMAC Address\t\t\tNetwork Address\t\tMask                   IP Address       Mask")
        i=1
        for element in self.interfaces:
            print("Interface#"+str(i)+"\t"+str(element.mac_addr)+"\t\t\t"+str(element.net_addr)+"\t\t"+str(element.net_mask)+"          "+str(element.ip_addr)+"         "+str(element.ip_mask))
            i=i+1
    def resources(self):
        sum_cpu = 0
        for cpu in self.cpus:
            sum_cpu = sum_cpu + cpu.n_cores
        return [self.ram, sum_cpu]
    def resources_clock(self):
        sum_cpu = 0
        sum_ssd = 0
        for cpu in self.cpus:
            sum_cpu = sum_cpu + cpu.n_cores
        for ssd in self.ssds:
            sum_ssd = sum_ssd + ssd
        return [self.ram, sum_cpu, sum_ssd]

class module:
    def __init__(self, id, type, guestname, hostname, datacenter):
        self.id = id
        self.type = type
        self.guestname = guestname
        self.hostname = hostname
        self.datacenter = datacenter


class vnf:
    def __init__(self, name, hypervisor):
        self.name = name
        self.modules = {}
        self.hypervisor = hypervisor
        self.vcpus = 0
        self.ram = 0
        self.ssd = 0
        self.wvcpus = 0
        self.wrap = 0
        self.wssd = 0
        self.anti_affinity = 0
        self.scale_factor = 0
        self.anti_affinity_list = []
    def add_module(self, id, type):
        if(len(self.anti_affinity_list)==0):
            print("foi")
            self.anti_affinity_list = self.hypervisor.rr_affinity_list(self.name,self.anti_affinity)
        flag_affinity = 1
        while(flag_affinity):
            if(self.anti_affinity_list):
                host = self.anti_affinity_list[0]
                self.anti_affinity_list.pop(0)
                if(self.hypervisor.check_blade_resources(self.vcpus, self.ram, self.ssd, host[0], host[1]) and self.hypervisor.affinity_check(type, self.anti_affinity, host[1], host[0])):
                    self.modules[type+str(id)] = module(id, type, type+str(id), host[0], host[1])
                    clock = self.hypervisor.datacenter[host[1]][host[0]].cpus[0].core
                    self.hypervisor.add_vm(1,self.vcpus,clock,self.ram,self.ssd,1,type+str(id), host[0], host[1])
                    self.hypervisor.powerOnVM(type+str(id), host[0], host[1])
                    self.hypervisor.vms[host[1]][host[0]][type+str(id)].type = type
                    print(type+str(id)+" "+host[1]+" "+host[0]+" added by Round-Robin")
                    return 1
            else:
                flag_affinity = 0
        print("Impossible to allocate according to this Anti-Affinity policy")
        return 0
    def add_module_greedy(self, id, type):
        host = self.hypervisor.best_blade(self.wvcpus,self.wvcpus,self.wssd)
        if(self.hypervisor.check_blade_resources(self.vcpus, self.ram, self.ssd, host[0], host[1])):
            self.modules[type+str(id)] = module(id, type, type+str(id), host[0], host[1])
            clock = self.hypervisor.datacenter[host[1]][host[0]].cpus[0].core
            self.hypervisor.add_vm(1,self.vcpus,clock,self.ram,self.ssd,1,type+str(id), host[0], host[1])
            self.hypervisor.powerOnVM(type+str(id), host[0], host[1])
            self.hypervisor.vms[host[1]][host[0]][type+str(id)].type = type
            print(type+str(id)+" "+host[1]+" "+host[0]+" added by Greedy Selection")
            return 1
        print("No free resources for the most available host")
        return 0
    
    def num_vcpus(self):
        return len(self.modules)*self.vcpus


        #if hypervisor.check_host(guestname, hostname, datacenter):
        #    self.modules[type+str(id)] = module(id, type, hostname, datacenter)
        #    print("Module successfully added!!")
        #else:
        #    print("Please, insert an existent VM!!")
    def config_params(self, vcpus, ram, ssd, wvcpus, wrap, wssd, anti_affinity):
        self.vcpus = vcpus
        self.ram = ram
        self.ssd = ssd
        self.wvcpus = wvcpus
        self.wrap = wrap
        self.wssd = wssd
        self.anti_affinity = anti_affinity



class slice:
    def __init__(self, hypervisor, name):
        self.vnfs = {}
        self.hypervisor = hypervisor
        self.subscribers = 0
        self.name = name
    def add_vnf(self, name):
        vnff = vnf(name, self.hypervisor)
        self.vnfs[name] = vnff
    def list_vnfs(self):
        for s in self.vnfs:
            print(self.vnfs[s].name)
    def add_subscriber(self):
        self.subscribers = self.subscribers + 1 
class route_entry:
    def __init__(self, interface_addr, interface_port, hop_addr, hop_port, cost):
        self.interface_addr = interface_addr
        self.interface_port = interface_port
        self.hop_addr = hop_addr
        self.hop_port = hop_port
        self.cost = cost

class router:
    def __init__(self, n_interfaces):
        self.n_interfaces = n_interfaces
        self.interfaces = []
        self.route_table = []

    def add_route(self, interface_addr, interface_port, hop_addr, hop_port, cost):
        self.route_table.append(route_entry(interface_addr, interface_port, hop_addr, hop_port, cost))

def scale_procedure(slice, vnf, k_scale):
    if slice.subscribers > vnf.num_vcpus()/k_scale:
        print(slice.name)
        i = len(vnf.modules)
        flag_affinity = vnf.add_module(i,vnf.name)
        if(flag_affinity==1):
            print(vnf.name+" added successfully by Round-Robin")
            return 1
        flag_resources = vnf.add_module_greedy(i, vnf.name)
        if(flag_resources==1):
            print(vnf.name+" added violating anti-affinity rules")
            return 1
        print("your datacenter has no free resources. Add more blades, please")
    return 0 


hyper = hypervisor()
dc = "datacenter_default"
hyper.add_datacenter(dc)
for i in range(0,20):
    blade_tmp = blade(2,768,2,10,"host#"+str(i+1))
    blade_tmp.cpu_setup(2.7, 28)
    blade_tmp.cpu_setup(2.7, 28)
    blade_tmp.ssd_setup(10240)
    hyper.add_server(dc,blade_tmp)


#core5g = slice(hyper)
#core5g.add_vnf("AMF")
#core5g.vnfs["AMF"].config_params(12,32,512,1,1,1,10)
#for i in range (0,20):
#    core5g.vnfs["AMF"].add_module(i+1,"AMF")
#core5g.add_vnf("SMF")
#core5g.vnfs["SMF"].config_params(12,32,512,1,1,1,1)
#core5g.list_vnfs()
#for i in core5g.vnfs["AMF"].modules:
#    print(core5g.vnfs["AMF"].modules[i].guestname+"\t"+core5g.vnfs["AMF"].modules[i].hostname+"\t"+core5g.vnfs["AMF"].modules[i].datacenter+"\t"+str(core5g.vnfs["AMF"].num_vcpus()))

eMBBvideo = slice(hyper, "eMBB Video")
eMBBvoice = slice(hyper, "eMBB Voice")

af = 1

critical = random.randrange(8,11)
high = random.randrange(6,8)
moderate = random.randrange(4,6)

eMBBvideo.add_vnf('AMF')
eMBBvideo.vnfs['AMF'].config_params(3,3,6,7,3,1,af)
eMBBvideo.vnfs['AMF'].scale_factor = critical
eMBBvideo.add_vnf('SMF')
eMBBvideo.vnfs['SMF'].config_params(3,3,6,7,7,3,af)
eMBBvideo.vnfs['SMF'].scale_factor = critical
eMBBvideo.add_vnf('UPF')
eMBBvideo.vnfs['UPF'].config_params(24,39,84,5,5,1,af)
eMBBvideo.vnfs['UPF'].scale_factor = high
eMBBvideo.add_vnf('PCF')
eMBBvideo.vnfs['PCF'].config_params(2,3,6,5,3,3,af)
eMBBvideo.vnfs['PCF'].scale_factor = high
eMBBvideo.add_vnf('UDM')
eMBBvideo.vnfs['UDM'].config_params(6,12,30,3,5,1,af)
eMBBvideo.vnfs['UDM'].scale_factor = moderate
eMBBvideo.add_vnf('AF')
eMBBvideo.vnfs['AF'].config_params(6,12,12,3,3,1,af)
eMBBvideo.vnfs['AF'].scale_factor = moderate
eMBBvideo.add_vnf('NEF')
eMBBvideo.vnfs['NEF'].config_params(3,3,6,3,3,1,af)
eMBBvideo.vnfs['NEF'].scale_factor = moderate
eMBBvideo.add_vnf('AUSF')
eMBBvideo.vnfs['AUSF'].config_params(6,12,30,5,3,3,af)
eMBBvideo.vnfs['AUSF'].scale_factor = high
eMBBvideo.add_vnf('NSSF')
eMBBvideo.vnfs['NSSF'].config_params(3,3,6,3,3,1,af)
eMBBvideo.vnfs['NSSF'].scale_factor = moderate
eMBBvideo.add_vnf('NRF')
eMBBvideo.vnfs['NRF'].config_params(3,3,6,5,5,7,af)
eMBBvideo.vnfs['NRF'].scale_factor = high

eMBBvoice.add_vnf('AMF')
eMBBvoice.vnfs['AMF'].config_params(3,3,6,5,3,1,af)
eMBBvoice.vnfs['AMF'].scale_factor = high
eMBBvoice.add_vnf('SMF')
eMBBvoice.vnfs['SMF'].config_params(3,3,6,5,5,3,af)
eMBBvoice.vnfs['SMF'].scale_factor = high
eMBBvoice.add_vnf('UPF')
eMBBvoice.vnfs['UPF'].config_params(15,27,36,3,3,3,af)
eMBBvoice.vnfs['UPF'].scale_factor = moderate
eMBBvoice.add_vnf('PCF')
eMBBvoice.vnfs['PCF'].config_params(2,3,6,5,3,3,af)
eMBBvoice.vnfs['PCF'].scale_factor = high
eMBBvoice.add_vnf('UDM')
eMBBvoice.vnfs['UDM'].config_params(6,12,30,3,5,7,af)
eMBBvoice.vnfs['UDM'].scale_factor = moderate
eMBBvoice.add_vnf('AUSF')
eMBBvoice.vnfs['AUSF'].config_params(6,12,30,5,3,3,af)
eMBBvoice.vnfs['AUSF'].scale_factor = high
eMBBvoice.add_vnf('NSSF')
eMBBvoice.vnfs['NSSF'].config_params(3,3,6,3,3,1,af)
eMBBvoice.vnfs['NSSF'].scale_factor = moderate
eMBBvoice.add_vnf('NRF')
eMBBvoice.vnfs['NRF'].config_params(3,3,6,3,5,7,af)
eMBBvoice.vnfs['NRF'].scale_factor = moderate

slices = [eMBBvideo, eMBBvoice]

loop = 1
while loop:
    new_subs = random.random()

    if new_subs < 0.8:
        eMBBvideo.add_subscriber()
    else:
        eMBBvoice.add_subscriber()
    for s in slices:
        for key, vnfs in s.vnfs.items():
            #print(vnfs.num_vcpus(), key)
            if s.subscribers > (vnfs.num_vcpus()/(vnfs.scale_factor*pow(10,-4))):
                print(s.name)
                i = len(vnfs.modules)
                flag_affinity = vnfs.add_module(i,vnfs.name) #Tenta adicionar por Round-Robbin #fica a dica de especificar
                if(flag_affinity==0):
                    flag_resources = vnfs.add_module_greedy(i,vnfs.name)
                    if(flag_resources==0):
                        print("your datacenter has no free resources. Add more blades, please")
                        #for i in eMBBvideo.vnfs["AMF"].modules:
                        #    print(eMBBvideo.vnfs["AMF"].modules[i].guestname+"\t"+eMBBvideo.vnfs["AMF"].modules[i].hostname+"\t"+eMBBvideo.vnfs["AMF"].modules[i].datacenter+"\t"+str(eMBBvideo.vnfs["AMF"].num_vcpus()))
                        #for i in eMBBvideo.vnfs["SMF"].modules:
                        #    print(eMBBvideo.vnfs["SMF"].modules[i].guestname+"\t"+eMBBvideo.vnfs["SMF"].modules[i].hostname+"\t"+eMBBvideo.vnfs["SMF"].modules[i].datacenter+"\t"+str(eMBBvideo.vnfs["SMF"].num_vcpus()))
                        #exit(1)
                        loop = 0
                        break

for s in slices:
    print(s.name+" "+str(s.subscribers)+" subscribers")
    for key, vnfs in s.vnfs.items():
        for i in vnfs.modules:
            print(vnfs.modules[i].guestname+"\t"+vnfs.modules[i].hostname+"\t"+vnfs.modules[i].datacenter+"\t"+str(vnfs.num_vcpus()))

