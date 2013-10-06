# retry_times
retry_times = 3

# config the endpoint by the num
def ssh_endpoint(num):
    if num == 0:
        return 22
    else:
        return 12200 + num

# determine if a vm is the controller
def is_controller(num):
    if num == 0:
        return True
    else:
        return False
