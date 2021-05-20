<?xml version="1.0"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0"> 
<xsl:output method="text" version="1.0" encoding="UTF-8" indent="no" omit-xml-declaration="yes"/>
<xsl:template match="sums"><![CDATA[<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<style>
.button {
  border:2px solid #000000;
  color:#000000;
  font-family:Arial;
  font-size:24px;
  font-weight:bold;
  height:68px;
  width:256px;
  max-width:256px;
  margin:18px;
}
.green {
  background-color:#44c767;
}
.red {
  background-color:#ff4040;
}
.yellow {
  background-color:#ffec23;
}
body {
  background: linear-gradient(to right,]]><xsl:value-of select="bg"/><![CDATA[,black);
  text-align:center;
  display:block;
}
.center {
  margin: 0;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}
.topleft {
  color:#FFFFFF;
  margin:12px;
  position:absolute;
  top: 0%;
  left: 0%;
}
</style>
</head>
<body>
<a href="https://www.github.com/Sphinxtar/DeezNetz"><h4 class="topleft">DeezNetz by Linus Sphinx</h4></a>
<div class="center">
<div><button type="button" class="button red" onclick="window.location.href='red.html'">Red: ]]><xsl:value-of select="red"/><![CDATA[</button></div>
<div><button type="button" class="button yellow" onclick="window.location.href='yellow.html'">Yellow: ]]><xsl:value-of select="yellow"/><![CDATA[</button></div>
<div><button type="button" class="button green" onclick="window.location.href='green.html'">Green: ]]><xsl:value-of select="green"/><![CDATA[ </button></div>
</div>
</body>
</html>]]>
</xsl:template> 
</xsl:stylesheet>

