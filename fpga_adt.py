################################################
# fpga_adt.py
# Andrew Woska
# agwoska@bu.edu
################################################
# may be replaced with something else later
################################################
import json
import eq_adt as eq


class fpga_adt:
    def __init__(self):
        self.layout = []
        self.wire = []
        self.inputs = []
        self.outputs = []
        self.output_lut_name = {}
        self.lut_type = 0
        self.luts = []
        self.connectivity = []
        self.eqs = []
        self.reqs = []
        self.fromBitstream = False
        self.luts_utilized = 0
        self.io_utilized = 0

    # end __init__

    def update_layout(self, layout):
        self.layout = layout

    # end update_layout

    def update_wire(self, wire):
        self.wire = wire

    # end update_wire

    def update_inputs(self, inputs):
        self.inputs = inputs

    # end update_inputs

    def update_outputs(self, outputs):
        self.outputs = outputs

    # end update_outputs

    def update_luts(self, luts):
        self.luts = luts

    # end update_luts

    def update_connectivity(self, connectivity):
        self.connectivity = connectivity

    # end update_lut_data

    def update_eqs(self, eqs):
        self.eqs = eqs

    # end update_eqs

    def update_lut_type(self, lut_type):
        self.lut_type = lut_type

    # end update_lut_type

    def update_reqs(self, reqs):
        self.reqs = reqs

    # end update_reqs

    def get_layout(self):
        return self.layout

    # end get_layout

    def get_wire(self):
        return self.wire

    # end get_wire

    def get_inputs(self):
        return self.inputs

    # end get_inputs

    def get_outputs(self):
        return self.outputs

    # end get_outputs

    def get_luts(self):
        return self.luts

    # end get_luts

    def get_connectivity(self):
        return self.connectivity

    # end get_lut_data

    def get_eqs(self):
        return self.eqs

    # end get_eqs

    def get_lut_type(self):
        return self.lut_type

    # end get_lut_type

    def get_reqs(self):
        return self.reqs

    # end get_reqs

    def isBitstream(self):
        return self.fromBitstream

    # end get_fromBitstream

    """ isFullyConnected
    if connectivity is empty, then the fpga is fully connected
    else the fpga is partially connected and a scheme has been provided
    in get_connectivity()
    """

    def isFullyConnected(self):
        return self.connectivity == []

    # end isFullyConnected

    def add_lut(self, lut):
        self.luts.append(lut)

    # end add_lut

    def add_eq(self, eq):
        self.eqs.append(eq)

    # end add_eq

    def add_req(self, req):
        self.reqs.append(req)

    # end add_req

    def update_utilization(self):
        num_luts_used = 0
        for lut in self.luts:
            if lut.get_op() != "":
                num_luts_used += 1
        self.luts_utilized = num_luts_used

    @classmethod
    def load_bitstream(cls, filepath):
        with open(filepath, "r") as file:
            data = json.load(file)

        fpga_instance = cls()

        # Reconstruct LUT objects
        if "luts" in data:
            fpga_instance.luts = [
                LUT(lut_data.get("name"), lut_data.get("type"))
                for lut_data in data["luts"]
            ]
            for lut_instance, lut_data in zip(fpga_instance.luts, data["luts"]):
                lut_instance.set_op(
                    lut_data.get("op", {})
                )  # Handle eq_adt reconstruction
                lut_instance.inputs = lut_data.get("inputs", [])
                lut_instance.output = lut_data.get("output", "")
                lut_instance.location = lut_data.get("location", [])
                lut_instance.connections = lut_data.get("connections", [])
                lut_instance.data = lut_data.get("data", {})

        # Set other attributes
        for key, value in data.items():
            if key != "luts" and hasattr(fpga_instance, key):
                setattr(fpga_instance, key, value)

        fpga_instance.fromBitstream = True

        return fpga_instance


# end fpga_adt


class LUT:
    def __init__(self, name, tLut):
        self.name = name
        self.type = tLut
        self.op = ""
        self.inputs = []
        self.output = ""
        self.location = []
        self.connections = []
        self.data = {}

    # end __init__

    def update_name(self, name):
        self.name = name

    # end update_name

    def update_op(self, op):
        self.op = op

    # end update_op

    def update_location(self, location):
        self.location = location

    # end update_location

    def update_connections(self, connections):
        self.connections = connections

    # end update_connections

    def get_name(self):
        return self.name

    # end get_name

    def get_op(self):
        return self.op

    # end get_op

    def get_location(self):
        return self.location

    # end get_location

    def get_connections(self):
        return self.connections

    # end get_connections

    def __repr__(self):
        return self.name

    def set_op(self, op_data):
        if isinstance(op_data, dict):
            # Create an eq_adt instance using the dictionary data
            self.op = eq.eq_adt(op_data.get("eq", ""))
            self.op.literals = op_data.get("literals", [])
            self.op.neglist = op_data.get("neglist", [])
            self.op.ops = op_data.get("ops", [])
            self.op.table = op_data.get("table", {})
            self.op.name = op_data.get("name", "")
            self.op.isCircuit = op_data.get("isCircuit", False)
        else:
            self.op = op_data


# end LUT
