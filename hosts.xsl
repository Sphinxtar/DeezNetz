<?xml version="1.0"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
<xsl:output method="text" version="1.0" encoding="UTF-8" indent="no" omit-xml-declaration="yes"/>
<xsl:template match="hosts"><![CDATA[<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<script>
async function getErr(hostName) {
const status = await fetch("http://"+hostName+":8142/]]><xsl:value-of select="msg"/><![CDATA[");
const bs = await status.text();
alert(bs);
}
</script>
<style>
.button {
  color:#000000;
  font-family:Arial;
}
.counts {
  border:2px solid #000000;
  font-size:16px;
  font-weight:bold;
  height:28px;
  width:192px;
  margin:14px;
}
.host {
  background-color:#ffffff;
  border:1px solid #000000;
  font-size:16px;
  font-weight:normal;
  height:24px;
  width:256px;
  margin:4px;
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
.hosts {
  margin:24px;
}
body {
  background: linear-gradient(to right,]]><xsl:value-of select="bg"/><![CDATA[,black);
  text-align:center;
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
<a href="index.html"><h4 class="topleft">DeezNetz by Linus Sphinx</h4></a>
<button type="button" class="button counts red" onclick="window.location.href='red.html'">Red: ]]><xsl:value-of select="red"/><![CDATA[</button>
<button type="button" class="button counts yellow" onclick="window.location.href='yellow.html'">Yellow: ]]><xsl:value-of select="yellow"/><![CDATA[</button>
<button type="button" class="button counts green" onclick="window.location.href='green.html'">Green: ]]><xsl:value-of select="green"/><![CDATA[</button>
<div class="hosts">]]><xsl:for-each select="host"><![CDATA[<span><button type="button" class="host" onclick="getErr(']]><xsl:value-of select="@name"/><![CDATA[')">]]><xsl:value-of select="@name"/><![CDATA[</button></span>]]></xsl:for-each><![CDATA[</div>
</body>
</html>]]>
</xsl:template>
</xsl:stylesheet>
