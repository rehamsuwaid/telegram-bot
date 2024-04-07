import json


def function_signature_to_abi(function_signature):
    parts = function_signature.split('(')
    name = parts[0]
    inputs = parts[1].split(')')[0].split(',')
    outputs = parts[2].split(')')[0].split(',')
    inputs_json = [{"internalType": t.strip(), "name": "", "type": t.strip()}
                   for t in inputs]
    outputs_json = [{"internalType": t.strip(), "name": "", "type": t.strip()}
                    for t in outputs]
    return [{
        "constant": True,
        "inputs": inputs_json,
        "name": name,
        "outputs": outputs_json,
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    }]


# Example usage
# function_signature = "balanceOf(address)(uint256)"
# abi = function_signature_to_abi(function_signature)
# print(json.dumps(abi, indent=4))
