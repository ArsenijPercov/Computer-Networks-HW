#!/usr/bin/env python2.7
"""p3-template.py:

    This mininet script creates a linear routed multi-hop topology:

        2001:638:709:a::/64 2001:638:709:f::/64 2001:638:709:b::/64
       .------------------..------------------..------------------.

      h1 ------ s1 ------ r1 ------ s0 ------ r2 ------ s2 ------ h2
        eth0          eth0  eth1          eth0  eth1          eth0

     Assign the following IPv6 addresses and prefixes:

     h1-eth0  2001:638:709:a::1/64
     r1-eth0  2001:638:709:a::f/64
     r1-eth1  2001:638:709:f::1/64
     r2-eth0  2001:638:709:f::2/64
     r2-eth1  2001:638:709:b::f/64
     h2-eth0  2001:638:709:b::1/64

     Debugging hints:

     - If you get a 'network unreachable' error, then most likely a
       forwarding table entry is missing somewhere or wrong.
     - If you get a 'destination unreachable' error, then most likely
       neighbor discovery failed somewhere.
     - Use the 'ip -6 address', 'ip -6 route', and 'ip -6 neigh'
       commands to inspect the forwarding tables and the neighbor
       mapping tables.
     - If pings from h1 to h2 do not work, try to ping r1 from h1 and
       try to ping r1 from h2. (Test whether the links work first.)
     - You can print the result of the configuration commands to see
       whether any errors occurred.
     - You can run tcpdump (or even wireshark) to capture packets in
       order to see what is going on.
"""

from mininet.cli import CLI
from mininet.net import Mininet
from mininet.nodelib import LinuxBridge
from mininet.log import setLogLevel

if __name__ == '__main__':
    setLogLevel('info')

    net = Mininet(switch=LinuxBridge, controller=None)

    h1 = net.addHost('h1', ip=None)
    # create rest of the topology here
    h2 = net.addHost('h2', ip=None)
    s0 = net.addSwitch('s0')
    s1 = net.addSwitch('s1')
    s2 = net.addSwitch('s2')
    r1 = net.addHost('r1', ip=None)
    r1.cmd("sysctl -w net.ipv6.conf.all.forwarding=1")
    r2 = net.addHost('r2', ip=None)
    r2.cmd("sysctl -w net.ipv6.conf.all.forwarding=1")
 
    net.addLink(h1,s1)
    net.addLink(s1,r1)
    net.addLink(r1,s0)
    net.addLink(s0,r2)
    net.addLink(r2,s2)
    net.addLink(s2,h2)

    # configure IPv6 addresses and forwarding table entries here
    print(h1.cmd("ip -6 address add 2001:638:709:a::1/64 dev h1-eth0"))
    print(r1.cmd("ip -6 address add 2001:638:709:a::f/64 dev r1-eth0"))
    print(r1.cmd("ip -6 address add 2001:638:709:f::1/64 dev r1-eth1"))
    print(r2.cmd("ip -6 address add 2001:638:709:f::2/64 dev r2-eth0"))
    print(r2.cmd("ip -6 address add 2001:638:709:b::f/64 dev r2-eth1"))
    print(h2.cmd("ip -6 address add 2001:638:709:b::1/64 dev h2-eth0"))

    print(h1.cmd("ip route add 2001:638:709::/48 via 2001:638:709:a::f dev h1-eth0"))

    print(r1.cmd("ip route add 2001:638:709:b::/64 via 2001:638:709:f::2 dev r1-eth1"))

    print(r2.cmd("ip route add 2001:638:709:a::/64 via 2001:638:709:f::1 dev r2-eth0"))
    
    print(h2.cmd("ip route add 2001:638:709::/48 via 2001:638:709:b::f dev h2-eth0"))
    net.start()
    CLI(net)
    net.stop()