from config import NVIDIA_URL, AMD_URL
import nvidia_driver
import amd_driver
from system_info import system_info


def main():
    system = system_info()
    # vendor = system["vendor"]
    vendor = "AMD"
    print("\n(!) {} graphics card detected".format(vendor))
    match vendor:
        case "NVIDIA":
            print("\nGetting driver from {}\n".format(vendor))
            return nvidia_driver.fetch_nvidia_driver(NVIDIA_URL, system_info)
        case "AMD":
            print("\nGetting driver from {}".format(vendor))
            return amd_driver.fetch_amd_driver(AMD_URL, system_info)


if __name__ == "__main__":
    main()
