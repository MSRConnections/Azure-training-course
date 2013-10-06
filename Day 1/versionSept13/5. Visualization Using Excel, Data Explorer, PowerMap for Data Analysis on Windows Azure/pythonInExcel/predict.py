from time import sleep

for sheet in all_sheets():
    active_sheet(sheet)
    if Cell("A1").value == 'Carat':
        display_sheet(sheet)
        break

data = zip(CellRange("A2:A53941").value,
           CellRange("E2:E53941").value)
data.sort()

# formatting

Cell("H2").copy_from(Cell("A2"))
Cell("I2").copy_from(Cell("E2"))
Cell("H2:I2").color = 'white'
CellRange("H1:I1").value = ["Carat", "Price"]
CellRange("H1:I1").font.bold = True
CellRange("H1:I1").font.italic = True
Cell("H2").font.color = '0x3f3f76'
Cell("I2").color = '0xdaeef3'
Cell("I2").font.color = '0x002060'

def price(carat):
    if carat == None:
        return ''
    elif not data[0][0] <= carat <= data[-1][0]:
        return "data out of bounds"
    for d_carat, d_price in data:
        if d_carat >= carat:
            return d_price

cur_val = Cell("H2").value
autofit()

while True:
    next_val = Cell("H2").value
    if next_val != cur_val:
        cur_val = next_val
        Cell("I2").value = price(cur_val)
        autofit()
    sleep(0.1)
