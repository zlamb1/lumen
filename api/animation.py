from enum import Enum

class ParamType(Enum):
    PRIV   = 1,
    BOOL   = 2,
    NUMBER = 3,
    COLOR  = 4

def param_type_to_str(type):
    if type == ParamType.PRIV:
        return 'priv'
    elif type == ParamType.BOOL:
        return 'bool'
    elif type == ParamType.NUMBER:
        return 'number' 
    elif type == ParamType.COLOR:
        return 'color'

class AnimationParam:
    def __init__(self, name, type, desc=None, min=None, max=None, value=None, priv_name=None):
        self.name = name
        self.type = type
        self.desc = desc
        self.min = min
        self.max = max
        self.value = value
        self.priv_name = priv_name or name
        if type == ParamType.BOOL and value is None:
            self.value = False
        if type == ParamType.NUMBER and value is None:
            self.value = 0
        if type == ParamType.COLOR and value is None:
            self.value = [0, 0, 0]

    def parse(self, value):
        if self.type == ParamType.BOOL:
            return value and value != "0" and value.lower() != "false"
        if self.type == ParamType.NUMBER:
            try:
                v = int(value)
            except Exception:
                return None
            if self.min != None and v < self.min:
                return None
            if self.max != None and v > self.max:
                return None
            return v
        if self.type == ParamType.COLOR:
            v = [0, 0, 0]
            value_len = len(value)
            if value[0] != '#' or (value_len != 4 and value_len != 7):
                return None
            for i in range(3):
                if value_len == 4:
                    s = value[i + 1] + value[i + 1]
                else: 
                    s = value[i * 2 + 1:i * 2 + 3]
                try:
                    v[i] = int(s, 16)
                except:
                    return None
            return v
    
    def format_value(self, value):
        if self.type == ParamType.COLOR:
            s = '#'
            s += hex((value[0] & 0xFF))[2:].zfill(2)
            s += hex((value[1] & 0xFF))[2:].zfill(2)
            s += hex((value[2] & 0xFF))[2:].zfill(2)
            return s
        return value

    def to_dict(self):
        paramdict = {
            'name': self.name,
            'type': param_type_to_str(self.type)
        }
        if not self.desc is None:
            paramdict['desc'] = self.desc
        if not self.min is None:
            paramdict['min'] = self.min
        if not self.max is None:
            paramdict['max'] = self.max
        return paramdict
        
class AnimationClass:
    def __init__(self, name, params, cls):
        self.name = name
        self.params = params or []
        self.cls = cls

    def create(self, params = {}):
        vparams = {}
        for param in self.params:
            if param.type == ParamType.PRIV:
                vparams[param] = param.value
                continue
            if param in params:
                value = params.parse(params[param])
                if value is None:
                    continue
                vparams[param] = value
        return self.cls(self.name, self.params, **vparams)

    def to_dict(self):
        params = []
        for param in self.params:
            if param.type == ParamType.PRIV:
                continue
            params.append(param.to_dict()) 
        return {
            'name': self.name,
            'params': params
        }

class Animation:
    def __init__(self, name, params, impl):
        self._name = name
        self._params = params
        self._impl = impl

    def animate(self):
        pass

    def setparam(self, name, value):
        filtered = [param for param in self._params if param.name == name]
        if not filtered:
            return None
        param = filtered[0]
        value = param.parse(value)
        if not value is None:
            self._impl[param.priv_name] = value
            return param.format_value(value)
        return None

    @property
    def state(self):
        _params = []
        params = {
            'name': self.name,
            'paused': self.paused,
        }
        for param in self._params:
            if param.type == ParamType.PRIV:
                continue
            paramdict = param.to_dict()
            paramdict['value'] = param.format_value(getattr(self._impl, param.priv_name, param.value))
            _params.append(paramdict)
        params['params'] = _params
        return params

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def paused(self):
        return self._paused

    @paused.setter
    def paused(self, value):
        self._paused = bool(value)

    @property
    def params(self):
        return self._params

class MockAnimation(Animation):
    def __init__(self, name, params, **kwargs):
        super().__init__(name, params, self)
        for key, value in kwargs.items():
            setattr(self, key, value)
        self._paused = False
    
    def __getitem__(self, key):
        return getattr(self, key)

    def __setitem__(self, key, value):
        setattr(self, key, value)
    