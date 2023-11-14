################################################
# fpga_adt.py
# Andrew Woska
# agwoska@bu.edu
################################################
# Current implemenation created by ChatGPT-3.5
################################################
# may be replaced with something else later
################################################

class fpga_adt:
    def __init__(self, data):
        self.layout = data.get("layout", [])
        self.wire = data.get("wire", [])
        self.inputs = data.get("input", [])
        self.outputs = data.get("output", [])
        self.luts = [LUT(lut_data) for lut_data in data.get("luts", [])]
        self.lut_data = []
    # end __init__
# end fpga_adt

class LUT:
    def __init__(self, data):
        self.name = data.get("name", "")
        self.type = data.get("type", 0)
        self.op = data.get("op", "")
        self.location = data.get("location", [])
        self.connections = data.get("connections", [])
    # end __init__
# end LUT
