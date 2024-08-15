from importlib.metadata import requires
import math

def calculate_network_components(current_nics, future_nics, leafports, spineports, reserved_ports, topology):
    # Calculate total NICs
    total_nics = current_nics + future_nics
    
    # Effective ports on a leaf switch
    effective_ports = leafports - reserved_ports

    if total_nics <= leafports:
        return ("The solution is supported on a single switch")
    
    # Calculate the number of downlink ports and ensure uplink ports are 16% higher
    requires_uplinks = total_nics * 1.16

    total_leaf = math.ceil((requires_uplinks + total_nics) / effective_ports)

    # Number of spine switches required 
    # Calculate the required number of spine switches, accounting for non-blocking spine-to-spine connections
    uplink_per_leaf = requires_uplinks / total_leaf


    spine_switches = 1
    while spine_switches * (spineports - (spine_switches - 1)) < total_uplink_ports:
        spine_switches += 1
        if spine_switches > spineports:
            return "Not possible with input values"
    
    # Calculate the number of cables required
    cables = total_uplink_ports  # One cable per uplink port
    
    # Add spine-to-spine connection cables (non-blocking)
    spine_to_spine_cables = (spine_switches * (spine_switches - 1)) // 2
    
    # Total cables
    total_cables = cables + spine_to_spine_cables
    
    return leaf_switches, spine_switches, total_cables

def main():
    # Input from the user
    """current_nics = int(input("Enter the number of current GPU NICs: "))
    future_nics = int(input("Enter the number of future GPU NICs: "))
    leafports = int(input("Enter the number of ports on the leaf switch: "))
    spineports = int(input("Enter the number of ports on the spine switch: "))
    reserved_ports = int(input("Enter the number of reserved ports: "))
    topology = int(input("Enter the topology (2 for 2-tier, 3 for 3-tier): "))"""

    current_nics = 54
    future_nics = 0
    leafports = 48
    spineports = 48
    reserved_ports = 0
    topology = 2
    
    # Calculate components
    result = calculate_network_components(current_nics, future_nics, leafports, spineports, reserved_ports, topology)
    
    # Output the results
    if isinstance(result, str):
        print(result)
    else:
        leaf_switches, spine_switches, total_cables = result
        print(f"Number of leaf switches required: {leaf_switches}")
        print(f"Number of spine switches required: {spine_switches}")
        print(f"Number of cables required: {total_cables}")

if __name__ == "__main__":
    main()