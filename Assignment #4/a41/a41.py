#!/usr/bin/env python
# Author: Noa Arama

from typing import IO

class HtmlDoc:

	def writeHTMLline(f: IO[str], t: int, line: str) -> None:
	     """writeLineHTML method"""
	     ts = "   " * t
	     f.write(f"{ts}{line}\n")

	def writeHTMLHeader(f: IO[str], winTitle: str) -> None:
	    """writeHeadHTML method"""
	    HtmlDoc.writeHTMLline(f, 0, "<html>")
	    HtmlDoc.writeHTMLline(f, 0, "<head>")
	    HtmlDoc.writeHTMLline(f, 1, f"<title>{winTitle}</title>")
	    HtmlDoc.writeHTMLline(f, 0, "</head>")
	    HtmlDoc.writeHTMLline(f, 0, "<body>")

	def writeHTMLfile() -> None:
	    """writeHTMLfile method"""
	    fnam: str = "a41.html"
	    winTitle = "My Art"
	    f: IO[str] = open(fnam, "w")
	    HtmlDoc.writeHTMLHeader(f, winTitle)
	    SvgCanvas.openSVGcanvas(f, 1, (500,300))
	    SvgCanvas.genArt(f, 2)
	    SvgCanvas.closeSVGcanvas(f, 1)
	    f.close()

	def writeHTMLcomment(f: IO[str], t: int, com: str) -> None:
	    """writeHTMLcomment method"""
	    ts: str = "   " * t
	    f.write(f"{ts}<!--{com}-->\n")

class SvgCanvas:
	'''
	This class should generate the tags for svg in the
	html file.
	'''
	def genArt(f: IO[str], t: int) -> None:
	   """genART method"""
	   # Circle.drawCircleLine(f, t, Circle((50,50,50), (255,0,0,1.0)))
	   # Circle.drawCircleLine(f, t, Circle((150,50,50), (255,0,0,1.0)))
	   # Circle.drawCircleLine(f, t, Circle((250,50,50), (255,0,0,1.0)))
	   # Circle.drawCircleLine(f, t, Circle((350,50,50), (255,0,0,1.0)))
	   # Circle.drawCircleLine(f, t, Circle((450,50,50), (255,0,0,1.0)))
	   # Circle.drawCircleLine(f, t, Circle((50,250,50), (0,0,255,1.0)))
	   # Circle.drawCircleLine(f, t, Circle((150,250,50), (0,0,255,1.0)))
	   # Circle.drawCircleLine(f, t, Circle((250,250,50), (0,0,255,1.0)))
	   # Circle.drawCircleLine(f, t, Circle((350,250,50), (0,0,255,1.0)))
	   # Circle.drawCircleLine(f, t, Circle((450,250,50), (0,0,255,1.0)))
	   Rectangle.drawRectangleLine(f,t,Rectangle((50,50,50,60),(255,0,0,1.0)))
        
	def openSVGcanvas(f: IO[str], t: int, canvas: tuple) -> None:
	     """openSVGcanvas method"""
	     ts: str = "   " * t
	     HtmlDoc.writeHTMLcomment(f, t, "Define SVG drawing box")
	     f.write(f'{ts}<svg width="{canvas[0]}" height="{canvas[1]}">\n')

	def closeSVGcanvas(f: IO[str], t: int) -> None:
	    """closeSVGcanvas method"""
	    ts: str = "   " * t
	    f.write(f"{ts}</svg>\n")
	    f.write(f"</body>\n")
	    f.write(f"</html>\n")


class Circle:
	'''
	This class is responsible for the circles in the
	artwork.
	'''
	def __init__(self, cir: tuple, col: tuple) -> None:
		self.cx: int = cir[0]
		self.cy: int = cir[1]
		self.rad: int = cir[2]
		self.red: int = col[0]
		self.green: int = col[1]
		self.blue: int = col[2]
		self.op: float = col[3]

	def drawCircleLine(f: IO[str], t: int, c) -> None:
		"""drawCircle method"""
		ts: str = "   " * t
		line1: str = f'<circle cx="{c.cx}" cy="{c.cy}" r="{c.rad}" '
		line2: str = f'fill="rgb({c.red}, {c.green}, {c.blue})" fill-opacity="{c.op}"></circle>'
		f.write(f"{ts}{line1+line2}\n")


class Ellipse:
	'''
	This class is responsible for the ellipses in the
	artwork.
	'''
	def __init__(self, eli: tuple, col: tuple) -> None:
		self.cx: int = eli[0]
		self.cy: int = eli[1]
		self.radx: int = eli[2]
		self.rady: int = eli[3]
		self.red: int = col[0]
		self.green: int = col[1]
		self.blue: int = col[2]
		self.op: float = col[3]

	def drawEllipseLine(f: IO[str], t: int , e):
		"""drawEllipse method"""
		ts: str = "   " * t
		line1: str = f'<ellipse cx="{e.cx}" cy="{e.cy}" rx="{e.radx}" ry="{e.rady}" '
		line2: str = f'fill="rgb({e.red}, {e.green}, {e.blue})" fill-opacity="{e.op}"></ellipse>'
		f.write(f"{ts}{line1+line2}\n")


class Rectangle:
	'''
	This class is responsible for the rectangles in the
	artwork.
	'''
	def __init__(self, rect: tuple, col: tuple) -> None:
		self.rx: int = rect[0]
		self.ry: int = rect[1]
		self.width: int = rect[2]
		self.height: int = rect[3]
		self.red: int = col[0]
		self.green: int = col[1]
		self.blue: int = col[2]
		self.op: float = col[3]

	def drawRectangleLine(f: IO[str], t: int , r):
		"""drawEllipse method"""
		ts: str = "   " * t
		line1: str = f'<rect x="{r.rx}" y="{r.ry}" width="{r.width}" height="{r.height}" '
		line2: str = f'fill="rgb({r.red}, {r.green}, {r.blue})" fill-opacity="{r.op}"/>'
		f.write(f"{ts}{line1+line2}\n")

def main() -> None:
    """main method"""
    HtmlDoc.writeHTMLfile()

if __name__ == "__main__":
    main()

