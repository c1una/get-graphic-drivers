from mimetypes import init
from config import NVIDIA_URL, AMD_URL
from system_info import system_info
import nvidia_driver
import amd_driver


def main():
    index = 0
    system = system_info()
    gpu_vendor = system["vendor"]
    # gpu_vendor = "AMD"
    # gpu_vendor = "NVIDIA"
    # gpu_vendor = "1"
    print("\n(!) {} graphics detected (!)".format(gpu_vendor))

    def match_vendor(vendor):
        nonlocal index
        match vendor:
            case "NVIDIA":
                print(f"\nRunning NVIDIA script\n")
                return nvidia_driver.fetch_nvidia_driver(NVIDIA_URL, system_info)
            case "AMD":
                print(f"\nRunning AMD script")
                return amd_driver.fetch_amd_driver(AMD_URL, system_info)
            case _:
                print(f"\nUnsupported graphics card")
                print("Trying to find another GPU...")
                index += 1
                match_vendor(system_info(index=index)["vendor"])

    match_vendor(gpu_vendor)


if __name__ == "__main__":
    main()
