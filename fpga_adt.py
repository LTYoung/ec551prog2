################################################
# fpga_adt.py
# Andrew Woska
# agwoska@bu.edu
################################################
# may be replaced with something else later
################################################

class fpga_adt:
    def __init__(self):
        self.layout = []
        self.wire = []
        self.inputs = []
        self.outputs = []
        self.lut_type = 0
        self.luts = []
        self.connectivity = []
        self.eqs = []
        self.reqs = []
        self.fromBitstream = False
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

    ''' isFullyConnected
    if connectivity is empty, then the fpga is fully connected
    else the fpga is partially connected and a scheme has been provided
    in get_connectivity()
    '''
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

# end fpga_adt

class LUT:
    def __init__(self, name, tLut):
        self.name = name
        self.type = tLut
        self.op = ''
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
    
# end LUT
