import wmi


def system_info(index=0):
    try:
        computer = wmi.WMI()
        os_info = computer.Win32_OperatingSystem()[0]
        architecture = os_info.OSArchitecture
        os_caption = os_info.Caption.split()
        os = "{} {} {}".format(os_caption[1], os_caption[2], architecture)
        video_controller_arr = computer.Win32_VideoController()
        video_controller_len = len(video_controller_arr)
        gpu_info_arr = video_controller_arr[0].Name.split()
        if index > video_controller_len:
            print("( x ) Can't find a supported GPU ( x )")
        if index > 0:
            gpu_info_arr = video_controller_arr[index].Name.split()
        vendor = gpu_info_arr[0]
        # print(
        #     "\nDetected: \nVendor: {}\nGraphics card: {}\nOS: {}".format(
        #         vendor, " ".join(gpu_info_arr), os
        #     )
        # )
        return {"vendor": vendor, "gpu_info_arr": gpu_info_arr, "os": os}
    except Exception as e:
        print("\n{}".format(e))


# test
# system_info(
