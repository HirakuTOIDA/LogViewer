class calibration:
    def __init__(self):
        self.cranc = 60000.0
        self.prop = 90000.0
        self.ias1 = 0.00053
        self.ias2 = 0.35
        self.alt = 0.01
        self.encordermax = 333.3
        self.adcmax = 2**16
        self.aileron1 = 0.38
        self.rudder1 = 0.81
        self.elevetor1 = 0.25
        #操舵試験から求める定数
        self.aileron2 = 28300
        self.rudder2 = 37100
        self.elevetor2 = 18500
