from string import ascii_lowercase, ascii_uppercase, digits, punctuation
from enum import Enum


class Characters(Enum):
    LowerButton = ascii_lowercase
    UpperButton = ascii_uppercase
    DigitButton = digits
    SpecialButton = punctuation


Characters_Number = {
    'LowerButton': len(Characters.LowerButton.value),
    'UpperButton': len(Characters.UpperButton.value),
    'DigitButton': len(Characters.DigitButton.value),
    'SpecialButton': len(Characters.SpecialButton.value)
}

Generate_Password = (
    'LowerButton', 'UpperButton', 'DigitButton', 'SpecialButton', 'RestarButton'
)
