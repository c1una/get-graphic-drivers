import wmi


def system_info():
    computer = wmi.WMI()
    os_info = computer.Win32_OperatingSystem()[0]
    architecture = os_info.OSArchitecture
    os_caption = os_info.Caption.split()
    os = "{} {} {}".format(os_caption[1], os_caption[2], architecture)
    gpu_info_arr = computer.Win32_VideoController()[0].Name.split()
    vendor = gpu_info_arr[0]
    print(
        "\nDetected: \nVendor: {}\nGraphics card: {}\nOS: {}".format(
            vendor, " ".join(gpu_info_arr), os
        )
    )
    return {"vendor": vendor, "gpu_info_arr": gpu_info_arr, "os": os}


# test
# system_info()
