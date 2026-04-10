
from pox.core import core
import pox.openflow.libopenflow_01 as of

log = core.getLogger()

mac_to_port = {}

def _handle_ConnectionUp(event):
    log.info("Switch %s connected", event.dpid)
    mac_to_port[event.dpid] = {}

def _handle_PacketIn(event):
    packet = event.parsed

    if not packet:
        return

    dpid = event.dpid
    in_port = event.port

    src = packet.src
    dst = packet.dst


    def get_host(mac):
        mac_str = str(mac)
        if mac_str.endswith("01"):
            return "h1"
        elif mac_str.endswith("02"):
            return "h2"
from pox.core import core
import pox.openflow.libopenflow_01 as of

log = core.getLogger()

mac_to_port = {}

def _handle_ConnectionUp(event):
    log.info("Switch %s connected", event.dpid)
    mac_to_port[event.dpid] = {}

def _handle_PacketIn(event):
    packet = event.parsed

    if not packet:
        return

    dpid = event.dpid
    in_port = event.port

    src = packet.src
    dst = packet.dst

    src_ip = None
    dst_ip = None

    ip_packet = packet.find('ipv4')
    if ip_packet:
        src_ip = str(ip_packet.srcip)
        dst_ip = str(ip_packet.dstip)


    def get_host_from_ip(ip):
        if ip == "10.0.0.1":
            return "h1"
        elif ip == "10.0.0.2":
            return "h2"
        else:
            return ip

    if src_ip and dst_ip:
        src_host = get_host_from_ip(src_ip)
        dst_host = get_host_from_ip(dst_ip)
    else:
        src_host = str(src)
        dst_host = str(dst)


    log.info("[PATH TRACE] s%s | %s -> %s", dpid, src_host, dst_host)


    mac_to_port[dpid][src] = in_port

    if dst in mac_to_port[dpid]:
        out_port = mac_to_port[dpid][dst]
    else:
        out_port = of.OFPP_FLOOD

    msg = of.ofp_packet_out()
    msg.data = event.ofp
    msg.in_port = in_port
    msg.actions.append(of.ofp_action_output(port=out_port))

    event.connection.send(msg)

def launch():
    core.openflow.addListenerByName("ConnectionUp", _handle_ConnectionUp)
    core.openflow.addListenerByName("PacketIn", _handle_PacketIn)
    log.info("Path Tracing + Forwarding Started")
