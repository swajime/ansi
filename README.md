# SwaANSI

* Tested on: os: [ubuntu-16.04, ubuntu-latest, macos-latest, windows-latest]
* Tested on: python-version: [2.7, 3.5, 3.6, 3.7, 3.8, pypy2, pypy3]

![Python package](https://github.com/swajime/ansi/workflows/Python%20package/badge.svg)

Enable wrapping text with color and attributes per ANSI escape sequences.

## ANSI wrapper for text strings

<p>This class allows the user to wrap strings with ansi color escape sequences
without the user having to know how they work.</p>

<p>Examples follow:</p>

<p>Note that not all styles work on all terminals.
Also note that some styles do not mix well with colors.</p>

<p>To see colors available, view SwaANSI.colors</p>

    from swajime import SwaANSI
    print(SwaANSI.colors)
    for color in sorted(SwaANSI.colors): print(SwaANSI.wrap(color, color))
    
<p>To see styles available, view SwaANSI.styles</p>

    from swajime import SwaANSI
    print(SwaANSI.styles)
    for style in sorted(SwaANSI.styles): print(SwaANSI.wrap(style, None, None, style))
    
<p>The class can be accessed without instances:</p>

    from swajime import SwaANSI
    print(SwaANSI.wrap('This is red text', 'Red', 'Yellow', 'Bold', 'Underline', 'Strikethrough'))

<p>Or you can create different objects with different attributes:</p>

    from swajime import SwaANSI
    greenSuccess = SwaANSI('Green', None, 'Bold')
    yellowWarning = SwaANSI('Yellow', None, 'Underline')
    redError = SwaANSI('Red', None, 'Double Underline')
    
    print(greenSuccess.wrap('This is a green success'))
    print(yellowWarning.wrap('This is a yellow warning'))
    print(redError.wrap('This is a red error'))
    
<p>Please report any bugs or issues to john@swajime.com</p>
