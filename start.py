from config import NVIDIA_URL, AMD_URL
from system_info import system_info
import nvidia_driver
import amd_driver


def main():
    system = system_info()
    vendor = system["vendor"]
    # vendor = "AMD"
    print("\n(!) {} graphics card detected".format(vendor))
    match vendor:
        case "NVIDIA":
            print(f"\nRunning NVIDIA script\n")
            return nvidia_driver.fetch_nvidia_driver(NVIDIA_URL, system_info)
        case "AMD":
            print(f"\nRunning AMD script")
            return amd_driver.fetch_amd_driver(AMD_URL, system_info)
        case _:
            print("Unsupported graphics card")
            return False


if __name__ == "__main__":
    main()
