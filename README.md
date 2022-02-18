# Python SarvData API Client
---
<p align="center">
  <a href="https://sarvdata.com/" rel="noopener">
  <img src="https://sarvdata.com/images/main-slide-img1.svg" alt="SarvData"></a>
</p>


---

## Installing
Clone code:
```
git clone https://github.com/Moein-Akbari/SarvData.git
```
After cloning the project install python required libraries using this command:
```
pip install -r requirements.txt
```

Now you need yo get `<TOKEN>` from https://portal.sarvdata.com/ApiManager

_Documentation_ https://sarvdata.com/blog/instructions-for-using-the-rest-api-web-service

## Examples

### SarvDataClient Object:
```
from SarvDataClient import SarvDataClient
sarv_client = SarvDataClient("<TOKEN>")
```
### Get account information:
```
sarv_client.account.who_am_i()
```
### Get VM list
```
virtual_machines = sarv_client.vms.vm_list() # Returns a list of <VM>s
my_vm = virtual_machines[0]
```
### Parameters For Creating VM
> Period Types
 Parameters could be changed, Check docs.
* 0 for Monthly
* 1 for Weekly
* 2 for Daily 
* 3 for Hourly. 
```
period_type = 3 # Hourly
```
> Count of period.
```
# 2 Hours
count = 2
```
> Location
```
locations = sarv_client.vms.locations()
for location in locations:
    if location["Title"] == "آمریکا | سرور های مجازی SSD":
        location_id = location["Id"]
        break
```
> Plans 
```
plans = sarv_client.vms.plans(location_id, period_type)
for plan in plans:
    if plan["StartupMemory"] == 2048 and plan["CpuCores"] == 2:
        plan_id = plan["Id"]
        break
```
> Operating System (disk)
```
disks = sarv_client.vms.disks(location_id, period_type, plan_id)
for disk in disks:
    if disk["Title"] == "Win Server 2019 x64":
        disk_id = disk["Id"]
        break
```
> Create a VM 
* :warning: **THIS MAY COST YOU MONEY!** :warning:
```
sarv_client.vms.create(location_id, plan_id, period_type, disk_id, count)
virtual_machines = sarv_client.vms.vm_list() # Update VM list
```
### VM Attributes
```
# VM ID
my_vm.identity

# VM OS
my_vm.disk_name

# VM IP Address : ipaddress.IPv4Address
my_vm.external_IP_address 

# VM Authentication Default Values
my_vm.default_username
my_vm.default_password

# VM Expire Date : datetime
my_vm.expire_moment

# VM Details
my_vm.plan_name
my_vm.startup_memory # MB
my_vm.cpu_cores
my_vm.disk_size # GB
my_vm.state
```
### VM Methods
```
# shutdown
my_vm = VM()
my_vm.stop()

# start
my_vm.start()

# restart
my_vm.restart()

# pause
my_vm.pause()

# save
my_vm.save()

# check status
my_vm.check()

# renew
period_type = 3 # Daily
count = 2 # 2 Days
coupon = "" # Discount code
my_vm.renew(period_type, count, coupon)
```
* :warning:  VM.reload Method changes os and **DELETES all data on your VM**. :warning:
```
# change OS
disk_id = 1012 # VM OS, use disks method to get available Operating Systems.
my_vm.reload(disk_id)
```
