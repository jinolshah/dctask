def intChecker(integer):    # Checking whether RetryCount is an integer greater or equal to zero
    if isinstance(integer, int):
        if integer >= 0:
            return True
        else:
            raise ValueError("RetryCount has to be greater than or equal to zero")
    else:
        raise ValueError("RetryCount has to be an integer greater than or equal to zero")

def verifier(event):
    length = len(event)
    if length not in (2,3):
        raise ValueError("Invalid number of arguments")
    elif event[0] not in ['R', 'S']:
        raise ValueError("EventType can only be either R or S")
    elif length == 2:
        if intChecker(event[1]):
            return "EventRequest"
    elif length == 3:
        if intChecker(event[2]):
            return "EventStatus"

class Queue:
    def __init__(self):
        self.queue = []

    def Push(self, event):
        if isinstance(event, list):
            result = verifier(event)    # Input Validation
            self.queue.append(event)
        else:
            raise ValueError("The input isn't of list type")
    
    def Pop(self):
        if len(self.queue) == 0:
            return None
        else:
            elem = self.queue[0]
            popped = self.queue.pop(0)
            return popped


# --------------------------------------------------------------------------------------------------- #


# 1.Initializing queue
q = Queue()

# 2.Pushing event packets into the queue
packets = [["S", "P", 0], ["R", 0], ["S", "M", 0], ["S", "P", 0], ["S", "T", 0], ["S", "P", 0], ["S", "C", 0], ["S", "M", 0]]    # Input
for pack in packets:
    q.Push(pack)

# 3.Popping elements from queue till queue is empty
status = []
while len(q.queue) > 0:
    popped = q.Pop()
    if popped[0] == "S":
        status.append(popped[1])
        if (popped[1] in ["C", "T"]) and popped[2] < 2:     # Checking StatusType and RetryCount
            popped[2] += 1     # Incrementing RetryCount
            q.Push(popped)
        else:
            print(f"EventStatus: {popped[0]}, {popped[1]}, {popped[2]}")
    else:
        statusLen = len(status)
        if statusLen > 0:
            if status[statusLen-1] in ["C", "T"]:    # Checking last received StatusType
                print(f"EventRequest: {popped[0]}, {popped[1]}")
            else:
                popped[1] += 1     # Incrementing RetryCount
                q.Push(popped)
        else:
            print(f"EventRequest: {popped[0]}, {popped[1]}")    # Outputting if no status previously received