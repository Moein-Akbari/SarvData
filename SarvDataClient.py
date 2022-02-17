# External
import requests

# Internal
import ipaddress
from datetime import datetime


class SarvDataClient:
    def __init__(
        self, api_key: str, api_domain="https://portal.sarvdata.com", api_suffix="/api"
    ):
        r"""Creates a SarvData object for using methods.
        :param api_key: Your account api key. get it from portal.sarvdata.com
        :param api_domain: (optional) site url.
        :param api_suffix: (optional) adds to api_domain and creates api url.
        :return: :class:`SarvData` object
        :rtype: SarvDataClient
        docs > sarvdata.com/blog/instructions-for-using-the-rest-api-web-service/
        """
        self.__api_key = api_key
        self.api_domain = api_domain
        self.api_suffix = api_suffix
        self.account = Account(self)
        self.vms = VMs(self)

    def request(self, url, method, data={}):
        endpoint = f"{self.api_domain}{self.api_suffix}{url}"
        response = requests.request(
            method, url=endpoint, headers={"ApiToken": self.__api_key}, json=data
        ).json()
        if response["Succeed"] != True:
            raise ValueError(response["Exception"])
        elif "Data" in response:
            return response["Data"]
        else:
            response["Succeed"]


class Account:
    def __init__(self, sarvdata_client: SarvDataClient):
        self.sarvdata_client = sarvdata_client

    def who_am_i(self) -> dict:
        r"""
        Returns api owner account's details:
            FirstName
            LastName
            PhoneNumber
            Email
        """
        url = "/whoami"
        return self.sarvdata_client.request(url, method="GET")


class VMs:
    def __init__(self, sarvdata_client: SarvDataClient):
        self.sarvdata_client = sarvdata_client

    def vm_list(self) -> list:
        r"""Returns a list of VM."""
        url = "/vm/list/"
        vm_list = []
        response = self.sarvdata_client.request(url, method="GET")
        for vm in response:
            vm_list.append(
                VM(
                    sarvdata_client=self.sarvdata_client,
                    identity=vm["Id"],
                    disk_name=vm["DiskName"],
                    external_IP_address=ipaddress.ip_address(vm["ExternalIPAddress"]),
                    default_username=vm["DefaultUserName"],
                    default_password=vm["DefaultPassword"],
                    expire_moment=datetime.strptime(
                        vm["ExpireMoment"], "%Y-%m-%dT%H:%M:%S.%f"
                    )
                    if vm["ExpireMoment"]
                    else None,
                    plan_name=vm["PlanName"],
                    startup_memory=vm["StartupMemory"],
                    cpu_cores=vm["CpuCores"],
                    disk_size=vm["DiskSizeGB"],
                    state=vm["State"],
                )
            )
        return vm_list

    def locations(self) -> list:
        r"""Returns locaion list and details."""
        url = "/locations"
        return self.sarvdata_client.request(url, method="GET")

    def create(
        self,
        location_id: int,
        plan_id: int,
        period_type: int,
        disk_id: int,
        count: int,
        coupon="",
    ):
        r"""Creates new VM. THIS MAY COST YOU MONEY
        :param location_id: VM Location, use locations method to get location list.
        :param plan_id: VM Plan, use Plan method to get plan list.
        :param period_type: Use 0 for Monthly, 1 for Weekly, 2 for Daily and 3 for Hourly. Parameters could be changed, Check docs.
        :param disk_id: VM OS, use disks method to get available Operating Systems.
        :param count: count of periods.
        :param coupon: (optional) discount code.
        docs > sarvdata.com/blog/instructions-for-using-the-rest-api-web-service/
        """
        url = "/vm/create"
        data = {
            "LocationId": location_id,
            "PlanId": plan_id,
            "PeriodType": period_type,
            "DiskId": disk_id,
            "Count": count,
            "Coupon": coupon,
        }
        return self.sarvdata_client.request(url, method="POST", data=data)

    def plans(self, location_id: int, period_type: int) -> list:
        r"""Returns plan list and details.
        :param location_id: VM Location, use locations() to get location list.
        :param period_type: Use 0 for Monthly, 1 for Weekly, 2 for Daily and 3 for Hourly. Parameters could be changed, Check docs.
        docs > sarvdata.com/blog/instructions-for-using-the-rest-api-web-service/
        """
        url = f"/locations/{location_id}/plans/{period_type}"
        return self.sarvdata_client.request(url, method="GET")

    def disks(self, location_id: int, period_type: int, plan_id: int) -> list:
        r"""Returns OS list.
        :param location_id: VM Location, use locations method to get location list.
        :param plan_id: VM Plan, use Plan method to get plan list.
        :param period_type: Use 0 for Monthly, 1 for Weekly, 2 for Daily and 3 for Hourly. Parameters could be changed, Check docs.
        docs > sarvdata.com/blog/instructions-for-using-the-rest-api-web-service/
        """
        url = f"/locations/{location_id}/plans/{plan_id}/disks/{period_type}"
        return self.sarvdata_client.request(url, method="GET")


class VM:
    def __init__(
        self,
        sarvdata_client: SarvDataClient,
        identity: int,
        disk_name: str,
        external_IP_address: ipaddress.IPv4Address,
        default_username: str,
        default_password: str,
        expire_moment: datetime,
        plan_name: str,
        startup_memory: int,
        cpu_cores: int,
        disk_size: int,
        state: str,
    ):
        self.sarvdata_client = sarvdata_client
        self.identity = identity
        self.disk_name = disk_name
        self.external_IP_address = external_IP_address
        self.default_username = default_username
        self.default_password = default_password
        self.expire_moment = expire_moment
        self.plan_name = plan_name
        self.startup_memory = startup_memory
        self.cpu_cores = cpu_cores
        self.disk_size = disk_size
        self.state = state

    def __repr__(self):
        return f"<VM {self.identity} {self.external_IP_address} {self.state}>"

    def stop(self) -> bool:
        r"""
        Stops VM. Get vm_id using vm_list().
        """
        url = f"/vm/stop/{self.identity}"
        return self.sarvdata_client.request(url, method="GET")

    def start(self) -> bool:
        r"""
        Starts VM. Get vm_id using vm_list().
        """
        url = f"/vm/start/{self.identity}"
        return self.sarvdata_client.request(url, method="GET")

    def restart(self) -> bool:
        r"""
        Restarts VM. Get vm_id using vm_list().
        """
        url = f"/vm/restart/{self.identity}"
        return self.sarvdata_client.request(url, method="GET")

    def pause(self) -> bool:
        r"""
        Pauses VM. Get vm_id using vm_list().
        """
        url = f"/vm/pause/{self.identity}"
        return self.sarvdata_client.request(url, method="GET")

    def save(self) -> bool:
        r"""
        Saves VM. Get vm_id using vm_list().
        """
        url = f"/vm/save/{self.identity}"
        return self.sarvdata_client.request(url, method="GET")

    def check(self) -> str:
        r"""Returns VM Status
        one of these:
            ["Stopped", "Running", "Paused", "Unknown", "Identifying", "Saved", "Saving"]
        """
        url = f"/vm/check/{self.identity}"
        return self.sarvdata_client.request(url, method="GET")

    def reload(self, disk_id: int, coupon: str):
        r"""Changes OS of VM. ALL DATA WILL BE DELETED!
        :param disk_id: VM OS, use disks method to get available Operating Systems.
        :param coupon: (optional) discount code.
        """
        url = "/vm/reload"
        data = {"VMId": self.identity, "DiskId": disk_id, "Coupon": coupon}
        return self.sarvdata_client.request(url, method="POST", data=data)

    def renew(
        self,
        period_type: int,
        count: int,
        coupon="",
    ):
        r"""Creates new VM. THIS MAY COST YOU MONEY
        :param period_type: Use 0 for Monthly, 1 for Weekly, 2 for Daily and 3 for Hourly. Parameters could be changed, Check docs.
        :param disk_id: VM OS, use disks method to get available Operating Systems.
        :param count: count of period.
        :param coupon: discount code.
        docs > sarvdata.com/blog/instructions-for-using-the-rest-api-web-service/
        """
        url = "/vm/renew"
        data = {
            "VMId": self.identity,
            "PeriodType": period_type,
            "Count": count,
            "Coupon": coupon,
        }
        return self.sarvdata_client.request(url, method="POST", data=data)
