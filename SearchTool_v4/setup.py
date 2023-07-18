class Setup:
    def __init__(self):
        self._aType = 0
        self._alpha = 0.
        self._delta = 0.
        self._dx = 0.

    def setVariables(self, parameters):
        self._aType = parameters['aType']
        self._alpha = parameters['alpha']
        self._delta = parameters['delta']
        self._dx = parameters['dx']
       
    def getAType(self):
        return self._aType
    
    def getDelta(self):
        return self._delta
    
    def getAlpha(self):
        return self._alpha
    
    def getDx(self):
        return self._dx
