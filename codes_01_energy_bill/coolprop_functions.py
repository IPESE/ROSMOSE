import json
from pyxosmose.state import State

def mixture(T=298, P=101325, frac_water=0.89, frac_fat=0.11):
  
  # call coolprop
  state1 = State(pair='TP',fluid='Water',temperature=T,pressure=P)
  state2 = State(pair='TP',fluid='MethylLinolenate',temperature=T,pressure=P)
  
  state1.StateCalc()
  state2.StateCalc()
  
  # ideal mixture
  state_mix = {}
  state_mix['fluid'] = 'water[' + str(frac_water) + ']&fat[' + str(frac_fat) + ']'
  
  for key in ['density', 'cpmass', 'cvmass', 'enthalpy', 'entropy']:
    state_mix[key] = frac_water * getattr(state1, key) + frac_fat * getattr(state2, key)
  return state_mix



def save_states(states, json_name='results'):
  with open('results/' + json_name + '.json', 'w') as f:
    json.dump(states, f)
  return


      
def load_states(path='results/scenario1.json'):
  with open(path, 'r') as f:
    data = json.loads(f.read())
  return data
