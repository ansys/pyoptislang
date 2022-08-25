"""Return free ports."""
# (c) 2021 ANSYS, Inc. Unauthorized use, distribution, or duplication is prohibited.
#
# Check for free ports in a specific range (default=49690-49700)

import os
import socket

portrange = range(49690, 49701)

SOCK = None
PORT = 0

for port in portrange:
    try:
        server_address = ("localhost", port)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if not os.name == "posix":
            # set SO_EXCLUSIVEADDRUSE  socket option to ensure that only this socket
            # will listen on the given port
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_EXCLUSIVEADDRUSE, 1)
        sock.bind(server_address)
        sock.listen(5)
        SOCK = sock
        PORT = port
        break
    except Exception as e:
        PORT = 0
        # print('Failed to listen on port {0}: {1}'.format(port, str(e)))

portrange_str = "({0}-{1})".format(portrange[0], portrange[len(portrange) - 1])
if PORT:
    print("Found free port {0} in range {1}".format(PORT, portrange_str))
else:
    print("No free port found in range {0}".format(portrange_str))

if SOCK is not None:
    try:
        SOCK.close()
    except Exception as ex:
        print("Exception closing socket: {0}".format(str(ex)))
