#!/usr/bin/env python
# Author: Noa Arama


from typing import IO
import random

class ArtConfig:

	def __init__(self):
		'''ArtConfig initilizer'''
		self.shape = random.randint(0,3)
		self.xcord = random.randint(0,801)
		self.ycord = random.randint(0, 501)
		self.cirRad = random.randint(0, 100)
		self.eliSRad = random.randint(10,30)
		self.eliRad = random.randint(10,30)
		self.rectWidth = random.randint(10,100)
		self.rectHeight = random.randint(10,100)
		self.red = random.randint(0,255)
		self.green = random.randint(0,255)
		self.blue = random.randint(0,255)
		self.opa = random.random()

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
	    fnam: str = "a431.html"
	    oneTitle = "My Art"
	    f: IO[str] = open(fnam, "w")
	    HtmlDoc.writeHTMLHeader(f, oneTitle)
	    SvgCanvas.openSVGcanvas(f, 1, (800,500))
	    SvgCanvas.genArtOne(f, 2)
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
	def genArtOne(f: IO[str], t: int) -> None:
	   """genART method"""
	   i = 0
	   while i < 100:
	   		s1 = ArtConfig()
	   		s2 = ArtConfig()
	   		s3 = ArtConfig()
	   		Circle.drawCircleLine(f,t,Circle((s1.xcord,s1.ycord,s1.cirRad), (s1.red , s1.green, s1.blue, s1.opa)))
	   		# Ellipse.drawEllipseLine(f,t,Ellipse((s2.xcord, s2.ycord, s2.eliSRad, s2.eliRad), (s2.red , s2.green, s2.blue, s2.opa)))
	   		# Rectangle.drawRectangleLine(f,t,Rectangle((s3.xcord, s3.ycord, s3.rectWidth, s3.rectHeight), (s3.red , s3.green, s3.blue, s3.opa)))
	   		i = i+1
        
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
