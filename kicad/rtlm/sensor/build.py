"""Generate TPS-01 KiCad sources with the KiCad 10 bundled Python."""
import json
from pathlib import Path
import sys
from uuid import uuid4

import pcbnew as pcb

HERE = Path(__file__).resolve().parent
NAME = 'tps-01'
LIB = Path(r'C:/Program Files/KiCad/10.0/share/kicad/footprints')
CONNECTOR = 'Molex_Micro-Fit_3.0_43045-0400_2x02_P3.00mm_Horizontal'
J1 = 'Connector_Molex:' + CONNECTOR
R = 'Resistor_SMD:R_0603_1608Metric'
C = 'Capacitor_SMD:C_0603_1608Metric'
HEADER = 'Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Vertical'
HALL = 'Package_SO:SOIC-8_3.9x4.9mm_P1.27mm'
AMP = 'Package_TO_SOT_SMD:SOT-23-5'
HOLE = 'MountingHole:MountingHole_3.2mm_M3'

# Each row carries the schematic and PCB pad map together. A blank net is NC.
parts = {
    'U1': ('MT6701CT-STD', HALL, (64, 64, 0), [
        ('1', 'VDD', 'power_in', '5V_IN'), ('2', 'MODE', 'input', '5V_IN'),
        ('3', 'OUT', 'output', 'ANGLE_RAW'), ('4', 'GND', 'power_in', 'GND'),
        ('5', 'PUSH', 'output', ''), ('6', 'SDA', 'bidirectional', 'SDA'),
        ('7', 'SCL', 'input', 'SCL'), ('8', 'Z_CSN', 'bidirectional', '')]),
    'U2': ('TLV9001IDBVR', AMP, (73, 57, 0), [
        ('1', 'OUT', 'output', 'ANGLE_BUF'), ('2', 'V-', 'power_in', 'GND'),
        ('3', 'IN+', 'input', 'ANGLE_SCALED'), ('4', 'IN-', 'input', 'ANGLE_BUF'),
        ('5', 'V+', 'power_in', '5V_IN')]),
    'J1': ('43045-0400', J1, (86.5, 63, 270), [
        ('1', 'GND', 'passive', 'GND'), ('2', '5V', 'passive', '5V_IN'),
        ('3', 'SIG', 'passive', 'TPS_OUT'), ('4', 'NC', 'passive', '')]),
    'J2': ('I2C service (DNP)', HEADER, (66.5, 73.5, 90), [
        ('1', 'GND', 'passive', 'GND'), ('2', 'SDA', 'passive', 'SDA'),
        ('3', 'SCL', 'passive', 'SCL')]),
}


def passive(ref, value, placement, first, second):
    lib = R if ref.startswith('R') else C
    parts[ref] = (value, lib, placement, [
        ('1', '~', 'passive', first), ('2', '~', 'passive', second)])


passive('C1', '100 nF', (58, 61.5, 180), '5V_IN', 'GND')
passive('C2', '1 uF', (58, 64, 180), '5V_IN', 'GND')
passive('C3', '100 nF', (77, 57, 0), '5V_IN', 'GND')
passive('R1', '100k 1%', (59, 68.5, 0), 'ANGLE_RAW', 'ANGLE_SCALED')
passive('R2', '1M 1%', (63, 68.5, 0), 'ANGLE_SCALED', 'GND')
passive('R3', '100R', (78, 54.5, 0), 'ANGLE_BUF', 'TPS_OUT')
passive('R4', '4.7k', (72, 69, 90), '5V_IN', 'SDA')
passive('R5', '4.7k', (75, 69, 90), '5V_IN', 'SCL')
for ref, x in [('H1', 52), ('H2', 76)]:
    parts[ref] = ('M3 mounting hole', HOLE, (x, 64, 0), [])


def q(value):
    return json.dumps(str(value), ensure_ascii=False)


def uid():
    return str(uuid4())


def make_schematic():
    root = uid()
    libs = []
    local_libs = []
    items = []
    positions = {
        'U1': (73.66, 68.58), 'U2': (165.10, 68.58), 'J1': (236.22, 68.58),
        'J2': (236.22, 104.14), 'C1': (48.26, 104.14), 'C2': (88.90, 104.14),
        'C3': (165.10, 104.14), 'R1': (48.26, 132.08), 'R2': (101.60, 132.08),
        'R3': (165.10, 132.08), 'R4': (48.26, 160.02), 'R5': (101.60, 160.02),
        'H1': (157.48, 160.02), 'H2': (185.42, 160.02),
        '#FLG01': (227.33, 135.89), '#FLG02': (247.65, 135.89),
    }
    flags = {
        '#FLG01': ('PWR_FLAG', '', None, [('1', '~', 'power_out', '5V_IN')]),
        '#FLG02': ('PWR_FLAG', '', None, [('1', '~', 'power_out', 'GND')]),
    }
    for ref, (value, footprint, _, pins) in (parts | flags).items():
        lib = f'TPS:{ref}'
        x, y = positions[ref]
        if ref in ('U1', 'U2'):
            left = (len(pins) + 1) // 2
            geometry = [(-12.7 if i < left else 12.7, 3.81 - (i if i < left else i-left)*2.54,
                         0 if i < left else 180) for i in range(len(pins))]
            drawing = '(rectangle (start -10.16 6.35) (end 10.16 -6.35) (stroke (width 0.25) (type default)) (fill (type background)))'
            offset = 10.16
        elif ref.startswith('J'):
            geometry = [(-5.08, 2.54-i*2.54, 0) for i in range(len(pins))]
            drawing = '(rectangle (start -2.54 5.08) (end 5.08 -7.62) (stroke (width 0.25) (type default)) (fill (type background)))'
            offset = 8.89
        elif ref.startswith('R'):
            geometry = [(-5.08, 0, 0), (5.08, 0, 180)]
            drawing = '(rectangle (start -2.54 1.02) (end 2.54 -1.02) (stroke (width 0.25) (type default)) (fill (type none)))'
            offset = 5.08
        elif ref.startswith('C'):
            geometry = [(-3.81, 0, 0), (3.81, 0, 180)]
            drawing = '(polyline (pts (xy -1.27 2.54) (xy -1.27 -2.54)) (stroke (width 0.4) (type default)) (fill (type none))) (polyline (pts (xy 1.27 2.54) (xy 1.27 -2.54)) (stroke (width 0.4) (type default)) (fill (type none)))'
            offset = 6.35
        else:
            geometry = [(0, 0, 90)] if pins else []
            drawing = '(circle (center 0 0) (radius 1.27) (stroke (width 0.25) (type default)) (fill (type none)))' if not pins else ''
            offset = 5.08

        electrical = []
        for (num, name, kind, net), (dx, dy, angle) in zip(pins, geometry):
            px, py = round(x+dx, 4), round(y-dy, 4)
            length = 0 if ref.startswith('#') else 2.54
            electrical.append(f'(pin {kind} line (at {dx} {dy:.4f} {angle}) (length {length}) (name {q(name)} (effects (font (size 1 1)))) (number {q(num)} (effects (font (size 1 1)))))')
            if not net:
                items.append(f'(no_connect (at {px} {py}) (uuid {uid()}))')
                continue
            end_x = round(px + (-3.81 if angle == 0 else 3.81), 4)
            items.append(f'(wire (pts (xy {px} {py}) (xy {end_x} {py})) (stroke (width 0) (type default)) (uuid {uid()}))')
            justification = 'right' if angle == 0 else 'left'
            items.append(f'(label {q(net)} (at {end_x} {py} 0) (effects (font (size 1 1)) (justify {justification} bottom)) (uuid {uid()}))')
        hide = '(pin_names hide) (pin_numbers hide)' if not ref.startswith(('U', 'J')) else '(pin_names (offset 0.5))'
        bom = 'no' if ref.startswith(('H', '#')) else 'yes'
        on_board = 'no' if ref.startswith('#') else 'yes'
        dnp = 'yes' if ref == 'J2' else 'no'
        properties = ''.join(f'(property {q(key)} {q(val)} (at 0 0 0) (effects (font (size 1.27 1.27))))'
                             for key, val in [('Reference', ref.rstrip('0123456789')), ('Value', value), ('Footprint', footprint)])
        definition = f'{hide} (in_bom {bom}) (on_board {on_board}) {properties} (symbol {q(ref+"_0_1")} {drawing}) (symbol {q(ref+"_1_1")} {" ".join(electrical)})'
        libs.append(f'(symbol {q(lib)} {definition})')
        local_libs.append(f'(symbol {q(ref)} {definition})')
        order_fields = ''
        if ref == 'U1':
            order_fields = f'(property "MPN" {q(value)} (at {x} {y} 0) (effects (font (size 1 1)) (hide yes)))'
            order_fields += f'(property "LCSC" "C5451785" (at {x} {y} 0) (effects (font (size 1 1)) (hide yes)))'
        items.append(f'''(symbol (lib_id {q(lib)}) (at {x} {y} 0) (unit 1)
          (in_bom {bom}) (on_board {on_board}) (dnp {dnp}) (uuid {SYMBOLS[ref]})
          (property "Reference" {q(ref)} (at {x} {y-offset:.4f} 0) (effects (font (size 1.27 1.27)) {'(hide yes)' if ref.startswith('#') else ''}))
          (property "Value" {q(value)} (at {x} {y-offset+2.54:.4f} 0) (effects (font (size 1.27 1.27))))
          (property "Footprint" {q(footprint)} (at {x} {y} 0) (effects (font (size 1 1)) (hide yes)))
          {order_fields}
          (instances (project {q(NAME)} (path {q('/'+root)} (reference {q(ref)}) (unit 1)))))''')
    for x, y, label in [(37, 47, 'Hall angle sensor and supply'), (141, 47, 'Buffered analog output'),
                        (218, 47, 'RTLM analog harness'), (218, 91, '5 V I2C service')]:
        items.append(f'(text {q(label)} (at {x} {y} 0) (effects (font (size 1.5 1.5) (bold yes)) (justify left)) (uuid {uid()}))')
    p = HERE / f'{NAME}.kicad_sch'
    library_body = '\n'.join(local_libs)
    (HERE / 'TPS.kicad_sym').write_text(f'(kicad_symbol_lib (version 20241209) (generator kicad_symbol_editor)\n{library_body})\n', encoding='utf8')
    (HERE / 'sym-lib-table').write_text('(sym_lib_table (version 7) (lib (name "TPS") (type "KiCad") (uri "${KIPRJMOD}/TPS.kicad_sym") (options "") (descr "TPS-01 symbols")))\n', encoding='utf8')
    (HERE / f'{NAME}.kicad_pro').write_text('{}\n', encoding='utf8')
    p.write_text(f'''(kicad_sch (version 20250114) (generator eeschema) (uuid {root})
      (paper "A4") (title_block (title "RTLM throttle position sensor") (rev "0.2"))
      (lib_symbols {' '.join(libs)})\n{chr(10).join(items)})\n''', encoding='utf8')
    return root


def point(xy):
    return pcb.VECTOR2I(*(pcb.FromMM(v) for v in xy))


def apply_silkscreen(board):
    # Retain component artwork for assembly drawings on the fabrication layers.
    for footprint in board.GetFootprints():
        for item in footprint.GraphicalItems():
            if item.GetLayer() == pcb.F_SilkS:
                item.SetLayer(pcb.F_Fab)
            elif item.GetLayer() == pcb.B_SilkS:
                item.SetLayer(pcb.B_Fab)
        for field in footprint.GetFields():
            if field.GetLayer() in (pcb.F_SilkS, pcb.B_SilkS):
                field.SetVisible(False)
    for item in list(board.GetDrawings()):
        if item.GetLayer() in (pcb.F_SilkS, pcb.B_SilkS):
            board.Remove(item)

    # Eight paths of the RTLM wordmark from assets/Logo-Card-White.svg, in mm.
    paths = [
        [(53.545, 53.371), (56.343, 53.371), (56.011, 53.946), (55.898, 54.1), (55.765, 54.211), (55.61, 54.277), (55.434, 54.299), (53.009, 54.299), (53.545, 53.371)],
        [(52.849, 54.521), (54.175, 54.521), (53.205, 56.201), (53.122, 56.317), (53.024, 56.4), (52.912, 56.45), (52.787, 56.466), (51.725, 56.466), (52.849, 54.521)],
        [(57.12, 52.752), (57.19, 52.655), (57.271, 52.586), (57.364, 52.544), (57.469, 52.531), (58.575, 52.531), (58.089, 53.371), (59.549, 53.371), (59.217, 53.946), (59.105, 54.1), (58.975, 54.211), (58.826, 54.277), (58.659, 54.299), (57.553, 54.299), (56.787, 55.626), (57.871, 55.626), (57.513, 56.245), (57.444, 56.342), (57.362, 56.411), (57.269, 56.452), (57.165, 56.466), (55.661, 56.466), (55.386, 56.423), (55.246, 56.295), (55.241, 56.081), (55.371, 55.781), (57.12, 52.752)],
        [(60.588, 52.221), (60.658, 52.124), (60.739, 52.055), (60.832, 52.014), (60.937, 52.0), (62.087, 52.0), (59.661, 56.201), (59.578, 56.317), (59.48, 56.4), (59.369, 56.45), (59.243, 56.466), (58.137, 56.466), (60.588, 52.221)],
        [(61.521, 53.592), (61.591, 53.495), (61.672, 53.426), (61.765, 53.385), (61.87, 53.371), (67.884, 53.371), (68.186, 53.418), (68.339, 53.559), (68.345, 53.794), (68.202, 54.123), (67.002, 56.201), (66.918, 56.317), (66.821, 56.4), (66.709, 56.45), (66.583, 56.466), (65.478, 56.466), (66.627, 54.476), (66.66, 54.399), (66.659, 54.344), (66.623, 54.31), (66.552, 54.299), (65.579, 54.299), (64.481, 56.201), (64.398, 56.317), (64.3, 56.4), (64.188, 56.45), (64.063, 56.466), (62.957, 56.466), (64.208, 54.299), (62.484, 54.299), (61.386, 56.201), (61.302, 56.317), (61.205, 56.4), (61.093, 56.45), (60.967, 56.466), (59.862, 56.466), (61.521, 53.592)],
        [(51.764, 53.371), (53.246, 53.371), (52.71, 54.299), (51.228, 54.299), (51.764, 53.371)],
        [(51.138, 54.521), (52.583, 54.521), (52.111, 55.339), (50.666, 55.339), (51.138, 54.521)],
        [(50.471, 55.648), (51.907, 55.648), (51.435, 56.466), (49.998, 56.466), (50.471, 55.648)],
    ]
    for vertices in paths:
        logo = pcb.PCB_SHAPE(board)
        logo.SetShape(pcb.SHAPE_T_POLY)
        polygon = pcb.SHAPE_POLY_SET()
        polygon.NewOutline()
        for vertex in vertices:
            xy = point(vertex)
            polygon.Append(xy.x, xy.y)
        logo.SetPolyShape(polygon)
        logo.SetLayer(pcb.F_SilkS)
        logo.SetWidth(0)
        logo.SetFilled(True)
        board.Add(logo)
    title = pcb.PCB_TEXT(board)
    title.SetText('Pedal Position Sensor')
    title.SetPosition(point((60, 58.25)))
    title.SetLayer(pcb.F_SilkS)
    title.SetTextSize(point((1.0, 1.0)))
    title.SetTextThickness(pcb.FromMM(.17))
    board.Add(title)


def route(track, via):
    # Short local bypass connections and ground returns.
    track('5V_IN', 'U1.1', (60.0, 62.095), (59.405, 61.5), 'C1.1', width=.35)
    track('5V_IN', 'C1.1', 'C2.1', width=.30)
    track('5V_IN', 'U1.2', (59.41, 63.365), 'C2.1', width=.30)
    track('5V_IN', 'U2.5', (75.275, 56.05), 'C3.1', width=.30)
    for pad, location in [
        ('U1.4', (62.9, 66.565)), ('U2.2', (70.66, 57)),
        ('C1.2', (56.05, 61.5)), ('C2.2', (56.05, 64)), ('C3.2', (78.95, 57)),
        ('R2.2', (64.85, 68.5)),
    ]:
        track('GND', pad, location)
        via('GND', location)

    for pad, location in [('C1.1', (58.775, 60.37)), ('C3.1', (76.225, 58.22)),
                          ('R4.1', (72, 70.9)), ('R5.1', (75, 70.9))]:
        track('5V_IN', pad, location, width=.30)
        via('5V_IN', location)
    track('5V_IN', 'J1.2', (85, 64.5), (85, 58.7), (82.3, 56), (78.445, 56), (76.225, 58.22),
          (76.225, 55.0), (74.225, 53), (61.4, 53), (58.775, 55.625), (58.775, 60.37),
          layer=pcb.B_Cu, width=.45)
    track('5V_IN', 'J1.2', (84, 69), (79.4, 69), (77.5, 70.9), (75, 70.9), (72, 70.9),
          layer=pcb.B_Cu, width=.45)

    # The high-impedance divider drives only the buffer. R3 isolates cable capacitance.
    track('ANGLE_RAW', 'U1.3', (60.4, 64.635), (59.8, 65.235), (59.8, 66.1),
          (58.175, 67.725), 'R1.1')
    track('ANGLE_SCALED', 'R1.2', (60.65, 68.5), 'R2.1')
    track('ANGLE_SCALED', (60.65, 68.5), (60.65, 67.35))
    via('ANGLE_SCALED', (60.65, 67.35))
    track('ANGLE_SCALED', (60.65, 67.35), (69.4, 58.6), (70.35, 58.6), layer=pcb.B_Cu)
    via('ANGLE_SCALED', (70.35, 58.6))
    track('ANGLE_SCALED', (70.35, 58.6), (71.0, 57.95), 'U2.3')
    track('ANGLE_BUF', 'U2.1', (72.5, 56.05), (73.08, 56.63), (73.08, 57.5),
          (73.53, 57.95), 'U2.4', width=.22)
    track('ANGLE_BUF', 'U2.1', (71.1, 56.05), (70.6, 55.55), (70.6, 54.3),
          (71.4, 53.5), (76.175, 53.5), 'R3.1')
    track('TPS_OUT', 'R3.2', (80, 54.5), (84, 58.5), 'J1.3')

    track('SDA', 'U1.6', (68.8, 64.635), (72, 67.835), 'R4.2')
    track('SDA', 'R4.2', (70.16, 70.015), (70.16, 72.38), 'J2.2')
    track('SCL', 'U1.7', (69.4, 63.365), (71.565, 65.53), (72.355, 65.53), 'R5.2')
    track('SCL', 'R5.2', (73.95, 69.225), (73.95, 71.13), 'J2.3')


def make_board(root):
    board = pcb.BOARD()
    board.SetCopperLayerCount(2)
    ground = 'GND'
    nets = {}
    pads = {}
    for ref, (value, footprint, (x, y, angle), pins) in parts.items():
        library, name = footprint.split(':')
        f = pcb.FootprintLoad(str(LIB / (library+'.pretty')), name)
        f.SetFPID(pcb.LIB_ID(library, name))
        f.SetReference(ref)
        f.SetValue(value)
        f.SetPosition(point((x, y)))
        f.SetOrientationDegrees(angle)
        f.SetPath(pcb.KIID_PATH(f'/{root}/{SYMBOLS[ref]}'))
        if ref == 'U1':
            f.SetFields({'MPN': value, 'LCSC': 'C5451785'})
            for field in ('MPN', 'LCSC'):
                f.GetField(field).SetVisible(False)
        f.Value().SetVisible(False)
        f.Reference().SetVisible(False)
        if ref == 'J2':
            f.SetAttributes(f.GetAttributes() | pcb.FP_DNP)
        if ref.startswith('H'):
            f.SetAttributes(f.GetAttributes() | pcb.FP_EXCLUDE_FROM_BOM | pcb.FP_EXCLUDE_FROM_POS_FILES)
        board.Add(f)
        mapping = {num: (name, kind, netname) for num, name, kind, netname in pins}
        for p in f.Pads():
            num = p.GetNumber()
            if num not in mapping:
                continue
            name, kind, netname = mapping[num]
            p.SetPinType(kind if netname else 'no_connect')
            key = netname or f'unconnected-({ref}-{name}-Pad{num})'
            full_name = '/' + key if netname else key
            if key not in nets:
                nets[key] = pcb.NETINFO_ITEM(board, full_name)
                board.Add(nets[key])
            p.SetNet(nets[key])
            pads[ref + '.' + num] = tuple(round(pcb.ToMM(v), 5) for v in p.GetPosition())

    outline = [(48, 51), (96, 51), (96, 77), (48, 77)]
    for a, b in zip(outline, outline[1:] + outline[:1]):
        edge = pcb.PCB_SHAPE(board)
        edge.SetShape(pcb.SHAPE_T_SEGMENT)
        edge.SetLayer(pcb.Edge_Cuts)
        edge.SetStart(point(a))
        edge.SetEnd(point(b))
        edge.SetWidth(pcb.FromMM(.05))
        board.Add(edge)

    apply_silkscreen(board)

    def track(net, *vertices, layer=pcb.F_Cu, width=.25):
        vertices = [pads[v] if isinstance(v, str) else v for v in vertices]
        for a, b in zip(vertices, vertices[1:]):
            if a == b:
                continue
            t = pcb.PCB_TRACK(board)
            t.SetStart(point(a))
            t.SetEnd(point(b))
            t.SetWidth(pcb.FromMM(width))
            t.SetLayer(layer)
            t.SetNet(nets[net])
            board.Add(t)

    def via(net, xy):
        v = pcb.PCB_VIA(board)
        v.SetPosition(point(xy))
        v.SetViaType(pcb.VIATYPE_THROUGH)
        v.SetLayerPair(pcb.F_Cu, pcb.B_Cu)
        v.SetWidth(pcb.FromMM(.6))
        v.SetDrill(pcb.FromMM(.3))
        v.SetNet(nets[net])
        board.Add(v)

    if not ROUTE:
        print(pads)
    else:
        route(track, via)
        zone = pcb.ZONE(board)
        zone.SetLayer(pcb.B_Cu)
        zone.SetNet(nets[ground])
        zone.SetLocalClearance(pcb.FromMM(.25))
        zone.SetMinThickness(pcb.FromMM(.2))
        zone.SetPadConnection(pcb.ZONE_CONNECTION_FULL)
        polygon = zone.Outline()
        polygon.NewOutline()
        for xy in outline:
            vector = point(xy)
            polygon.Append(vector.x, vector.y)
        board.Add(zone)
        pcb.ZONE_FILLER(board).Fill(board.Zones())
    pcb.SaveBoard(str(HERE / f'{NAME}.kicad_pcb'), board)


ROUTE = '--placement' not in sys.argv
SYMBOLS = {ref: uid() for ref in [*parts, '#FLG01', '#FLG02']}


if __name__ == '__main__':
    make_board(make_schematic())


