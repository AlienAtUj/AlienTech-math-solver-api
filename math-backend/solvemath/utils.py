import re

def extract_equations(text: str) -> list[str]:
   
    text = text.lower()

    
    text = re.sub(r'\bsolve\b|\bequation\b|\bsimultaneously\b', '', text)

    
    text = re.sub(r'\band\b|,|\n', ';', text)

    
    parts = [p.strip() for p in text.split(';') if p.strip()]

    equations = []
    for eq in parts:
    
        eq = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', eq)
        eq = re.sub(r'([a-zA-Z])(\d)', r'\1*\2', eq)
        eq = re.sub(r'([a-zA-Z])([a-zA-Z])', r'\1*\2', eq)  

     
        eq = eq.replace('^', '**')

  
        eq = re.sub(r'\s*([=+\-*/^()])\s*', r'\1', eq)

        if '=' not in eq:
            eq += '=0'

        equations.append(eq)

    return equations
import re

def extract_equations_from_text(text):
    """
    Extracts mathematical equations and inequalities from a block of text.
    Returns a list of string equations or inequalities.
    """

    text = text.replace('^', '**')

    equation_pattern = r"""
        (?<!\w)                     
        ([\w\.\*\+\-/()]+            
        \s*(=|<=|>=|<|>)\s*          
        [\w\.\*\+\-/()]+)           
        (?!\w)                     
    """

    matches = re.findall(equation_pattern, text, re.VERBOSE)

    
    return [match[0].strip() for match in matches]
