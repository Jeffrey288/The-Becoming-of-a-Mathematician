"""
pyText.py
"""

"""
TextWrap(text, font, width, shift, color = (0, 0, 0)) --> List
TextRender(lines, font, spacing, alignment = 'left', color = (0, 0, 0)) --> Surface
"""

'''
Pending:
- Add text formatting
'''

import pygame

# TextWrap(text, font, width, shift = 0, color = (0, 0, 0))
def TextWrap(text, font, width, shift = 0, color = (0, 0, 0)):

    counter = 0
    displayWidth = width - 2 * shift
    words = text.split(" ")
    widthCounter = 0
    lines = [[]]
    newLine = False
    spaceWidth = font.size(' ')[0]
    
    for i in words:
        newLine = '\n' in i
        # For newline characters
        if newLine:
            temp2 = i.split("\n")
            j = temp2[0]
        else:
            j = i

        nowWidth = font.size(j)[0]
        if widthCounter + nowWidth + spaceWidth >= displayWidth:
            # Newline
            lines.append([])
            # Reset widthCounter
            widthCounter = nowWidth + spaceWidth
        else:
            # Add to width
            widthCounter += nowWidth + spaceWidth
        # Add word
        lines[-1].append(j + ' ')

        if newLine:
            if len(temp2) == 2:
                lines.append([temp2[-1] + ' '])
                widthCounter = font.size(temp2[-1] + ' ')[0]
            else:
                for k in temp2[1:]:
                    lines.append([k + ' '])
                    widthCounter = font.size(k + ' ')[0]

    for i in range(len(lines)):
        lines[i] = ''.join(lines[i])
        lines[i] = lines[i].rstrip(' ')

    return lines

# TextRender(lines, font, spacing, alignment = 'left', color = (0, 0, 0))
def TextRender(lines, font, spacing, alignment = 'left', color = (0, 0, 0)):

    # Initiation
    renderline = []
    renderwidth = 0
    renderheight = 0

    # Reading Lines
    # Generating Surfaces
    # Calculating Surface Dimensions
    for i in lines:
        k = font.render(i, 1, color)
        renderline.append(k)
        w = k.get_width()
        if w > renderwidth:
            renderwidth = w
        renderheight += k.get_height()
    renderheight += spacing * (len(renderline) - 1)

    # Create Surface, set Per-pixel Alpha
    textSurf = pygame.Surface((renderwidth, renderheight), pygame.SRCALPHA, 32)
    # Surface alpha: textSurf.set_alpha(256)
    # Colorkey: textSurf.set_colorkey((0, 0, 0))

    # Blit text on Surface
    topCoord = 0
    for i in renderline:
        tempRect = i.get_rect()
        tempRect.top = topCoord
        if alignment == 'left':
            tempRect.left = 0
        elif alignment == 'center':
            tempRect.centerx = renderwidth/2
        elif alignment == 'right':
            tempRect.right = renderwidth
        topCoord += tempRect.height + spacing
        textSurf.blit(i, tempRect)

    return textSurf


# Main: Testing
if __name__ == "__main__":

    SCALE = 1.5
    def Scale(metric):
        return int(metric // SCALE)

    ScreenWidth = Scale(1280)
    ScreenHeight = Scale(960)
    TextShift = Scale(25)
    TextHeight = Scale(300)

    pygame.init()
    
    Screen = pygame.display.set_mode((ScreenWidth, ScreenHeight))
    Screen.fill((255, 0, 255))
    
    TextSurf = pygame.Surface((ScreenWidth - 2 * TextShift, TextHeight))
    TextSurf.fill((255,255,255))

    BasicFont = pygame.font.Font('assets/times.ttf', 40)

    something = TextWrap("やんでれ ²　somewhere over the works, waaaaaaaaay\nhigh\ni like to fly in the sky", BasicFont, ScreenWidth - 2 * TextShift, TextShift)
    hhh = TextRender(something, BasicFont, 10, color = (0, 255, 0))
    Screen.blit(hhh, (0,0))
    pygame.display.flip()

    input()
