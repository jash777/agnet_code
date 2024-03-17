# rule.py

from iptc import Table, Chain, Rule, Match, Target
import logging
import iptc
import ipaddress

logging.basicConfig(filename='Rule.log', level=logging.INFO)
logger = logging.getLogger(__name__)

def add_iptables_rule(protocol, destination_port, action):
    try:
        rule = iptc.Rule()
        rule.protocol = protocol
        chain = iptc.Chain(iptc.Table(iptc.Table.FILTER), "INPUT")

        # Create the target based on the action
        target = rule.create_target(action.upper())

        # Create the match based on protocol
        match = None
        if protocol.lower() == 'tcp':
            match = rule.create_match("tcp")
        elif protocol.lower() == 'udp':
            match = rule.create_match("udp")
        # Add more conditions for other protocols if necessary

        # Set the destination port
        if match:
            match.dport = str(destination_port)
        
        # Insert the rule into the chain
        chain.insert_rule(rule)
        
        logging.info("Iptables rule added successfully.")
    except iptc.IPTCError as e:
        logging.error(f"IPTCError: {e}")
        # Handle IPTC specific errors
    except Exception as e:
        logging.error(f"Error adding iptables rule: {e}")
        raise  # Re-raise the exception for error handling in the caller

def block_port(port):
    # Create a new rule
    rule = iptc.Rule()
    rule.protocol = "tcp"
    rule.target = iptc.Target(rule, "DROP")
    match = rule.create_match("tcp")
    match.sport = str(port)
    rule.add_match(match)

    # Insert the rule at the beginning of the INPUT chain
    chain = iptc.Chain(iptc.Table(iptc.Table.FILTER), "INPUT")
    chain.insert_rule(rule)


def inbound_rule(inbound_rule_data):
    """Adds an iptables rule to the INPUT chain allowing inbound traffic based on
       the specified protocol, port, and source IP.

    Args:
        inbound_rule_data (dict): Dictionary containing the inbound rule data.

    Returns:
        bool: True if the rule was added successfully, False otherwise.
    """
    try:
        rule = iptc.Rule()
        rule.protocol = inbound_rule_data['protocol']

        chain = iptc.Chain(iptc.Table(iptc.Table.FILTER), "INPUT")

        logging.info("Received inbound rule data: %s", inbound_rule_data)

        if inbound_rule_data['protocol'].lower() in ['tcp', 'udp']:
            match = rule.create_match(inbound_rule_data['protocol'])
            match.dport = str(inbound_rule_data['port'])

        if 'source_ip' in inbound_rule_data:
            rule.src = inbound_rule_data['source_ip']

        rule.create_target("ACCEPT")
        chain.insert_rule(rule)

        logging.info("Iptables rule added successfully.")
        return True
    except iptc.IPTCError as e:
        logging.error("IPTCError occurred while adding iptables rule: %s", e)
        return False
    except KeyError as e:
        logging.error("KeyError occurred while adding iptables rule: %s", e)
        return False
    except Exception as e:
        logging.error("Error occurred while adding iptables rule: %s", e)
        return False



def outbound_rule(outbound_rule_data):
    """Adds an iptables rule to the OUTPUT chain allowing outbound traffic based on
       the specified protocol, port, and destination IP.

    Args:
        outbound_rule_data (dict): Dictionary containing the outbound rule data.

    Returns:
        bool: True if the rule was added successfully, False otherwise.
    """
    try:
        rule = iptc.Rule()
        rule.protocol = outbound_rule_data['protocol']

        chain = iptc.Chain(iptc.Table(iptc.Table.FILTER), "OUTPUT")

        logging.info("Request payload: %s", outbound_rule_data)

        if outbound_rule_data['protocol'].lower() in ['tcp', 'udp']:
            match = rule.create_match(outbound_rule_data['protocol'])
            match.sport = str(outbound_rule_data['port'])

        if 'destination_ip' in outbound_rule_data:
            rule.dst = outbound_rule_data['destination_ip']
        else:
            # Allow traffic with an empty destination IP address
            rule.dst = ''

        rule.create_target("DROP")
        chain.insert_rule(rule)

        logging.info("Iptables rule added successfully.")
        return True
    except iptc.IPTCError as e:
        logging.error("IPTCError occurred while adding iptables rule: %s", e)
        return False
    except KeyError as e:
        logging.error("KeyError occurred while adding iptables rule: %s", e)
        return False
    except Exception as e:
        logging.error("Error occurred while adding iptables rule: %s", e)
        return False
