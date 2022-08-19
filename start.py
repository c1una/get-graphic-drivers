from mimetypes import init
from config import NVIDIA_URL, AMD_URL
from system_info import system_info
import nvidia_driver
import amd_driver


def main():
    index = 0
    system = system_info()
    # print("\n(!) {} graphics detected (!)".format(gpu_vendor))

    def match_vendor(system):
        nonlocal index
        vendor = system["vendor"]
        # gpu_vendor = system["vendor"]
        # vendor = "AMD"
        # gpu_vendor = "NVIDIA"
        # vendor = "fsdf"
        try:
            match vendor:
                case "NVIDIA":
                    print(f"\nRunning NVIDIA script\n")
                    return nvidia_driver.fetch_nvidia_driver(NVIDIA_URL, system)
                case "AMD" | "Radeon":
                    print(f"\nRunning AMD script")
                    return amd_driver.fetch_amd_driver(AMD_URL, system)
                case _:
                    print(f"\nUnsupported graphics card")
                    print("Trying to find another GPU...")
                    index += 1
                    match_vendor(system_info(index=index))
        except Exception as e:
            print("\n{}".format(e))
            input("Press enter to quit:")

    match_vendor(system)


if __name__ == "__main__":
    main()
