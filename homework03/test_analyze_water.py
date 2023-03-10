from analyze_water import turbidity, decay 
import pytest


def test_turbidity():
        assert turbidity(7.3,6.1) == 44.53
        assert turbidity(1.3,4.1) == 5.33
        assert turbidity(2.4,6.7) == 16.08
        assert turbidity(8.8,9.1) == 80.08
        assert isinstance(turbidity(1.7,3.5), float) == True  
         

def test_decay():
        assert decay(1.5,1.0,0.02) == 20.07
        assert decay(2.3,1.0,0.02) == 41.23
        assert decay(8.1,1.0,0.02) == 103.54
        assert isinstance(decay(1.9,1,0.02), float) == True
        
