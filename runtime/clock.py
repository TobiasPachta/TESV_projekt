EVENT_COUNTER = 0



def set_event_counter(new_counter_as_string):
    global EVENT_COUNTER 
    EVENT_COUNTER = int(new_counter_as_string)
    print("New Counter is now " + str(EVENT_COUNTER))
    return EVENT_COUNTER