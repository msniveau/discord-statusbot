def banner_message(length, message):
    l2=length-int(round((len(message)/2)))
    response=''
    while l2 != 0:
        response+=' '
        l2=l2-1
    response+=message
    return response

